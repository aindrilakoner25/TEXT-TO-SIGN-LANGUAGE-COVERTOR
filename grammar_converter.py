def apply_isl_grammar(words):
    """
    Basic ISL grammar transformation
    """
    helping_verbs = ["is", "am", "are", "was", "were", "be"]
    # Remove helping verbs
    filtered_words = [word for word in words if word.lower() not in helping_verbs]
    # Simple SVO → SOV conversion
    # If sentence length >= 3, move second word to end
    if len(filtered_words) >= 3:
        subject = filtered_words[0]
        verb = filtered_words[1]
        remaining = filtered_words[2:]
        # Move verb to end
        new_sentence = [subject] + remaining + [verb]
        return new_sentence
    return filtered_words


