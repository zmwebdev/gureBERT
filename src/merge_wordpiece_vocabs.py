# merge two vocab.txt
# python src/merge_wordpiece_vocabs.py

vocab_en = []
with open("wpModels/vocab.en.txt", "r") as f:
    for token in f:
        vocab_en.append(token.rstrip())

#print(vocab_en)

vocab_eu = []    
with open("wpModels/vocab.eu-mini.txt", "r") as f:
    for token in f:
        vocab_eu.append(token.rstrip())

with open("wpModels/vocab.en-eu.txt", "w") as f:
  diff_tokens = set(vocab_eu)-set(vocab_en)
  vocab_en += diff_tokens
  for token in vocab_en:
    f.write(token+"\n")
