import os
from moviepy.editor import VideoFileClip, concatenate_videoclips
ALPHABET_FOLDER = "alphabets"
DIGIT_FOLDER = "digits"
GAP_VIDEO = "gap.mp4"
TARGET_WIDTH = 1920
TARGET_HEIGHT = 1080
def resize_clip(clip):
    clip = clip.resize(height=TARGET_HEIGHT)
    clip = clip.on_color(
        size=(TARGET_WIDTH, TARGET_HEIGHT),
        color=(0, 0, 0),
        pos=("center", "center")
    )
    return clip
def get_letter_video(letter):
    path = os.path.join(ALPHABET_FOLDER, f"{letter.upper()}.mov")
    return path if os.path.exists(path) else None
# Get Digit Video
def get_digit_video(digit):
    path = os.path.join(DIGIT_FOLDER, f"{digit}.mp4")
    return path if os.path.exists(path) else None
# Create Final Sentence Video
def create_sentence_video(tokens):
    clips = []
    # Load gap once (for performance)
    GAP_CLIP = None
    if os.path.exists(GAP_VIDEO):
        GAP_CLIP = resize_clip(VideoFileClip(GAP_VIDEO))
    for token in tokens:
        # SPACE → Use gap.mp4
        if token == "__space__":
            if GAP_CLIP:
                clips.append(GAP_CLIP)
            continue
        if token == "__pause__":
            if GAP_CLIP:
                pause_clip = GAP_CLIP.subclip(0, min(1.0, GAP_CLIP.duration))
                clips.append(pause_clip)
            continue
        if token == "__question__":
            # Add question expression video here if you have one
            continue
        # DIGITS
        if token.isdigit():
            digit_path = get_digit_video(token)
            if digit_path:
                clip = resize_clip(VideoFileClip(digit_path))
                clips.append(clip)
            continue
        # LETTERS
        letter_path = get_letter_video(token)
        if letter_path:
            clip = resize_clip(VideoFileClip(letter_path))
            clips.append(clip)
    # Final Output
    if clips:
        final = concatenate_videoclips(clips, method="chain")
        # Reduce resolution for faster export
        final = final.resize(height=720)
        final.write_videofile(
            "final_output.mp4",
            codec="libx264",
            preset="ultrafast",
            audio=False,
            threads=4
        )
        print("Video Created Successfully!")
    else:
        print("No matching videos found.")