from huggingface_hub import hf_hub_download
import os

def download_model_files(repo_id: str, filename: str, cache_dir: str) -> str:
    """Downloads a file from the Hugging Face Hub.

    Args:
        repo_id: The repository ID.
        filename: The name of the file to download.
        cache_dir: The directory to store the downloaded file.

    Returns:
        The local path to the downloaded file.
    """
    path = hf_hub_download(
        repo_id=repo_id,
        filename=filename,
        cache_dir=cache_dir
    )
    return str(path)

if __name__ == "__main__":
    # Example usage for Helsinki-NLP model
    download_model_files(
        repo_id="Helsinki-NLP/opus-mt-mul-en",
        filename="spiece.model",
        cache_dir="./models/opus-mt-mul-en"
    )
