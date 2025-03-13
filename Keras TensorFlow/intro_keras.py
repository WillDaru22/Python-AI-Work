# WillDaru22
#
# Acknowledgements
# So many documents and specifics from this site
# https://keras.io/

import tensorflow as tf
from tensorflow import keras

# dimension1 = 0
# dimension2 = 0


# Input: an optional boolean argument (default value is True for training dataset)
# Return: two NumPy arrays for the train_images and train_labels
def get_dataset(training=True):
    mnist = keras.datasets.mnist
    (train_images, train_labels), (test_images, test_labels) = mnist.load_data()
    if training is False:
        return test_images, test_labels
    else:
        return train_images, train_labels


# This function will print several statistics about the data
# Input: the dataset and labels produced by the previous function; does not return anything
def print_stats(train_images, train_labels):
    class_names = ['Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine']
    print(len(train_images))
    print(str(len(train_images[0])) + "x" + str(len(train_images[0][0])))
    # global dimension1  # attempts to update the global variable
    # dimension1 = len(train_images[0])
    # global dimension2  # attempts to update the global variable
    # dimension2 = len(train_images[0][0])
    num_label = 0
    for i, label in enumerate(class_names):
        for lab in train_labels:  # get number of occurrences of image with the label
            if lab == i:
                num_label += 1
        print(str(i) + ".", label, "-", num_label)
        num_label = 0
    # print(len(train_labels))  # debug
    return


# takes no arguments and returns an untrained neural network model
def build_model():
    model = keras.Sequential(
        [
            keras.layers.Flatten(input_shape=(28, 28)),  # had to hard code this due to a bug in which the globals
            # dimension 1 and dimension 2 were not being updated under certain circumstances.  Replace with dimension
            # 1 and dimension 2 if needed
            keras.layers.Dense(128, activation="relu"),
            keras.layers.Dense(64, activation="relu"),
            keras.layers.Dense(10),
        ]
    )
    # model.add(keras.layers.Flatten(input_shape=(dimension1, dimension2)))
    # model.add(keras.layers.Dense(128, activation=keras.activations.relu))
    # model.add(keras.layers.Dense(64, activation=keras.activations.relu))
    # model.add(keras.layers.Dense(10))
    opt = keras.optimizers.SGD(learning_rate=0.001)
    loss_fn = keras.losses.SparseCategoricalCrossentropy(from_logits=True)
    model.compile(loss=loss_fn, optimizer=opt, metrics=['accuracy'])
    return model


# takes the model produced by the previous function and the dataset and labels produced by the first function and
# trains the data for T epochs; does not return anything
def train_model(model, train_images, train_labels, T):
    model.fit(train_images, train_labels, epochs=T)
    return


# takes the trained model produced by the previous function and the test image/labels, and prints the evaluation
# statistics as described below (displaying the loss metric value if and only if the optional parameter has not been
# set to False); does not return anything
def evaluate_model(model, test_images, test_labels, show_loss=True):
    test_loss, test_accuracy = model.evaluate(test_images, test_labels, verbose=0)
    if show_loss:
        print("Loss:", '{:.4f}'.format(test_loss))
        print("Accuracy:", '{:.2f}'.format(test_accuracy*100), end='%\n')  # print and fix for decimal
    else:
        print("Accuracy:", '{:.2f}'.format(test_accuracy*100), end='%\n')  # print and fix for decimal
    return


# takes the trained model and test images, and prints the top 3 most likely labels for the image at the given index,
# along with their probabilities; does not return anything
def predict_label(model, test_images, index):
    class_names = ['Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine']
    prediction = model.predict(test_images, verbose=0)
    largest_labels = []
    largest = []
    for i in range(3):  # find 3 most likely items
        label_add = ""
        predict_add = 0
        for k, predicted in enumerate(prediction[index]):  # go over predictions at index
            if class_names[k] in largest_labels and predicted in largest:  # largest item already in our list
                pass
            else:  # if not checking and item already in our list of largest
                if predicted > predict_add:  # if the item is larger
                    label_add = class_names[k]
                    predict_add = predicted
        # iteration done so add the largest item we found to the lists
        largest_labels.append(label_add)
        largest.append(predict_add)
    # largest found, now to print out
    for j in range(3):
        print(str(largest_labels[j]) + ":", '{:.2f}'.format(largest[j]*100), end="%\n")  # print and fix for decimal
    return


# Testing here
if __name__ == '__main__':
    # Your debugging code goes here.
    # print("Training")
    # (images, labels) = get_dataset()
    # print(type(images))
    # print(type(labels))
    # print(type(labels[0]))
    # print_stats(images, labels)
    # print("Testing")
    # (t_images, t_labels) = get_dataset(False)
    # print(type(t_images))
    # print(type(t_labels))
    # print(type(t_labels[0]))
    # print_stats(t_images, t_labels)
    # print("building model")
    # modelo = build_model()
    # print(modelo)
    # print(modelo.loss)
    # print(modelo.optimizer)
    # print("train model")
    # train_model(modelo, images, labels, 10)
    # print("evaluate model")
    # evaluate_model(modelo, images, labels, show_loss=False)
    # evaluate_model(modelo, images, labels)
    # print("Predicting Label")
    # modelo.add(keras.layers.Softmax())
    # predict_label(modelo, images, 1)
    pass
