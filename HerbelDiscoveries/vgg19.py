import tensorflow as tf
from keras import layers, models
from keras.applications import VGG19  # Change import to VGG19
from keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt

# Set paths
train_data_dir = 'F:/Major/Data/Updated-Dataset/Dataset/dataset'
validation_data_dir = 'F:/Major/Data/TestData'
saved_model_path = 'model_multiclass_vgg19.h5'  # Change the model name if desired

# Define parameters
batch_size = 32
epochs = 10
image_size = (150, 150)
learning_rate = 0.0001

# Data augmentation for the training set
train_datagen = ImageDataGenerator(
    rescale=1./255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    validation_split=0.2
)

# Load and augment training data
train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=image_size,
    batch_size=batch_size,
    class_mode='categorical',
    subset='training'
)

# Load and rescale validation data
validation_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=image_size,
    batch_size=batch_size,
    class_mode='categorical',
    subset='validation'
)

# Create VGG19 model with pretrained weights (excluding top layers)
base_model = VGG19(input_shape=(150, 150, 3), include_top=False, weights='imagenet')  # Change to VGG19
base_model.trainable = False

# Build the final model
model = models.Sequential([
    base_model,
    layers.Flatten(),
    layers.Dense(256, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(30, activation='softmax')
])

# Compile the model with the specified learning rate
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Train the model
history = model.fit(
    train_generator,
    epochs=epochs,
    validation_data=validation_generator
)

# Plot accuracy over epochs
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.show()

# Save the trained model
# model.save(saved_model_path)
# print(f"Model saved to {saved_model_path}")
