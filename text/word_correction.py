from functools import partial

# From https://www.kaggle.com/cpmpml/spell-checker-using-word2vec
# WORDS: list of (word, id). Sample [('dog', 0), ('cat', 1) ...]
def P(word, WORDS):
    "Probability of `word`."
    # use inverse of rank as proxy
    # returns 0 if the word isn't in the dictionary
    return - WORDS.get(word, 0)


def correction(word, WORDS):
    "Most probable spelling correction for word."
    return max(candidates(word, WORDS), key=partial(P, WORDS=WORDS))

def candidates(word, WORDS):
    "Generate possible spelling corrections for word."
    return (known([word], WORDS) or known(edits1(word), WORDS) or known(edits2(word), WORDS) or [word])


def known(words, WORDS):
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)


def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)


def edits2(word):
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))