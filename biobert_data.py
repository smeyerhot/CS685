import torch
from torch.utils.data import Dataset
import numpy as np
import pandas as pd

torch.manual_seed(42)

class BioBERTGPT2Dataset(Dataset):

  def __init__(self, df, encoder_tokenizer, decoder_tokenizer=None, gpt2_type="gpt2", max_length=768, decoder_only=True, eos=False, padding=True):

    self.encoder_tokenizer = encoder_tokenizer
    self.decoder_tokenizer = decoder_tokenizer
    self.input_ids = []
    self.decoder_ids = []
    self.both_ids = []
    self.attn_masks = []
    self.decoder_attn_masks = []
    self.both_attn_masks = []
    self.id_nums = df.id.copy()
    self.decoder_only = decoder_only

    encoder_txt = df.gpt_input.copy()
    decoder_txt = df.decoder.copy()

    for i in range(len(encoder_txt)):
        if padding:
            if decoder_only:
                encoder_dict = encoder_tokenizer(encoder_txt[i] + encoder_tokenizer.eos_token, truncation=True, max_length=max_length, padding="max_length")
                decoder_dict = encoder_tokenizer(decoder_txt[i][0] + encoder_tokenizer.eos_token, truncation=True, max_length=max_length, padding="max_length")
                both_dict = encoder_tokenizer(encoder_txt[i] + decoder_txt[i][0] + encoder_tokenizer.eos_token, truncation=True, max_length=max_length, padding="max_length")
            else:
                if eos:
                    encoder_dict = encoder_tokenizer(encoder_txt[i] + encoder_tokenizer.eos_token, truncation=True, max_length=max_length, padding="max_length")
                    decoder_dict = decoder_tokenizer(decoder_txt[i][0] + decoder_tokenizer.eos_token, truncation=True, max_length=max_length, padding="max_length")
                else:
                    encoder_dict = encoder_tokenizer(encoder_txt[i], truncation=True, max_length=max_length, padding="max_length")
                    decoder_dict = decoder_tokenizer(decoder_txt[i][0], truncation=True, max_length=max_length, padding="max_length")
        else:
            if decoder_only:
                encoder_dict = encoder_tokenizer(encoder_txt[i] + encoder_tokenizer.eos_token, truncation=True, max_length=max_length)
                decoder_dict = encoder_tokenizer(decoder_txt[i][0] + encoder_tokenizer.eos_token, truncation=True, max_length=max_length)
                both_dict = encoder_tokenizer(encoder_txt[i] + decoder_txt[i][0] + encoder_tokenizer.eos_token, truncation=True, max_length=1000)
            else:
                if eos:
                    encoder_dict = encoder_tokenizer(encoder_txt[i] + encoder_tokenizer.eos_token, truncation=True, max_length=max_length)
                    decoder_dict = decoder_tokenizer(decoder_txt[i][0] + decoder_tokenizer.eos_token, truncation=True, max_length=max_length)
                else:
                    encoder_dict = encoder_tokenizer(encoder_txt[i], truncation=True, max_length=max_length)
                    decoder_dict = decoder_tokenizer(decoder_txt[i][0], truncation=True, max_length=max_length)
            
        self.decoder_ids.append(torch.tensor(decoder_dict['input_ids']))
        self.decoder_attn_masks.append(torch.tensor(decoder_dict['attention_mask']))

        self.input_ids.append(torch.tensor(encoder_dict['input_ids']))
        self.attn_masks.append(torch.tensor(encoder_dict['attention_mask']))

        self.both_ids.append(torch.tensor(both_dict["input_ids"]))
        self.both_attn_masks.append(torch.tensor(both_dict["attention_mask"]))
    
  def __len__(self):
    return len(self.input_ids)

  def __getitem__(self, idx):
    return self.input_ids[idx], self.decoder_ids[idx], self.id_nums[idx], self.attn_masks[idx], self.decoder_attn_masks[idx], self.both_ids[idx], self.both_attn_masks[idx]