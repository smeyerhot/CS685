
from transformers import AutoModelForCausalLM, AutoTokenizer, AdamW, GPT2LMHeadModel, GPT2DoubleHeadsModel, GPT2TokenizerFast, GPT2Config, BertTokenizer

from transformers.modeling_outputs import CausalLMOutputWithCrossAttentions
from transformers.models.gpt2.modeling_gpt2 import GPT2DoubleHeadsModelOutput
import copy
import torch
import numpy as np
import torch.nn as nn
import torch.nn.functional as F
from pytorch_pretrained_bert.modeling_gpt2 import GPT2PreTrainedModel, GPT2MultipleChoiceHead, GPT2Model, GPT2LMHead, Attention, Block, \
    LayerNorm, MLP
    
# One problem with BudgieNet is it suffers from the credit assignment problem that comes with generating discrete tokens. We want to
# pass back a signal on the sentence level but are unable to do anything but on a word level.

class BudgieNet(GPT2LMHeadModel):
    def __init__(self, config):
        super().__init__(config)
        self.interesting_head = GPT2LMHead(self.transformer.wte.weight, config)
        self.funny_head = GPT2LMHead(self.transformer.wte.weight, config)
        self.choosing_head = nn.Linear(self.transformer.wte.weight.size()[-1], 2)
        self.choice_dispatch = {0: self.interesting_head, 1: self.funny_head}
        self.rewards = {0: [], 1: []}  # max rewards hardcoded with even distribution of funny and interesting ie. 5:5
        self.correct = {0: [], 1: []} 
        self.scores = {0: [], 1: []}
        self.probs = {0: [], 1: []}
        self.combined_logits = {0: [], 1: []}
        self.logits = []
        self.chosen_head = None
        self.batch_size = 2
        self.index = 0
        self.choice = 0
        self.generating = False
        self.generation_step = -1

    def reset_state(self):
        self.generation_step = -1
        self.rewards = {0: [] , 1: []}  
        self.correct = {0: [], 1: []} 
        self.scores = {0: [], 1: []}
        self.probs = {0: [], 1: []}
        self.combined_logits = {0: [], 1: []}
        self.stop_generation()
        self.generation_step = -1

    def affirm_social(self, correct):
        if correct:
            self.correct[self.choice].append(1)
        else:    
            self.correct[self.choice].append(0)

    def affirm_reward(self, value):
        self.rewards[self.choice].append(value)
        
    def start_generation(self):
        self.generating = True

    def stop_generation(self):
        self.generating = False
        self.generation_step = -1

    def combine_logits(self):
        logits = torch.stack(self.logits)
        mean_logits = torch.mean(logits, dim=0).squeeze()
        self.combined_logits[self.choice].append(mean_logits)
        self.logits.clear()

    def increment(self):
        self.index += 1

    def choose(self, sentence):
        scores = F.relu(self.choosing_head(sentence))
        probs = F.softmax(scores, dim=-1)
        prob = torch.max(probs)
        idx = torch.argmax(probs)
        self.choice = idx.item()
        self.probs[self.choice].append(prob.item())
        self.scores[self.choice].append(scores)

    def calculate_rewarded_loss(self):
        loss = 0
        for i in range(2):
            combined = self.combined_logits[i]
            if not len(combined):
                loss += 0
                continue

            logits = torch.stack(combined, dim=0)
            rewards = torch.tensor(self.rewards[i])
            flipped_logits = torch.transpose(logits, 0, 1)
            rewarded_logits = torch.multiply(flipped_logits, rewards)
            rewarded_logits = torch.transpose(rewarded_logits, 0, 1)
            scores = torch.mean(rewarded_logits, dim=0)
            probs = F.softmax(scores, dim=-1)
            prob = torch.max(probs)
            print(f"reward prob: {prob}")
            loss += -1 * torch.log(prob)

        return loss

    def calculate_cross_entropy(self):
        loss = 0 
        for i in range(2):    
            iprobs = self.probs[i]
            original_length = len(iprobs)
            if not len(iprobs):
                loss += 0
                continue

            probs = torch.tensor(iprobs)
            mask = torch.tensor(self.correct[i], dtype=bool)
            partial_loss = torch.sum(probs[mask], dim=0) / original_length
            print(f"choice prob: {partial_loss}")
            partial_loss = -1 * torch.log(partial_loss)
            loss += partial_loss

        return loss

    def calculate_total_loss(self):
       return self.calculate_rewarded_loss() + self.calculate_cross_entropy()

    @torch.enable_grad()    
    def forward(
            self,
            input_ids=None,
            past_key_values=None,
            attention_mask=None,
            token_type_ids=None,
            position_ids=None,
            head_mask=None,
            inputs_embeds=None,
            labels=None,
            use_cache=None,
            output_attentions=None,
            output_hidden_states=None,
            return_dict=None,
        ):  
      
        transformer_outputs = self.transformer(
            input_ids=input_ids,
            past_key_values=past_key_values,
            attention_mask=attention_mask,
            token_type_ids=token_type_ids,
            position_ids=position_ids,
            head_mask=head_mask,
            inputs_embeds=inputs_embeds,
            use_cache=use_cache,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
            return_dict=return_dict,
        )

        last_hidden_state = transformer_outputs.last_hidden_state
        hidden_states = transformer_outputs.hidden_states
        past = transformer_outputs.past_key_values
        lm_logits = None
        loss = None
        if self.playmode:
            self.chosen_head = self.choice_dispatch[0]
            lm_logits = self.chosen_head(last_hidden_state)
            return CausalLMOutputWithCrossAttentions(
            loss=loss,
            logits=lm_logits,
            past_key_values=past,
            hidden_states=transformer_outputs.hidden_states,
            attentions=transformer_outputs.attentions,
          )
        if self.generating:
            lm_logits = self.chosen_head(last_hidden_state)
            if self.generation_step > 0:
                print(f"lm_logits.size: {lm_logits.size()}")
                self.logits.append(lm_logits)
        else:
            self.chosen_head = self.choice_dispatch[self.choice]
        
        self.generation_step += 1

        return CausalLMOutputWithCrossAttentions(
            loss=loss,
            logits=lm_logits,
            past_key_values=past,
            hidden_states=transformer_outputs.hidden_states,
            attentions=transformer_outputs.attentions,
        )
    