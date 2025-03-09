# WillDaru22
#
# Acknowledgements
# help with figuring out covariance math issues
# <Dead link unfortunately>
# Hints about diagonalizing a matrix
# <Dead link unfortunately>
# Reversing a numpy array
# https://www.askpython.com/python/array/reverse-an-array-in-python
# Getting nth element of npy array
# https://stackoverflow.com/questions/44759527/get-nth-element-from-numpy-array
# deleting things from numpy arrays
# https://numpy.org/doc/stable/reference/generated/numpy.delete.html
# Better sorting
# https://stackoverflow.com/questions/8092920/sort-eigenvalues-and-associated-eigenvectors-after-using-numpy-linalg-eig-in-pyt
# convert image to matrix
# https://stackoverflow.com/questions/15612373/convert-image-png-to-matrix-and-then-to-1d-array


from scipy.linalg import eigh
import numpy as np
import matplotlib.pyplot as plt
# import matplotlib
# matplotlib.use('Agg')


# load the dataset from a provided .npy file, re-center it around the origin and return it as a NumPy array of floats
def load_and_center_dataset(filename):
    x = np.load(filename)
    x = np.reshape(x, (2000, 784))
    # print(np.mean(x, axis=0))  # test debug
    return x - np.mean(x, axis=0)  # center around origin


# calculate and return the covariance matrix of the dataset as a NumPy matrix (d x d array)
def get_covariance(dataset):  # need to debug this EDIT: Fixed
    return (1 / (len(dataset) - 1)) * np.dot(np.transpose(dataset), dataset)


# perform eigen decomposition on the covariance matrix S and return a diagonal matrix (NumPy array) with the largest
# m eigenvalues on the diagonal, and a matrix (NumPy array) with the corresponding eigenvectors as columns
def get_eig(S, m):
    # testvals, testvectors = eigh(S)  # debug
    vals, vectors = eigh(S, eigvals=(len(S) - m, len(S) - 1))
    idx = vals.argsort()[::-1]
    vals = vals[idx]
    vectors = vectors[:, idx]
    # vals = sorted(vals, reverse=True)
    # vectors = np.fliplr(vectors)
    vals = np.diag(vals)
    return vals, vectors  # , testvals, testvectors  # debug


# similar to get_eig, but instead of returning the first m, return all eigenvectors that explains more than perc % of
# variance
def get_eig_perc(S, perc):  # frustration.py
    pervals = []
    # pervectors = []
    once = 0
    vals, vectors = eigh(S)
    i = 0
    # print(vectors)  # debug
    vectors = np.transpose(vectors)  # it just works
    for item in vals:  # iterates over both of our arrays
        # print(item)
        if item / np.sum(vals) > perc:  # checks if the eigenvalue is above the perc after variance
            pervals.append(item)
            if once == 0:
                vectors = vectors[i:len(vectors)]  # workaround makes this work somehow
                once += 1
        i += 1
    # pervectors = np.array(pervectors)
    vectors = np.transpose(vectors)  # it just works
    pervals = np.array(pervals)
    idx = pervals.argsort()[::-1]
    pervals = pervals[idx]
    vectors = vectors[:, idx]
    # pervals = sorted(pervals, reverse=True)  # sorts by descending
    # vectors = np.fliplr(vectors)  # flips the list to make it similar
    pervals = np.diag(pervals)  # diagonal matrix make
    return pervals, vectors


# project each image into your m-dimensional space and return the new representation as a d x 1 NumPy array
def project_image(image, U):
    # img_vector = np.reshape(image, (28, 28))  # if we need a 28 x 28 image, pretty sure already 1d vector though
    new_rep = np.dot(image, U)
    projected = np.dot(new_rep, np.transpose(U))
    return projected


# use matplotlib to display a visual representation of the original image and the projected image side-by-side
def display_image(orig, proj):
    orig_img = np.reshape(orig, (28, 28))
    proj_img = np.reshape(proj, (28, 28))
    fig, axs = plt.subplots(figsize=(9, 3), nrows=1, ncols=2)
    axs[0].set_title('Original')
    axs[1].set_title('Projection')
    img1 = axs[0].imshow(orig_img, aspect='equal', cmap='gray')
    fig.colorbar(img1, ax=axs[0])
    img2 = axs[1].imshow(proj_img, aspect='equal', cmap='gray')
    fig.colorbar(img2, ax=axs[1])
    plt.show()
    return
