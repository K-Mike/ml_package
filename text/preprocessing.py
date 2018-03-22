import string
import re

# Contraction replacement patterns
cont_patterns = [
    (b'\$', b's'),
    (b'\@', b'a'),
    (b'0', b'o'),
    (b'f\*ck', b'fuck'),
    (b'f\*\*k', b'fuck'),
    (b'su\*\*s', b'sucks'),

    (b'(W|w)on\'t', b'will not'),
    (b'(C|c)an\'t', b'can not'),
    (b'(I|i)\'m', b'i am'),
    #     (r'\b[uU]\b', 'you'),
    (b'(A|a)in\'t', b'is not'),
    (b'(\w+)\'ll', b'\g<1> will'),
    (b'(\w+)n\'t', b'\g<1> not'),
    (b'(\w+)\'ve', b'\g<1> have'),
    (b'(\w+)\'s', b'\g<1> is'),
    (b'(\w+)\'re', b'\g<1> are'),
    (b'(\w+)\'d', b'\g<1> would'),

    # (b'&lt;3', b' heart '),
    # (b':d', b' smile '),
    # (b':dd', b' smile '),
    # (b':p', b' smile '),
    # (b'8\)', b' smile '),
    # (b':-\)', b' smile '),
    # (b':\)', b' smile '),
    # (b';\)', b' smile '),
    # (b'\(-:', b' smile '),
    # (b'\(:', b' smile '),
    # (b'yay!', b' good '),
    # (b'yay', b' good '),
    # (b'yaay', b' good '),
    # (b':/', b' worry '),
    # (b':&gt;', b' angry '),
    # (b":'\)", b' sad '),
    # (b':-\(', b' sad '),
    # (b':\(', b' sad '),
    # (b':s', b' sad '),
    # (b':-s', b' sad '),
    (b'\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}', b' '),
    #     (b'(\[[\s\S]*\])', b' '),
    (b'[\s]*?(www.[\S]*)', b' '),

    (b'\-', b' '),
    (b'\_', b' '),
    (b'\'', b' '),
    (b'\(', b' '),
    (b'\)', b' '),
    (b'!', b' exclamation '),
    (b'\?', b' question '),
    (b'\.', b' period ')
]
patterns = [(re.compile(regex), repl) for (regex, repl) in cont_patterns]


def clean_text(text):
    """ Simple text clean up process"""
    # 0. confusable_homoglyphs
    # text = align_text(text)
    # 1. Go to lower case (only good for english)
    # Go to bytes_strings as I had issues removing all \n in r""
    clean = bytes(text.lower(), encoding="utf-8")

    # replace words like hhhhhhhhhhhhhhi with hi
    for ch in string.ascii_lowercase:
        pattern = bytes(ch + '{3,}', encoding="utf-8")
        clean = re.sub(pattern, bytes(ch, encoding="utf-8"), clean)
    # 2. Drop \n and  \t
    clean = clean.replace(b"\n", b" ")
    clean = clean.replace(b"\t", b" ")
    clean = clean.replace(b"\b", b" ")
    clean = clean.replace(b"\r", b" ")
    # 3. Replace english contractions
    for (pattern, repl) in patterns:
        clean = re.sub(pattern, repl, clean)
    # 0. confusable_homoglyphs
    clean = str(clean, 'utf-8')
    clean = align_text(clean)
    clean = bytes(clean.lower(), encoding="utf-8")
        # 4. Drop puntuation
        # I could have used regex package with regex.sub(b"\p{P}", " ")
    #     exclude = re.compile(b'[%s]' % re.escape(bytes(string.punctuation, encoding='utf-8')))
    #     clean = b" ".join([exclude.sub(b'', token) for token in clean.split()])
    # 5. Drop numbers - as a scientist I don't think numbers are toxic ;-)
    clean = re.sub(b"\d+", b" ", clean)
    # 6. Remove extra spaces - At the end of previous operations we multiplied space accurences
    clean = re.sub(b'\s+', b' ', clean)
    # Remove ending space if any
    clean = re.sub(b'\s+$', b'', clean)
    # 7. Now replace words by words surrounded by # signs
    # e.g. my name is bond would become #my# #name# #is# #bond#
    # clean = re.sub(b"([a-z]+)", b"#\g<1>#", clean)
    # clean = re.sub(b" ", b"# #", clean)  # Replace space
    # clean = b"#" + clean + b"#"  # add leading and trailing #
    # 8. Word replace
    #     clean = re.sub(b'sock-puppetry', b'sock puppetry', clean)
    #     clean = re.sub(b'sock-puppetry', b'sock puppetry', clean)

    # 9. string manipulation
    clean = str(clean, 'utf-8')
    #     clean = re.sub(r'\b[uU]\b', 'you', clean)

    return clean


def align_text(text):
    true_chars = '!?,.\'23589&%' + string.ascii_letters
    my_rules = {'χ': 'x'}
    #     print(text)
    confuses = confusables.is_confusable(text, preferred_aliases=['latin'], greedy=True)
    #     confuses = confusables.is_confusable(text, preferred_aliases=['COMMON'], greedy=True)
    #     print(confuses)
    if not confuses:
        return text

    # print('inlude')
    for con in confuses:
        ch = con['character']
        if ch in true_chars:
            continue
        if ch in my_rules:
            lat_ch = my_rules[ch]
        else:
            lat_ch = con['homoglyphs'][0]['c']
        # print(ch, con['homoglyphs'])
        text = text.replace(ch, lat_ch)

    return text