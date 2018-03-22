import os
import scipy
import time
from contextlib import contextmanager
import numpy as np


# TODO: Unify save_sparse_matrix, load_sparse_matrix, save_matrix, load_matrix
def save_sparse_matrix(filename, x):
    x_coo = x.tocoo()
    row = x_coo.row
    col = x_coo.col
    data = x_coo.data
    shape = x_coo.shape
    np.savez(filename, row=row, col=col, data=data, shape=shape)


def load_sparse_matrix(filename):
    y = np.load(filename)
    z = scipy.sparse.coo_matrix((y['data'], (y['row'], y['col'])), shape=y['shape'])
    return z


def save_matrix(X_train, Y_train, X_test, name_list, base_dir='data'):
    fname = '_'.join(['X_train'] + name_list)
    path = os.path.join(base_dir, fname)
    if scipy.sparse.issparse(X_train):
        save_sparse_matrix(path, X_train)
    else:
        np.save(path, X_train)

    fname = '_'.join(['Y_train'] + name_list)
    path = os.path.join(base_dir, fname)
    if scipy.sparse.issparse(X_train):
        Y_train_sp = scipy.sparse.csc_matrix(Y_train)
        save_sparse_matrix(path, Y_train_sp)
    else:
        np.save(path, Y_train)

    fname = '_'.join(['X_test'] + name_list)
    path = os.path.join(base_dir, fname)
    if scipy.sparse.issparse(X_train):
        save_sparse_matrix(path, X_test)
    else:
        np.save(path, X_test)


def load_matrix(name_list, base_dir='data'):
    fname = '_'.join(['X_train'] + name_list)
    path = os.path.join(base_dir, fname) + '.npz'
    if os.path.isfile(path):
        X_train = load_sparse_matrix(path)
    else:
        X_train = np.load(path[:-4] + '.npy')

    fname = '_'.join(['Y_train'] + name_list)
    path = os.path.join(base_dir, fname) + '.npz'
    if os.path.isfile(path):
        Y_train_sp = load_sparse_matrix(path)
    else:
        Y_train_sp = np.load(path[:-4] + '.npy')


    fname = '_'.join(['X_test'] + name_list)
    path = os.path.join(base_dir, fname) + '.npz'
    if os.path.isfile(path):
        X_test = load_sparse_matrix(path)
    else:
        X_test = np.load(path[:-4] + '.npy')

    return X_train, Y_train_sp, X_test


@contextmanager
def timer(name):
    """
    Taken from Konstantin Lopuhin https://www.kaggle.com/lopuhin
    in script named : Mercari Golf: 0.3875 CV in 75 LOC, 1900 s
    https://www.kaggle.com/lopuhin/mercari-golf-0-3875-cv-in-75-loc-1900-s
    """
    t0 = time.time()
    yield
    print(f'[{name}] done in {time.time() - t0:.0f} s')