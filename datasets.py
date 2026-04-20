import requests
import os
import zipfile
import shutil
import tarfile
# Download ISLTranslate CSV
print("Downloading ISLTranslate.csv ...")
csv_url = "https://raw.githubusercontent.com/Exploration-Lab/ISLTranslate/main/data/ISLTranslate.csv"
r = requests.get(csv_url)
with open("ISLTranslate.csv", "wb") as f:
    f.write(r.content)
print("ISLTranslate.csv downloaded ✔️")
# Create folder for sign dictionary videos
SIGN_FOLDER = "sign_dictionary_videos"
if not os.path.exists(SIGN_FOLDER):
    os.makedirs(SIGN_FOLDER)
print("Downloading sample sign dictionary videos...")
# Download smaller sample tar file from Hugging Face sign-dictionary-isl
urls = [
    "https://huggingface.co/datasets/bridgeconn/sign-dictionary-isl/resolve/main/shard_00001-train.tar",
    "https://huggingface.co/datasets/bridgeconn/sign-dictionary-isl/resolve/main/shard_00002-train.tar"
]
for url in urls:
    filename = url.split("/")[-1]
    print(f"Downloading {filename} ...")
    r = requests.get(url, stream=True)
    with open(filename, "wb") as f:
        shutil.copyfileobj(r.raw, f)
    print(f"{filename} downloaded ✔️")
    # Extract tar
    print(f"Extracting {filename} ...")
    with tarfile.open(filename) as tar:
        tar.extractall(path=SIGN_FOLDER)
    print(f"{filename} extracted ✔️")
    # Remove tar file to save space
    os.remove(filename)
print("All sample sign dictionary videos ready ")
print("\nDownload and extraction complete")
