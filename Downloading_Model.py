from huggingface_hub import hf_hub_download

# Example for downloading the spiece.model file (SentencePiece)
hf_hub_download(
    repo_id="Helsinki-NLP/opus-mt-mul-en",
    filename="spiece.model",
    cache_dir="./models/opus-mt-mul-en"
)
# You can also download other files such as pytorch_model.bin, config.json, and tokenizer.json.
