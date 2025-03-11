# WillDaru22
# 
# classify.py
#
# Acknowledgements
# Opening every file in directory
# https://stackoverflow.com/questions/18262293/how-to-open-every-file-in-a-folder
# https://stackoverflow.com/questions/25868109/python-read-all-files-in-directory-and-subdirectories
# Excluding subdirectory from walk
# https://stackoverflow.com/questions/19859840/excluding-directories-in-os-walk
# Finding key frequency across multiple files implementation (similar idea to the way I thought of)
# https://stackoverflow.com/questions/17186253/how-to-find-frequency-of-the-keys-in-a-dictionary-across-multiple-text-files
# Help with understanding generators from the previous example
# https://wiki.python.org/moin/Generators
# Help with log math and getting more precise results
# <Dead link unfortunately>


import os
import math


def create_bow(vocab, filepath):  # create and return a bag of words Python dictionary from a single document
    """ Create a single dictionary for the data
        Note: label may be None
    """
    bow = {}
    # TODO: add your code here
    word_count = {}
    f = open(filepath, encoding='utf-8')
    words = word_count_helper(f)  # get count of each word in the file
    for word in words:
        if word not in word_count:
            word_count[word] = {"total": 0}
        word_count[word]["total"] += 1
    f.close()
    # print(word_count)  # debug
    for word in word_count:  # creates our bag of words using the word count from the file compared to the vocab
        if word not in bow:
            if word not in vocab:
                if None not in bow:
                    bow[None] = 0
                bow[None] += 1
                continue
            else:
                bow[word] = 0
        bow[word] += word_count[word]["total"]
    return bow


def load_training_data(vocab, directory):  # create and return training set (bag of words Python dictionary + label)
    # from the files in a training directory
    """ Create the list of dictionaries """
    dataset = []
    # TODO: add your code here
    exclude = {'test'}  # filepath to exclude
    for path, dirs, files in os.walk(directory, topdown=True):  # goes through directories and subdirectories
        dirs[:] = [d for d in dirs if d not in exclude]  # excludes test from the walk
        for file in files:
            bag = {'label': path[-4:], 'bow': create_bow(vocab, os.path.join(path, file))}
            dataset.append(bag)
    return dataset


def create_vocabulary(directory, cutoff):  # create and return a vocabulary as a list of word types with counts >=
    # cutoff in the training directory
    """ Create a vocabulary from the training directory
        return a sorted vocabulary list
    """
    vocab = []
    # TODO: add your code here
    exclude = {'test'}  # filepath to exclude
    word_count = {}  # directory to take all the counts of words
    for path, dirs, files in os.walk(directory, topdown=True):  # builds a directory with all the counts of words
        dirs[:] = [d for d in dirs if d not in exclude]  # excludes from the walk
        for file in files:
            f = open(os.path.join(path, file), encoding='utf-8')
            words = word_count_helper(f)
            for word in words:
                if word not in word_count:
                    word_count[word] = {"total": 0}
                word_count[word]["total"] += 1
                # print(word_count[word]["total"])  # debug
            f.close()
    # print(word_count)
    for word in word_count:  # moves words to the vocab list that occur more than the cutoff
        if word_count[word]['total'] >= cutoff:
            vocab.append(word)
    # print(vocab)  # debug
    vocab = sorted(vocab)  # sorts the list
    return vocab


# helper method to get words from a file, makes a generator
def word_count_helper(file):
    for line in file:
        for word in line.split():  # just in case we have whitespace
            yield word  # honestly a simple return is probably fine here, but working with an adapted code


def prior(training_data, label_list):  # given a training set, estimate and return the prior probability P(label) of
    # each label
    """ return the prior probability of the label in the training set
        => frequency of DOCUMENTS
    """

    smooth = 1  # smoothing factor
    logprob = {}
    # TODO: add your code here
    # num_label = 0  # debug
    num_six = 0  # number with label 2016, hardcoded since we only have 2016 and 2020
    num_twen = 0  # number with label 2020
    for data in training_data:  # calculate number of labels in the training set
        # print(data["label"])  # debug
        if data["label"] in label_list:
            if data["label"] == '2016':  # for seeing with label 2016
                num_six += 1
            if data["label"] == '2020':  # for seeing with label 2020
                num_twen += 1
            # num_label += 1  # debug
    logprob['2020'] = math.log(num_twen + smooth) - math.log(len(training_data) + 2)
    # print(logprob['2020'])  # debug
    logprob['2016'] = math.log(num_six + smooth) - math.log(len(training_data) + 2)
    # print(logprob['2016'])  # debug
    # print(num_six, num_twen, num_label)  # debug
    return logprob


def p_word_given_label(vocab, training_data, label):  # given a training set and a vocabulary, estimate and return
    # the class conditional distribution P(word|label) over all words for the given label using smoothing
    """ return the class conditional probability of label over all words, with smoothing """

    smooth = 1  # smoothing factor
    word_prob = {}
    # TODO: add your code here
    total_words = 0
    word_count_each = {}  # stores counts of words in the given label and vocab
    # P(w|label) = nw + smooth*1/(n + smooth * size(vocab)+1
    for data in training_data:
        # print(data)  # debug
        if data["label"] == label:
            for word in data['bow']:
                if word is None:
                    total_words += data['bow'][None]
                    if None not in word_count_each:
                        word_count_each[None] = 0
                    word_count_each[None] += data['bow'][None]
                else:
                    total_words += data['bow'][word]  # adds number of word to total words
                    if word not in word_count_each:
                        word_count_each[word] = 0
                    word_count_each[word] += data['bow'][word]  # adds to let us easily know the count of words
    for word in vocab:
        if word not in word_count_each:
            word_count_each[word] = 0
    # should have all words and counts of words now
    for word in word_count_each:
        word_prob[word] = math.log(word_count_each[word]+smooth) - math.log(total_words + smooth*(len(vocab)+1))
    # print(word_count_each)  # debug
    return word_prob


##################################################################################
def train(training_directory, cutoff):  # load the training data, estimate the prior distribution P(label) and class
    # conditional distributions P(word|label), return the trained model
    """ return a dictionary formatted as follows:
            {
             'vocabulary': <the training set vocabulary>,
             'log prior': <the output of prior()>,
             'log p(w|y=2016)': <the output of p_word_given_label() for 2016>,
             'log p(w|y=2020)': <the output of p_word_given_label() for 2020>
            }
    """
    retval = {}
    # TODO: add your code here
    vocab = create_vocabulary(training_directory, cutoff)
    training_data = load_training_data(vocab, training_directory)
    retval['vocabulary'] = vocab
    retval['log prior'] = prior(training_data, ['2016', '2020'])
    retval['log p(w|y=2016)'] = p_word_given_label(vocab, training_data, '2016')
    retval['log p(w|y=2020)'] = p_word_given_label(vocab, training_data, '2020')
    return retval


def classify(model, filepath):  # given a trained model, predict the label for the test document (see below for
    # implementation details including the return value)
    """ return a dictionary formatted as follows:
            {
             'predicted y': <'2016' or '2020'>,
             'log p(y=2016|x)': <log probability of 2016 label for the document>,
             'log p(y=2020|x)': <log probability of 2020 label for the document>
            }
    """
    retval = {}
    # TODO: add your code here
    file_words = create_bow(model['vocabulary'], filepath)  # create our bag of words for the given document
    words_six = {}  # to store individual probabilities of words in 2016
    words_twenty = {}  # to store individual probabilities of words in 2020
    for word in file_words:  # calculate word probability in both years
        words_six[word] = file_words[word] * model['log p(w|y=2016)'][word]
        words_twenty[word] = file_words[word] * model['log p(w|y=2020)'][word]
    # print(words_six)  # debug
    # print(words_twenty)  # debug
    sum_six = model['log prior']['2016']  # starts with log(p(label = 2016))
    sum_twenty = model['log prior']['2020']  # starts with log(p(label = 2020))
    for word in words_six:  # gets probability of 2016
        sum_six += words_six[word]
    for word in words_twenty:  # gets probability of 2020
        sum_twenty += words_twenty[word]
    # print(sum_six)  # debug
    # print(sum_twenty)  # debug
    retval['log p(y=2020|x)'] = sum_twenty
    retval['log p(y=2016|x)'] = sum_six
    if sum_twenty > sum_six:  # makes prediction based on the larger probability
        retval['predicted y'] = '2020'
    if sum_six > sum_twenty:
        retval['predicted y'] = '2016'
    return retval
