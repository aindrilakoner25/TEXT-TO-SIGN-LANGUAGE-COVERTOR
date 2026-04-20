import os
import json
WORD_FOLDER = "words"
def load_word_mapping():
    word_map = {}
    for file in os.listdir(WORD_FOLDER):
        if file.endswith(".json"):
            json_path = os.path.join(WORD_FOLDER, file)
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Get word from transcript.text
                word_text = data.get("transcript", {}).get("text", "").lower()
                video_id = file.replace(".json", "")
                if word_text:
                    word_map[word_text] = video_id
    return word_map
