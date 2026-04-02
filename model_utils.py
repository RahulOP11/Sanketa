import os
import tensorflow as tf
from tensorflow.keras import layers, models

def get_mnist_model(model_path="mnist_cnn.h5"):
    """
    Loads the MNIST CNN model if it exists, otherwise trains a new one and saves it.
    """
    if os.path.exists(model_path):
        print(f"Loading existing model from {model_path}")
        return tf.keras.models.load_model(model_path)
    
    print("Training a new MNIST CNN model...")
    # Load data
    (train_images, train_labels), _ = tf.keras.datasets.mnist.load_data()
    
    # Preprocess data
    train_images = train_images.reshape((60000, 28, 28, 1))
    train_images = train_images.astype('float32') / 255
    
    # Build model (simple CNN)
    model = models.Sequential()
    model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.Flatten())
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(10, activation='softmax'))
    
    # Compile and train
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
                  
    model.fit(train_images, train_labels, epochs=5, batch_size=64, validation_split=0.1)
    
    # Save model
    model.save(model_path)
    print(f"Model saved to {model_path}")
    return model

def predict_digit(model, image_array):
    """
    Predicts a single digit image (28x28 numpy array).
    """
    # Preprocess image for the model
    # Image should be 28x28, grayscale, inverted (digits=white, bg=black), and normalized to 0-1
    img = image_array.reshape(1, 28, 28, 1).astype('float32') / 255.0
    predictions = model.predict(img, verbose=0)
    return tf.argmax(predictions, axis=1).numpy()[0]
