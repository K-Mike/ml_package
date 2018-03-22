import tqdm
import pandas as pd


def convert_tokens_to_ids(tokenized_sentences, words_dict, embedding_word_dict, sentences_length,
                          unknown_word_id, end_word_id):
    """
    Convert tokenized sentences based on word_list dictionary to embedding_word_dict dictionary.
    :param tokenized_sentences: list of sentences [0, 9, 5].
    :param words_list:  index - word dictionary.
    :param embedding_word_dict:  word - index dictionary.
    :param sentences_length: max length of sentence.
    :param unknown_word_id:
    :param end_word_id:
    :return: list of tokenized sentences.
    """
    words_train = []

    for sentence in tokenized_sentences:
        current_words = []
        for word_index in sentence:
            word = words_dict[word_index]
            word_id = embedding_word_dict.get(word, unknown_word_id)
            current_words.append(word_id)

        if len(current_words) >= sentences_length:
            # half_len = int(sentences_length / 2)
            # current_words = current_words[:half_len] + current_words[len(current_words) - half_len:]
            current_words = current_words[:sentences_length]
        else:
            current_words += [end_word_id] * (sentences_length - len(current_words))
        words_train.append(current_words)

    return words_train


# TODO: very slow and get a lot of memory. Make it with numpy array.
# Pretrained embedding
# https://nlp.stanford.edu/projects/glove/
# https://code.google.com/archive/p/word2vec/
def read_embedding_list(file_path):

    embedding_list = []
    with open(file_path) as f:
        for row in tqdm.tqdm(f.read().split("\n")[1:-1]):
            data = row.split(" ")
            vec = {}
            vec[0] = data[0]
            vec.update({i + 1: float(a) for i, a in enumerate(data[1:-1])})
            embedding_list.append(vec)

    df = pd.DataFrame(embedding_list)
    df = df.set_index(0)
    df = df.astype('float32')
    print('embedding shape', df.shape)
    return df