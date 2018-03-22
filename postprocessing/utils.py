import numpy as np
from scipy.stats import rankdata


def rank_correction(X, method='dense'):
    """
    Rank data in each column.
    :param X: numpy array
    :param method : str, optional
        The method used to assign ranks to tied elements.
        The options are 'average', 'min', 'max', 'dense' and 'ordinal'.

        'average':
            The average of the ranks that would have been assigned to
            all the tied values is assigned to each value.
        'min':
            The minimum of the ranks that would have been assigned to all
            the tied values is assigned to each value.  (This is also
            referred to as "competition" ranking.)
        'max':
            The maximum of the ranks that would have been assigned to all
            the tied values is assigned to each value.
        'dense':
            Like 'min', but the rank of the next highest element is assigned
            the rank immediately after those assigned to the tied elements.
        'ordinal':
            All values are given a distinct rank, corresponding to the order
            that the values occur in `a`.

        The default is 'dense'.
    :return: Ranked array.
    """
    X_rank = np.zeros_like(X)

    for i in range(X.shape[1]):
        rank_col = rankdata(X[:, i], method=method)
        rank_col = rank_col / rank_col.max()
        X_rank[:, i] = rank_col

    return X_rank