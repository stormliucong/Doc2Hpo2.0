import re

class NegationDetector:
    def __init__(self, negation_window=10, sentence_delimiters=None):
        """
        Initializes the negation detector with configurable sentence delimiters.
        
        :param negation_window: Maximum number of words to search before and after the term for negation.
        :param sentence_delimiters: A set of characters used to identify sentence boundaries.
        """
        self.negation_keywords = {"not", "no", "none", "never", "without", "nor", "can't", "won't", "isn't", "aren't", "doesn't", "didn't"}
        self.negation_window = negation_window
        self.sentence_delimiters = sentence_delimiters or {'. ', '!', '?', '\n', '\t'}

    def is_negated(self, text, term_span):
        """
        Detects if the given term is negated in a paragraph.
        
        :param text: The paragraph containing the term.
        :param term_span: A tuple (start, end) indicating the start and end indices of the term in the string.
        :return: True if the term is negated, False otherwise.
        """
        start, end = term_span
        if start < 0 or end > len(text) or start >= end:
            raise ValueError("Invalid term_span indices.")

        # Extract the term and determine the sentence boundaries
        term = text[start:end]
        sentence_start, sentence_end = self._get_sentence_boundaries(text, start, end)
        
        # Extract the sentence containing the term
        sentence = text[sentence_start:sentence_end].lower()
        # Tokenize the text before and after the term
        before_text = sentence[:start - sentence_start]
        after_text = sentence[end - sentence_start:]
        before_words = self._tokenize(before_text)
        after_words = self._tokenize(after_text)

        # Limit search to the smaller of negation_window or sentence boundary
        effective_window = self.negation_window

        if self._contains_negation(before_words[-effective_window:], direction="before"):
            return True

        if self._contains_negation(after_words[:effective_window], direction="after"):
            return True

        return False

    def _get_sentence_boundaries(self, text, start, end):
        """
        Determines the boundaries of the sentence containing the term.

        :param text: The paragraph containing the term.
        :param start: The start index of the term.
        :param end: The end index of the term.
        :return: A tuple (sentence_start, sentence_end) indicating the boundaries of the sentence.
        """
        # Build a regular expression for sentence delimiters
        delimiter_regex = r"|".join(re.escape(d) for d in self.sentence_delimiters)
        # Find the nearest preceding sentence delimiter
        sentence_start_match = list(re.finditer(delimiter_regex, text[:start]))
        sentence_start = sentence_start_match[-1].end() if sentence_start_match else 0

        # Find the nearest following sentence delimiter
        sentence_end_match = re.search(delimiter_regex, text[end:])
        sentence_end = end + sentence_end_match.start() + 1 if sentence_end_match else len(text)

        return sentence_start, sentence_end

    def _tokenize(self, text):
        """
        Tokenizes the text into words, removing unnecessary punctuations.

        :param text: The text to tokenize.
        :return: A list of words.
        """
        return re.findall(r'\b\w+\b', text)

    def _contains_negation(self, words, direction):
        """
        Checks if the given list of words contains negation keywords.

        :param words: List of words to check.
        :param direction: Whether to check "before" or "after" the term.
        :return: True if a negation keyword is detected, False otherwise.
        """
        return any(word in self.negation_keywords for word in words)


# Example usage:
if __name__ == "__main__":
    text = ("The patient is not good today. He is showing any signs of improvement! "
            "However, the earlier reports did not suggest any worsening either?")
    term_span = (19, 23)  # Indices for "good"
    detector = NegationDetector(negation_window=10, sentence_delimiters=None)
    is_negated = detector.is_negated(text, term_span)
    print(f"The term 'good' is negated: {is_negated}")

    term_span = (37, 44)  # Indices for "showing"
    detector = NegationDetector(negation_window=10, sentence_delimiters=None)
    is_negated = detector.is_negated(text, term_span)
    print(f"The term 'showing' is negated: {is_negated}")
