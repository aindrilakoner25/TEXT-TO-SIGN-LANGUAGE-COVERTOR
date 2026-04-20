from nlp_processor import process_paragraph
from video_merger import create_sentence_video
def main():
    text = input("Enter a sentence or sentences: ")
    # Now returns letters, not words
    letters = process_paragraph(text)
    print("Processed letters:", letters)
    create_sentence_video(letters)
if __name__ == "__main__":
    main()