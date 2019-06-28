# BERT with SentencePiece.
This is a repository of BERT model with SentencePiece tokenizer.  

## Requirements
sentencepiece
tensorflow
pandas

## Preprocess 
Preprocess raw data files to split sentences as follows.

```
python3 src/sentence-split.py --config eu.congif.ini --do_lower_case 
```

### Training SentencePiece model
Train a SentencePiece model using the preprocessed data.

```
python3 src/train-sentencepiece.py --config eu.congif.ini
```

### Creating data for pretraining
Create .tfrecord files for pretraining.
By default, we mask whole words and we set to 512 the sequence length.

```
python3 src/create_pretraining_data.py \
    --input_file=corpus/eu/2014wiki.eu.sent_splited \
    --output_file=corpus/eu/pretraining.tf.data \
    --model_file=./model/eu.model \
    --vocab_file=./model/eu.vocab \
    --do_lower_case=True
```
### Pretraining
You need GPU/TPU environment to pretrain a BERT model.  

python src/run_pretraining.py \
  --config_file eu.congif.ini \
  --input_file=corpus/eu/pretraining.tf.data \
  --output_dir=gureBERT/eu.gureBERT \
  --do_train=True \
  --do_eval=True \
  --train_batch_size=256 \
  --max_seq_length=512 \
  --max_predictions_per_seq=20 \
  --num_train_steps=1000000 \
  --num_warmup_steps=10000 \
  --save_checkpoints_steps=10000 \
  --learning_rate=1e-4 \
