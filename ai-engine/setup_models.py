import subprocess
import sys

def download_spacy_models():
    print("Downloading spaCy models for Indonesian and English...")
    models = ["en_core_web_sm", "id_core_news_sm"]
    for model in models:
        print(f"Downloading {model}...")
        try:
            subprocess.run([sys.executable, "-m", "spacy", "download", model], check=True)
            print(f"Successfully installed {model}")
        except subprocess.CalledProcessError:
            print(f"Warning: Failed to download {model}. Fallback regex pattern matching will be used.")

if __name__ == "__main__":
    download_spacy_models()
