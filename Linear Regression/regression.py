# 
# WillDaru22
#
# How to read csv without first column
# https://stackoverflow.com/questions/19143667/how-to-read-a-csv-without-the-first-column
# Generating numpy array from csv file
# https://numpy.org/doc/stable/reference/generated/numpy.genfromtxt.html
# Numpy printing columns
# https://numpy.org/doc/stable/reference/generated/numpy.genfromtxt.html
# Numpy rounding numbers to certain decimal positions
# https://numpy.org/doc/stable/reference/generated/numpy.around.html#numpy.around
# Adding column to array in python
# https://www.kite.com/python/answers/how-to-add-a-column-to-a-numpy-array-in-python
# Reshaping python arrays ie changing n x 0 array into n x 1
# https://numpy.org/devdocs/reference/generated/numpy.reshape.html

import numpy as np
import random

# Feel free to import other packages, if needed.


def get_dataset(filename):
    """

    INPUT: 
        filename - a string representing the path to the csv file.

    RETURNS:
        An n by m+1 array, where n is # data points and m is # features.
        The labels y should be in the first column.
    """

    with open(filename, newline='') as csvfile:
        ncols = len(csvfile.readline().split(','))  # calculate number of columns in the csv file
    dataset = np.genfromtxt('bodyfat.csv', delimiter=',', skip_header=1, usecols=range(1, ncols))  # reads in our
    # dataset and converts it to our array.  Actually keeps the data as float64 which is super nice
    return dataset


def print_stats(dataset, col):
    """

    INPUT: 
        dataset - the body fat n by m+1 array
        col     - the index of feature to summarize on. 
                  For example, 1 refers to density.

    RETURNS:
        None
    """
    print(len(dataset[:, col]))  # print length of column
    print(np.round(np.mean(dataset[:, col]), 2))  # print mean of column
    print(np.round(np.std(dataset[:, col]), 2))  # print standard deviation of column


def regression(dataset, cols, betas):
    """

    INPUT: 
        dataset - the body fat n by m+1 array
        cols    - a list of feature indices to learn.
                  For example, [1,8] refers to density and abdomen.
        betas   - a list of elements chosen from [beta0, beta1, ..., betam]

    RETURNS:
        mse of the regression model
    """
    meant = 0  # variable to help us store each row of the sum
    mse = 0  # overall mse
    for row in dataset:  # for each row in the dataset
        meant += betas[0]  # add the beta 0
        for num, col in enumerate(cols):  # go through the columns specified
            meant += betas[num+1]*row[col]  # add the beta(i) and the column of the row
        meant -= row[0]  # subtract first element of each row at the end
        meant = pow(meant, 2)  # square the sum of the row
        mse += meant  # add to overall sum
        meant = 0  # reset for next row
    mse = mse/(len(dataset[:, 0]))  # divide by number of rows we iterated over
    return mse


def gradient_descent(dataset, cols, betas):
    """

    INPUT: 
        dataset - the body fat n by m+1 array
        cols    - a list of feature indices to learn.
                  For example, [1,8] refers to density and abdomen.
        betas   - a list of elements chosen from [beta0, beta1, ..., betam]

    RETURNS:
        An 1D array of gradients
    """
    grads = []  # initial list to store gradients before we convert it to numpy array
    rows_sum = 0  # variable to help us store the sum of the rows for each beta
    meant = 0  # variable to help us store each row of the sum
    for row in dataset:  # for each row in the dataset
        meant += betas[0]  # add the beta 0
        for num, col in enumerate(cols):  # go through the columns specified
            meant += betas[num+1]*row[col]  # add the beta(i) and the column of the row
        meant -= row[0]  # subtract first element of each row at the end
        rows_sum += meant
        meant = 0
    grads.append((rows_sum*2)/len(dataset[:, 0]))  # add to the array
    rows_sum = 0  # reset to handle the non beta 0 cases
    for column in cols:  # handling the other betas
        for row in dataset:  # for each row in the dataset
            meant += betas[0]  # add the beta 0
            for num, col in enumerate(cols):  # go through the columns specified
                meant += betas[num + 1] * row[col]  # add the beta(i) and the column of the row
            meant -= row[0]  # subtract first element of each row at the end
            meant = meant * row[column]
            rows_sum += meant
            meant = 0
        grads.append((rows_sum*2)/len(dataset[:, 0]))  # add to the array
        rows_sum = 0  # reset for next beta
    grads = np.array(grads)  # convert to numpy array
    return grads


def iterate_gradient(dataset, cols, betas, T, eta):
    """

    INPUT: 
        dataset - the body fat n by m+1 array
        cols    - a list of feature indices to learn.
                  For example, [1,8] refers to density and abdomen.
        betas   - a list of elements chosen from [beta0, beta1, ..., betam]
        T       - # iterations to run
        eta     - learning rate

    RETURNS:
        None
    """
    new_betas = betas
    for t in range(1, T+1):  # not doing 0 indexed iterations here so going from 1 to T+1
        gradient = gradient_descent(dataset, cols, new_betas)  # get gradients each time from the old betas
        new_betas = [x - eta*gradient[y] for y, x in enumerate(new_betas)]  # calculate new betas
        print(t, end='')  # prints each iteration number
        print("", '{:.2f}'.format(np.round(regression(dataset, cols, new_betas), 2)), end='')  # prints the mse
        for i, beta in enumerate(new_betas):
            print("", '{:.2f}'.format(np.round(beta, 2)), end='')  # prints each of the betas in proper format
        print()  # just prints a newline for us here


def compute_betas(dataset, cols):
    """

    INPUT: 
        dataset - the body fat n by m+1 array
        cols    - a list of feature indices to learn.
                  For example, [1,8] refers to density and abdomen.

    RETURNS:
        A tuple containing corresponding mse and several learned betas
    """
    X = np.ones((len(dataset[:, 0]), 1))
    for i, col in enumerate(cols):
        X = np.append(X, np.reshape(dataset[:, col], (len(dataset[:, col]), 1)), axis=1)
    betas = np.dot(np.dot(np.linalg.inv(np.dot(np.transpose(X), X)), np.transpose(X)), dataset[:, 0])
    mse = regression(dataset, cols, betas)
    return (mse, *betas)


def predict(dataset, cols, features):
    """

    INPUT: 
        dataset - the body fat n by m+1 array
        cols    - a list of feature indices to learn.
                  For example, [1,8] refers to density and abdomen.
        features- a list of observed values

    RETURNS:
        The predicted body fat percentage value
    """
    betas = compute_betas(dataset, cols)  # compute our betas and MSE.  MSE is going to be betas[0]
    result = betas[1]  # add beta 0 to result
    for i, feat in enumerate(features):  # add each beta and feature multiplied to the result of our prediction
        result += betas[i+2]*feat  # beta 1 is in betas[2] so use i+2
    return result


def random_index_generator(min_val, max_val, seed=42):
    """
    DO NOT MODIFY THIS FUNCTION.
    DO NOT CHANGE THE SEED.
    This generator picks a random value between min_val and max_val,
    seeded by 42.
    """
    random.seed(seed)
    while True:
        yield random.randrange(min_val, max_val)


def sgd(dataset, cols, betas, T, eta):
    """
    TODO: implement this function.
    You must use random_index_generator() to select individual data points.

    INPUT: 
        dataset - the body fat n by m+1 array
        cols    - a list of feature indices to learn.
                  For example, [1,8] refers to density and abdomen.
        betas   - a list of elements chosen from [beta0, beta1, ..., betam]
        T       - # iterations to run
        eta     - learning rate

    RETURNS:
        None
    """
    random_gen = random_index_generator(0, len(dataset), seed=42)
    new_betas = betas
    for t in range(1, T+1):  # not doing 0 indexed iterations here so going from 1 to T+1
        # random row for gradient.  reshaped our random row into the proper shape for our gradient function
        gradient = gradient_descent(np.reshape(dataset[next(random_gen)], (1, len(dataset[0]))), cols, new_betas)
        new_betas = [x - eta*gradient[y] for y, x in enumerate(new_betas)]  # calculate new betas
        print(t, end='')  # prints each iteration number
        print("", '{:.2f}'.format(np.round(regression(dataset, cols, new_betas), 2)), end='')  # prints the mse
        for i, beta in enumerate(new_betas):
            print("", '{:.2f}'.format(np.round(beta, 2)), end='')  # prints each of the betas in proper format
        print()  # just prints a newline for us here


if __name__ == '__main__':
    # Your debugging code goes here.
    pass