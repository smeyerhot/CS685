import torch
from torch.utils.data import Dataset
import numpy as np
import pandas as pd

def preprocessing(cd_df):
    encoder_text = []
    decoder_text = []
    all_fields = []
    visited = []
    id_num = []
    text = []

    for j, dial in enumerate(cd_df["dialogue_turns"]):
        encoder_temp = []
        decoder_temp = []
        u = dial["utterance"]

        visited = [False] * len(u)
        
        while not all(visited):
            text.append([''.join(u)])
            for i in range(len(u)):
                if visited[i] == True:
                    encoder_temp.append(u[i])
                else:
                    if i % 2 == 0:
                        encoder_temp.append(u[i])
                        visited[i] = True
                    else:
                        decoder_temp.append(u[i])
                        visited[i] = True
                        break
            
            id_num.append(j)

            encoder = " ".join(encoder_temp)
            decoder = " ".join(decoder_temp)
            encoder_text.append([encoder])
            decoder_text.append([decoder])
            encoder_temp = []
            decoder_temp = []

    all_fields = [id_num, encoder_text, decoder_text, text]
    all_fields = np.transpose(np.array(all_fields).reshape((4, -1)))
    qa_df = pd.DataFrame(all_fields, columns=["id", "encoder", "decoder", "text"])
    qa_df.head()

    return qa_df


def split_data(dataset, sizes):
    train_size = sizes[0]
    val_size = sizes[1]
    test_size = sizes[2]

    indices = torch.randperm(sum(sizes)).tolist()
    train_idx = indices[:train_size]
    val_idx = indices[train_size : train_size+val_size]
    test_idx = indices[train_size+val_size:]
    
    train = dataset.iloc[train_idx, :]
    validation = dataset.iloc[val_idx, :]
    test = dataset.iloc[test_idx, :]

    return train, validation, test


class GPT2Dataset(Dataset):

  def __init__(self, df, encoder_tokenizer, decoder_tokenizer, gpt2_type="gpt2", max_length=768, decoder_only=True):

    self.encoder_tokenizer = encoder_tokenizer
    self.decoder_tokenizer = decoder_tokenizer
    self.input_ids = []
    self.decoder_ids = []
    self.attn_masks = []
    self.decoder_attn_masks = []
    self.id_nums = df.id.copy()

    encoder_txt = df.encoder.copy()
    decoder_txt = df.decoder.copy()

    for i in range(len(encoder_txt)):
      if decoder_only:
        encoder_dict = encoder_tokenizer(encoder_txt[i][0] + encoder_tokenizer.eos_token, truncation=True, max_length=max_length, padding="max_length")
        decoder_dict = decoder_tokenizer(decoder_txt[i][0] + decoder_tokenizer.eos_token, truncation=True, max_length=max_length, padding="max_length")
      else:
        encoder_dict = encoder_tokenizer(encoder_txt[i][0], truncation=True, max_length=max_length, padding="max_length")
        decoder_dict = decoder_tokenizer(decoder_txt[i][0], truncation=True, max_length=max_length, padding="max_length")

      self.input_ids.append(torch.tensor(encoder_dict['input_ids']))
      self.decoder_ids.append(torch.tensor(decoder_dict['input_ids']))

      self.attn_masks.append(torch.tensor(encoder_dict['attention_mask']))
      self.decoder_attn_masks.append(torch.tensor(decoder_dict['attention_mask']))
    
  def __len__(self):
    return len(self.input_ids)

  def __getitem__(self, idx):
    return self.input_ids[idx], self.decoder_ids[idx], self.id_nums[idx], self.attn_masks[idx], self.decoder_attn_masks[idx]