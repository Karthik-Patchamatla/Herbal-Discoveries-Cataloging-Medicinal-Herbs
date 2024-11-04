import matplotlib.pyplot as plt
from keras.applications import InceptionV3
from keras.models import Sequential
from keras.layers import GlobalAveragePooling2D, Dense, Dropout
from keras.preprocessing.image import ImageDataGenerator

# Set the paths to your datasets
train_data_dir = 'F:/Major/Data/Updated-Dataset/Dataset/Dataset'
validation_data_dir = 'F:/Major/Data/ValidationData'

# Data augmentation for the training dataset
train_datagen = ImageDataGenerator(
    rescale=1./255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)

# Data augmentation for the validation dataset
validation_datagen = ImageDataGenerator(rescale=1./255)

# Specify the input shape and batch size
input_shape = (224, 224, 3)
batch_size = 32

# Create generators for training and validation datasets
train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=input_shape[:2],
    batch_size=batch_size,
    class_mode='categorical'
)

validation_generator = validation_datagen.flow_from_directory(
    validation_data_dir,
    target_size=input_shape[:2],
    batch_size=batch_size,
    class_mode='categorical'
)

# Load the InceptionV3 base model (pre-trained on ImageNet)
base_model = InceptionV3(include_top=False, weights='imagenet', input_shape=input_shape)

# Freeze the convolutional layers
for layer in base_model.layers:
    layer.trainable = False

# Create a new model on top of the InceptionV3 base model
model = Sequential()
model.add(base_model)
model.add(GlobalAveragePooling2D())
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(30, activation='softmax'))  # Adjust to the number of classes in your dataset

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Print the model summary
model.summary()

# Train the model using the generators
num_epochs = 10  # You can adjust this based on your requirements
history = model.fit(
    train_generator,
    epochs=num_epochs,
    validation_data=validation_generator
)

# Plot training and validation accuracy
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.title('Training and Validation Accuracy')
plt.show()

# Save the trained model
model.save('newinceptionv3.h5')
print("Model saved successfully!")

# Evaluate the mobbb