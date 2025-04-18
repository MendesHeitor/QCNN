# Loads and Processes the data that will be used in QCNN and Hierarchical Classifier Training
import numpy as np
import tensorflow as tf
from sklearn.decomposition import PCA
from tensorflow.keras.models import Model
from tensorflow.keras import layers, losses
import matplotlib.pyplot as plt  # Add this import at the top of the file

pca32 = ['pca32-1', 'pca32-2', 'pca32-3', 'pca32-4']
autoencoder32 = ['autoencoder32-1', 'autoencoder32-2', 'autoencoder32-3', 'autoencoder32-4']
pca30 = ['pca30-1', 'pca30-2', 'pca30-3', 'pca30-4']
autoencoder30 = ['autoencoder30-1', 'autoencoder30-2', 'autoencoder30-3', 'autoencoder30-4']
pca16 = ['pca16-1', 'pca16-2', 'pca16-3', 'pca16-4', 'pca16-compact']
autoencoder16 = ['autoencoder16-1', 'autoencoder16-2', 'autoencoder16-3', 'autoencoder16-4', 'autoencoder16-compact']
pca12 = ['pca12-1', 'pca12-2', 'pca12-3', 'pca12-4']
autoencoder12 = ['autoencoder12-1', 'autoencoder12-2', 'autoencoder12-3', 'autoencoder12-4']

def data_load_and_process(dataset, classes=[0, 1], feature_reduction='resize256', binary=True):
    if dataset == 'fashion_mnist':
        (x_train, y_train), (x_test, y_test) = tf.keras.datasets.fashion_mnist.load_data()
    elif dataset == 'mnist':
        (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
    elif dataset == 'cifar10':
        (x_train, y_train), (x_test, y_test) = tf.keras.datasets.cifar10.load_data()
        # Resizing to 28x28 => !NOTE: We should experiment with another idea other than resizing it here
        x_train = tf.image.resize(x_train, (28, 28)).numpy()
        x_test = tf.image.resize(x_test, (28, 28)).numpy()
        # Convert to grayscale => !NOTE: We should experiment with another idea other than converting to grayscale it here
        x_train = tf.image.rgb_to_grayscale(x_train).numpy().squeeze()
        x_test = tf.image.rgb_to_grayscale(x_test).numpy().squeeze()
        y_train = y_train.squeeze()
        y_test = y_test.squeeze()

    # print(x_train.shape, x_test.shape, type(x_train), type(x_test))

    x_train, x_test = x_train[..., np.newaxis] / 255.0, x_test[..., np.newaxis] / 255.0  # normalize the data

    # print(x_train.shape, x_test.shape, type(x_train), type(x_test))

    if classes == 'odd_even':
        odd = [1, 3, 5, 7, 9]
        X_train = x_train
        X_test = x_test
        if binary == False:
            Y_train = [1 if y in odd else 0 for y in y_train]
            Y_test = [1 if y in odd else 0 for y in y_test]
        elif binary == True:
            Y_train = [1 if y in odd else -1 for y in y_train]
            Y_test = [1 if y in odd else -1 for y in y_test]

    elif classes == '>4':
        greater = [5, 6, 7, 8, 9]
        X_train = x_train
        X_test = x_test
        if binary == False:
            Y_train = [1 if y in greater else 0 for y in y_train]
            Y_test = [1 if y in greater else 0 for y in y_test]
        elif binary == True:
            Y_train = [1 if y in greater else -1 for y in y_train]
            Y_test = [1 if y in greater else -1 for y in y_test]

    else:
        # print(x_train.shape, x_test.shape, type(x_train), type(x_test))
        # print(y_train.shape, y_test.shape, type(y_train), type(y_test))
        x_train_filter_01 = np.where((y_train == classes[0]) | (y_train == classes[1]))
        x_test_filter_01 = np.where((y_test == classes[0]) | (y_test == classes[1]))
        # print(x_train.shape, x_test.shape, type(x_train), type(x_test))
        X_train, X_test = x_train[x_train_filter_01], x_test[x_test_filter_01]
        Y_train, Y_test = y_train[x_train_filter_01], y_test[x_test_filter_01]
        # print("66", X_train.shape, X_test.shape, type(X_train), type(X_test))
        if binary == False:
            Y_train = [1 if y == classes[0] else 0 for y in Y_train]
            Y_test = [1 if y == classes[0] else 0 for y in Y_test]
        elif binary == True:
            Y_train = [1 if y == classes[0] else -1 for y in Y_train]
            Y_test = [1 if y == classes[0] else -1 for y in Y_test]
        # print("73", X_train.shape, X_test.shape, type(X_train), type(X_test))
        
    if feature_reduction == 'resize256':
        # Save an image with label 0
        label_0_index = np.where(np.array(Y_train) == 0)[0][0]
        plt.imsave('label_0_image.png', X_train[label_0_index].squeeze(), cmap='gray')

        # Save an image with label 1
        label_1_index = np.where(np.array(Y_train) == 1)[0][0]
        plt.imsave('label_1_image.png', X_train[label_1_index].squeeze(), cmap='gray')

        X_train = tf.image.resize(X_train[:], (256, 1)).numpy()
        X_test = tf.image.resize(X_test[:], (256, 1)).numpy()
        # print(X_train.shape, X_test.shape, type(X_train), type(X_test))
        X_train, X_test = tf.squeeze(X_train).numpy(), tf.squeeze(X_test).numpy()
        # print(X_train.shape, X_test.shape, type(X_train), type(X_test))
        # print(len(Y_train), len(Y_test), type(Y_train), type(Y_test))
        return X_train, X_test, Y_train, Y_test

    elif feature_reduction == 'pca8' or feature_reduction in pca32 \
            or feature_reduction in pca30 or feature_reduction in pca16 or feature_reduction in pca12:

        X_train = tf.image.resize(X_train[:], (784, 1)).numpy()
        X_test = tf.image.resize(X_test[:], (784, 1)).numpy()
        X_train, X_test = tf.squeeze(X_train), tf.squeeze(X_test)

        if feature_reduction == 'pca8':
            pca = PCA(8)
        elif feature_reduction in pca32:
            pca = PCA(32)
        elif feature_reduction in pca30:
            pca = PCA(30)
        elif feature_reduction in pca16:
            pca = PCA(16)
        elif feature_reduction in pca12:
            pca = PCA(12)


        X_train = pca.fit_transform(X_train)
        X_test = pca.transform(X_test)

        # Rescale for angle embedding
        if feature_reduction == 'pca8' or feature_reduction == 'pca16-compact' or \
                feature_reduction in pca30 or feature_reduction in pca12:
            X_train, X_test = (X_train - X_train.min()) * (np.pi / (X_train.max() - X_train.min())),\
                              (X_test - X_test.min()) * (np.pi / (X_test.max() - X_test.min()))
        return X_train, X_test, Y_train, Y_test

    elif feature_reduction == 'autoencoder8' or feature_reduction in autoencoder32 \
            or feature_reduction in autoencoder30 or feature_reduction in autoencoder16 or feature_reduction in autoencoder12:
        if feature_reduction == 'autoencoder8':
            latent_dim = 8
        elif feature_reduction in autoencoder32:
            latent_dim = 32
        elif feature_reduction in autoencoder30:
            latent_dim = 30
        elif feature_reduction in autoencoder16:
            latent_dim = 16
        elif feature_reduction in autoencoder12:
            latent_dim = 12



        class Autoencoder(Model):
            def __init__(self, latent_dim):
                super(Autoencoder, self).__init__()
                self.latent_dim = latent_dim
                self.encoder = tf.keras.Sequential([
                    layers.Flatten(),
                    layers.Dense(latent_dim, activation='relu'),
                ])
                self.decoder = tf.keras.Sequential([
                    layers.Dense(784, activation='sigmoid'),
                    layers.Reshape((28, 28))
                ])

            def call(self, x):
                encoded = self.encoder(x)
                decoded = self.decoder(encoded)
                return decoded

        autoencoder = Autoencoder(latent_dim)

        autoencoder.compile(optimizer='adam', loss=losses.MeanSquaredError())
        autoencoder.fit(X_train, X_train,
                        epochs=10,
                        shuffle=True,
                        validation_data=(X_test, X_test))

        X_train, X_test = autoencoder.encoder(X_train).numpy(), autoencoder.encoder(X_test).numpy()

        # Rescale for Angle Embedding
        # Note this is not a rigorous rescaling method
        if feature_reduction == 'autoencoder8' or feature_reduction == 'autoencoder16-compact' or\
                feature_reduction in autoencoder30 or feature_reduction in autoencoder12:
            X_train, X_test = (X_train - X_train.min()) * (np.pi / (X_train.max() - X_train.min())), \
                              (X_test - X_test.min()) * (np.pi / (X_test.max() - X_test.min()))

        return X_train, X_test, Y_train, Y_test

