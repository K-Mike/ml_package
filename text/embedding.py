import tqdm
import pandas as pd
import numpy as np


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

# Todo: sample of making embeding, re do it.
def create_datasets(embedding_path, maxlen=500):
    train = pd.read_csv('input/train.csv')
    test = pd.read_csv('input/test.csv')

    print('read_embedding_list')
    path_out = 'glove/crawl-300d-2M.csv'
    word_embeding = pd.read_csv(path_out, index_col=0)
    # word_embeding = read_embedding_list(embedding_path)
    # word_embeding = pd.read_table(embedding_path, sep=" ", index_col=0, header=None, quoting=csv.QUOTE_NONE)
    embedding_size = word_embeding.shape[1]

    # text cleaning
    train['comment_text'] = train['comment_text'].apply(clean_text)
    test['comment_text'] = test['comment_text'].apply(clean_text)

    # Tokenizing
    list_sentences_train = train["comment_text"].fillna(NAN_WORD).values
    list_sentences_test = test["comment_text"].fillna(NAN_WORD).values

    print("Tokenizing sentences in train set...")
    tokenized_sentences_train, words_dict = tokenize_sentences(list_sentences_train, {})

    print("Tokenizing sentences in test set...")
    tokenized_sentences_test, words_dict = tokenize_sentences(list_sentences_test, words_dict)

    print("clear embedding list...")
    embedding_matrix, embedding_word_dict = clear_embedding_list(word_embeding, words_dict, sp_bad_words)

    embedding_word_dict[UNKNOWN_WORD] = len(embedding_word_dict)
    embedding_matrix = np.vstack([embedding_matrix, [0.] * embedding_size])
    embedding_word_dict[END_WORD] = len(embedding_word_dict)
    embedding_matrix = np.vstack([embedding_matrix, [-1.] * embedding_size])

    id_to_word = dict((id, word) for word, id in words_dict.items())
    print("convert train...")
    train_list_of_token_ids = convert_tokens_to_ids(
        tokenized_sentences_train,
        id_to_word,
        embedding_word_dict,
        maxlen)
    print("convert test...")
    test_list_of_token_ids = convert_tokens_to_ids(
        tokenized_sentences_test,
        id_to_word,
        embedding_word_dict,
        maxlen)
    print("Create datasets...")
    x_train = np.array(train_list_of_token_ids)
    y_train = train[label_cols].values
    x_test = np.array(test_list_of_token_ids)

    return x_train, y_train, x_test, embedding_matrix, embedding_word_dict