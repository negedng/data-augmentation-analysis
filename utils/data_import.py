import copy
import numpy as np
from sklearn.utils import check_random_state

random_state = check_random_state(0)

def lists_from_dict(data_dictionary, shuffle=True):
    """Generates same length X,y 
    from a dictionary where data_dict[y[key]] is 
    the X array of the 'key' labelled data
    Parameters
    ----------
    data_dictionary : dictionary
        A dictionary: Keys - labels, values - data
    shuffle : boolean, optional
        Shuffle the return data. Default value: true.
    Returns
    -------
    array_like
        The data in an array
    array_like
        The labels (keys in the dictionary)"""
    X = []
    y = []
    for key in data_dictionary.keys():
        for sample in data_dictionary[key]:
            X.append(sample)
            y.append(key)
    X = np.array(X)
    y = np.array(y)
    if(shuffle):
        perm = random_state.permutation(len(y))
        return X[perm], y[perm]
    return X, y

def reduce_class_samples(data, label_key=None,
                        proportion=0.2, shuffle=True):
    """Reduce the samples in a label to the given value of it
    Parameters
    ----------
    data : dictionary
        The data dictionary, each element is array-like
    label_key : key
        The key of the class to be reduced in the array
        Default: None (choose the first in the key list)
    proportion: double
        The 0..1 value of the remaining size of the array
        Default: 0.2
    shuffle : boolean
        Shuffle the dictionary before split.
        Default: True
    Returns
    -------
    data
        The reduced dictionary
    label_key
        The key to the reduced type"""
    data_new = copy.deepcopy(data)
    if(label_key==None):
        label_key = data_new.keys()[0]
    label_size = len(data_new[label_key])
    data_port = (int) (label_size*proportion)
    data_temp = copy.deepcopy(data_new[label_key])
    if(shuffle):
        perm = random_state.permutation(len(data_temp))
        data_temp = np.array(data_temp)[perm]
    data_new[label_key] = copy.deepcopy(data_temp[:data_port])
    return data_new, label_key

def generate_balanced_dictionary(X,y,
                                 label_number=None):
    """Returns with a dictionary with same sample size
    Parameters
    ----------
    X : array_like
        The training data.
    y : array_like
        the labels
    label_number : int
        The number of labels to be kept.
    Returns
    -------
    data_dict
        Dictionary of arrays: key - label,
        value - data"""
    data_dict = {}
    unique, counts = np.unique(y, return_counts=True)
    if(label_number==None):
        label_number = len(unique)
    y_sort = [y_sort for _,y_sort in sorted(zip(counts,unique))]
    y_keep = y_sort[-label_number:]
    size = counts[unique.tolist().index(y_keep[0])]
    
    for i in range(len(X)):
        if y[i] in y_keep:
            if data_dict.has_key(y[i]):
                if(len(data_dict[y[i]])<size):
                    data_dict[y[i]].append(X[i])
            else:
                data_dict[y[i]] = [X[i]]
    return data_dict

def train_test_split_dictionary(data, test_rate=0.2):
    """Split the data into train and test dictionaries
    Parameters
    ----------
    data : dictionary
        The data dictionary
    test_rate : float
        The proportion of the test data"""
    data_train = {}
    data_test = {}
    for key in data.keys():
        sample_len = len(data[key])
        split = (int) (sample_len * test_rate)
        data_train[key]=data[key][split:]
        data_test[key]=data[key][:split]
    return data_train, data_test

