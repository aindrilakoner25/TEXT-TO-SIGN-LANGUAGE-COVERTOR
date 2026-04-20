import re
# Process one sentence
def process_text(text):
    is_question = "?" in text
    # Cleaning
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    words = text.split()
    if not words:
        return []
    # Tense Handling
    irregular_past = {
        "went": "go",
        "ate": "eat",
        "came": "come",
        "saw": "see",
        "did": "do",
        "had": "have",
        "made": "make",
        "took": "take",
        "gave": "give",
        "got": "get",
        "wrote": "write",
        "ran": "run",
        "thought": "think"
    }
    new_words = []
    continuous_detected = False
    for w in words:
        if w in irregular_past:
            new_words.append(irregular_past[w])
            continue
        if w.endswith("ed") and len(w) > 3:
            new_words.append(w[:-2])
            continue
        if w.endswith("ing") and len(w) > 4:
            continuous_detected = True
            new_words.append(w[:-3])
            continue
        new_words.append(w)
    words = new_words
    # Remove Helping Words
    helping_verbs = ["is", "am", "are", "was", "were", "be", "do", "does", "did", "will", "shall"]
    words = [w for w in words if w not in helping_verbs]
    remove_words = ["at", "to", "the", "a", "an", "in", "on", "of"]
    words = [w for w in words if w not in remove_words]
    if len(words) < 1:
        return words
    # Number Handling
    processed_words = []
    i = 0
    while i < len(words):
        word = words[i]
        if word.isdigit():
            for digit in word:
                processed_words.append(digit)
            if i + 1 < len(words):
                next_word = words[i + 1]
                special_plural = {
                    "years": "year",
                    "feet": "foot"
                }
                if next_word in special_plural:
                    processed_words.append(special_plural[next_word])
                    i += 2
                    continue
                if next_word.endswith("s") and len(next_word) > 3:
                    processed_words.append(next_word[:-1])
                    i += 2
                    continue
        processed_words.append(word)
        i += 1
    words = processed_words
    # Time Words
    time_words = ["yesterday", "today", "tomorrow", "now", "later"]
    found_time = None
    for w in words:
        if w in time_words:
            found_time = w
            break
    if found_time:
        words.remove(found_time)
    # Question Words
    question_words = ["what", "where", "when", "why", "how", "who"]
    found_qword = None
    for w in words:
        if w in question_words:
            found_qword = w
            break
    if found_qword:
        words.remove(found_qword)
    # Negative Words
    negative_words = ["not", "no", "never"]
    found_negative = None
    for w in words:
        if w in negative_words:
            found_negative = w
            break
    if found_negative:
        words.remove(found_negative)
    # SVO → SOV
    if len(words) >= 3:
        subject = words[0]
        verb = words[1]
        objects = words[2:]
        words = [subject] + objects + [verb]
    # Build Final Words
    final_words = []
    if found_time:
        final_words.append(found_time)
    final_words.extend(words)
    if continuous_detected and "now" not in final_words:
        final_words.append("now")
    if found_qword:
        final_words.append(found_qword)
    if found_negative:
        final_words.append(found_negative)
    if is_question:
        final_words.append("__question__")
    # CONVERT WORDS → LETTERS (NO WORD SEARCH)
    final_letters = []
    for word in final_words:
        if word in ["__question__"]:
            final_letters.append(word)
            continue
        for letter in word:
            final_letters.append(letter)
        final_letters.append("__space__")
    if final_letters and final_letters[-1] == "__space__":
        final_letters.pop()
    return final_letters
# Process MULTIPLE sentences
def process_paragraph(text):
    sentences = re.split(r'[.!?]+', text)
    all_letters = []
    for sentence in sentences:
        sentence = sentence.strip()
        if sentence:
            letters = process_text(sentence)
            all_letters.extend(letters)
            all_letters.append("__pause__")
    if all_letters and all_letters[-1] == "__pause__":
        all_letters.pop()
    return all_letters