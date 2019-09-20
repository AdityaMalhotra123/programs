import nltk

class Analyzer():
    """Implements sentiment analysis."""

    def __init__(self, positives, negatives):
        """Initialize Analyzer."""
        with open('positive-words.txt', 'r') as lines:
            for line in lines:
                if line.startswith(';') != True:
                    self.positives = [line.strip('\n') for line in lines]

        with open('negative-words.txt', 'r') as lines:
            for line in lines:
                if line.startswith(';') != True:
                    self.negatives = [line.strip('\n') for line in lines]

    def analyze(self, text):
        """Analyze text for sentiment, returning its score."""
        tokenizer = nltk.tokenize.TweetTokenizer()
        tokens = tokenizer.tokenize(text)
        s = 0
        i = 0
        while i < len(tokens):
            if tokens[i].lower() in self.positives:
                s += 1
            elif tokens[i].lower() in self.negatives:
                s-= 1
            i += 1
        return s
