"""
PURPOSE :Train models
"""
import os
import tensorflow as tf
import util
import const
import pandas as pd
from multiprocessing import Process

keras = tf.keras


def train(model, version, train_generator, validation_generator, steps_per_epoch, save=True, csv=True, plot=True,
          connected=True, dropout=0.0, dense=4096, BN=False, AveragePooling=True, MutiFC=False,
          report=True):
    """
    training code for pet(cat and dog) emotion. by now only support 'cat' or 'dog'
    :param report: if show classification report
    :param test_face: will use pure face test data
    :param MutiFC: add multiple fully connected layers
    :param AveragePooling: add global average pooling layer
    :param BN: if add batch normalization before fully-connected layer
    :param load_model: if load existed model
    :param dense: set number of cells in fully-connected layer
    :param dropout: set dropout ratio (float)
    :param connected: if add a fully connected layer
    :param classify: cat or dog
    :param model: the name of pre-trained model
    :param version: the current version
    :param plot: decide if need to plot & save images of acc and loss
    :param csv: if save the history to csv
    :param save: if save the model
    """

    # load pre-trained model from keras.application

    # create model
    model, modelName = util.create_model(model, connected, dropout, dense, BN, AveragePooling, MutiFC)

    MODEL_PATH = '../../../../dogs-vs-cats-dataset/'
    # file name for model
    modelPath = os.sep + modelName + version

    # compile model
    model.compile(optimizer=keras.optimizers.Adam,
                  loss=keras.losses.binary_crossentropy,
                  metrics=['accuracy'])
    model.summary()
    print('Now is running: ', ' Cat vs Dog ', version)

    # fit the model
    history = model.fit(train_generator, steps_per_epoch=steps_per_epoch, epochs=const.EPOCH,
                        validation_data=validation_generator, workers=4,
                        )

    # save model history to csv for further analyse
    if csv:
        pd.DataFrame(history.history).to_csv(MODEL_PATH + modelPath + '.csv')

    # summarize history for accuracy & loss
    if plot:
        util.plotInfo(MODEL_PATH, modelPath, history)

    # save model
    if save:
        try:
            model.save(MODEL_PATH + modelPath + '.h5')
        except OSError:
            # I found a bug in saving model with tf. it shows os error but it did save model
            print("OSError, is it saved? ")
            pass

    # show each class report
    if report:
        y_actual = validation_generator.classes
        y_predicted = model.predict(validation_generator)
        class_ = util.get_confusion_matrix(y_actual=y_actual, y_predicted=y_predicted)
        print(class_)


# ------------------------------------------------------------------
if __name__ == "__main__":
    tf.keras.backend.clear_session()
    trainPath = '../../../../dogs-vs-cats-dataset/train'
    validationPath = '../../../../dogs-vs-cats-dataset/test'
    train_generator, validation_generator, steps_per_epoch = util.load_Cat_Dog(trainPath, validationPath)
    train('VGG19', '', train_generator, validation_generator, steps_per_epoch, plot=False, dense=2048, BN=True)

