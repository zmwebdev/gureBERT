for DIR in $( find data/wiki/ -mindepth 1 -type d ); do 
  python3 src/create_pretraining_data.py \
    --input_file=${DIR}/all.txt \
    --output_file=${DIR}/all-maxseq128.tfrecord \
    --model_file=./model/wiki-eu.model \
    --vocab_file=./model/wiki-eu.vocab \
    --do_lower_case=True \
    --max_seq_length=128 \
    --max_predictions_per_seq=20 \
    --masked_lm_prob=0.15 \
    --random_seed=12345 \
    --dupe_factor=5
done