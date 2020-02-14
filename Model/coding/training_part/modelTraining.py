import tensorflow as tf
import util
import const
import pandas as pd
from multiprocessing import Process


keras = tf.keras


def train(classify, model, version, save=True, csv=True, plot=True, fine_tuning=False):
    """
    training code for pet(cat and dog) emotion

    :param fine_tuning:
    :param steps_per_epoch: step per epoch
    :param validation_generator: test data iterator
    :param train_generator: train data iterator
    :param classify: cat or dog
    :param model: the name of pre-trained model
    :param version: the current version
    :param plot: decide if need to plot & save images of acc and loss
    :param csv: if save the history to csv
    :param save: if save the model
    """
    # classify = 'cat'  # by now only support 'cat' or 'dog'

    # load pre-trained model from keras.application
    train_generator, validation_generator, steps_per_epoch = util.get_Classify(classify)
    model, modelName = util.create_model(model)
    if not fine_tuning:
        # compile model
        model.compile(optimizer=const.MODEL_OPTIMISER,
                      loss=const.MODEL_LOSS,
                      metrics=['accuracy'])
        # fit the model
        history = model.fit_generator(
            train_generator,
            steps_per_epoch=steps_per_epoch,
            epochs=const.EPOCH,
            validation_data=validation_generator)

    else:
        # first: train only the top layers (which were randomly initialized)
        # i.e. freeze all convolutional InceptionV3 layers
        model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
        # train the model on the new data for a few epochs
        model.fit_generator(
            train_generator,
            steps_per_epoch=steps_per_epoch,
            epochs=1,
            validation_data=validation_generator)
        model.compile(optimizer=keras.optimizers.SGD(lr=0.0001, momentum=0.9),
                      loss='categorical_crossentropy', metrics=['accuracy'])
        model.fit(train_generator,
                  steps_per_epoch=steps_per_epoch,
                  epochs=const.EPOCH,
                  validation_data=validation_generator)

    modelPath = classify + ' ' + modelName + version
    # save model
    if save:
        model.save(const.MODEL_PATH + modelPath + '.h5')

    # save model history to csv for further analyse
    if csv:
        pd.DataFrame(history.history).to_csv(const.MODEL_PATH + modelPath + '.csv')

    # summarize history for accuracy & loss
    if plot:
        util.plotInfo(const.MODEL_PATH, modelPath, history)


# ------------------------------------------------------------------
if __name__ == "__main__":
    Pet = 'dog'
    version = '_v2'
    # train(Pet, 'InceptionV3', version, plot=False, fine_tuning=False, save=True, csv=True)
    #
    # MobileNetV2 = Process(target=train(Pet, 'MobileNetV2', version, plot=False))
    # Xception = Process(target=train(Pet, 'Xception', version, plot=False))
    # InceptionResNetV2 = Process(target=train(Pet, 'InceptionResNetV2', version, plot=False))
    # InceptionV3 = Process(target=train(Pet, 'InceptionV3', version, plot=False))
    VGG19 = Process(target=train(Pet, 'VGG19', version, plot=False))

    # MobileNetV2.start()
    # MobileNetV2.join()
    # Xception.start()
    # Xception.join()
    # InceptionV3.start()
    # InceptionV3.join()
    # InceptionResNetV2.start()
    # InceptionResNetV2.join()

    VGG19.start()
    VGG19.join()
