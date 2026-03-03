"""
Training Script for Hand Cleanliness Classification
Trains a CNN model to classify hands into 3 categories: clean, medium, dirty
"""
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models, callbacks
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime

# Set random seeds for reproducibility
tf.random.set_seed(42)
np.random.seed(42)

def create_model(input_shape=(224, 224, 3), num_classes=3):
    """
    Create a lightweight CNN model suitable for ESP32 deployment
    
    Args:
        input_shape: Shape of input images (height, width, channels)
        num_classes: Number of output classes (3: clean, medium, dirty)
    
    Returns:
        Compiled Keras model
    """
    model = models.Sequential([
        # First convolutional block
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Second convolutional block
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Third convolutional block
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Fourth convolutional block
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Flatten and dense layers
        layers.Flatten(),
        layers.Dense(512, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.5),
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(num_classes, activation='softmax')  # 3 classes
    ])
    
    return model

def create_lightweight_model(input_shape=(224, 224, 3), num_classes=3):
    """
    Create an even lighter model using depthwise separable convolutions
    Better for ESP32 deployment
    """
    model = models.Sequential([
        # Input normalization
        layers.Rescaling(1./255, input_shape=input_shape),
        
        # First block
        layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        
        # Second block
        layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        
        # Third block
        layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        
        # Fourth block
        layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        
        # Global pooling instead of flatten (reduces parameters)
        layers.GlobalAveragePooling2D(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(num_classes, activation='softmax')
    ])
    
    return model

def train_model(train_dir='data/train', val_dir='data/val', 
                epochs=50, batch_size=32, image_size=224,
                model_type='lightweight'):
    """
    Train the hand cleanliness classification model
    
    Args:
        train_dir: Directory containing training images
        val_dir: Directory containing validation images
        epochs: Number of training epochs
        batch_size: Batch size for training
        image_size: Target image size (square)
        model_type: 'standard' or 'lightweight'
    """
    
    # Check if directories exist
    if not os.path.exists(train_dir):
        raise ValueError(f"Training directory {train_dir} does not exist!")
    if not os.path.exists(val_dir):
        raise ValueError(f"Validation directory {val_dir} does not exist!")
    
    # Data augmentation for training
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        zoom_range=0.2,
        brightness_range=[0.8, 1.2],
        fill_mode='nearest'
    )
    
    # Only rescaling for validation
    val_datagen = ImageDataGenerator(rescale=1./255)
    
    # Create data generators
    train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=(image_size, image_size),
        batch_size=batch_size,
        class_mode='categorical',
        shuffle=True
    )
    
    val_generator = val_datagen.flow_from_directory(
        val_dir,
        target_size=(image_size, image_size),
        batch_size=batch_size,
        class_mode='categorical',
        shuffle=False
    )
    
    # Get class names
    class_names = list(train_generator.class_indices.keys())
    print(f"\nClasses: {class_names}")
    print(f"Class indices: {train_generator.class_indices}")
    
    # Create model
    if model_type == 'lightweight':
        model = create_lightweight_model((image_size, image_size, 3), len(class_names))
        print("\nUsing lightweight model (better for ESP32)")
    else:
        model = create_model((image_size, image_size, 3), len(class_names))
        print("\nUsing standard model")
    
    # Compile model
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss='categorical_crossentropy',
        metrics=['accuracy', 'top_k_categorical_accuracy']
    )
    
    # Print model summary
    model.summary()
    
    # Callbacks
    checkpoint_callback = callbacks.ModelCheckpoint(
        'models/best_model.h5',
        monitor='val_accuracy',
        save_best_only=True,
        mode='max',
        verbose=1
    )
    
    early_stop_callback = callbacks.EarlyStopping(
        monitor='val_loss',
        patience=10,
        restore_best_weights=True,
        verbose=1
    )
    
    reduce_lr_callback = callbacks.ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=5,
        min_lr=1e-7,
        verbose=1
    )
    
    # Create models directory
    os.makedirs('models', exist_ok=True)
    
    # Train model
    print("\nStarting training...")
    history = model.fit(
        train_generator,
        epochs=epochs,
        validation_data=val_generator,
        callbacks=[checkpoint_callback, early_stop_callback, reduce_lr_callback],
        verbose=1
    )
    
    # Save final model
    model.save('models/final_model.h5')
    print("\nModel saved to models/final_model.h5")
    
    # Plot training history
    plot_training_history(history)
    
    return model, history, class_names

def plot_training_history(history):
    """Plot training and validation accuracy/loss"""
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    
    # Accuracy plot
    axes[0].plot(history.history['accuracy'], label='Training Accuracy')
    axes[0].plot(history.history['val_accuracy'], label='Validation Accuracy')
    axes[0].set_xlabel('Epoch')
    axes[0].set_ylabel('Accuracy')
    axes[0].set_title('Model Accuracy')
    axes[0].legend()
    axes[0].grid(True)
    
    # Loss plot
    axes[1].plot(history.history['loss'], label='Training Loss')
    axes[1].plot(history.history['val_loss'], label='Validation Loss')
    axes[1].set_xlabel('Epoch')
    axes[1].set_ylabel('Loss')
    axes[1].set_title('Model Loss')
    axes[1].legend()
    axes[1].grid(True)
    
    plt.tight_layout()
    plt.savefig('models/training_history.png', dpi=150)
    print("Training history plot saved to models/training_history.png")
    plt.close()

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Train hand cleanliness classification model')
    parser.add_argument('--train-dir', type=str, default='data/train',
                       help='Training data directory')
    parser.add_argument('--val-dir', type=str, default='data/val',
                       help='Validation data directory')
    parser.add_argument('--epochs', type=int, default=50,
                       help='Number of training epochs')
    parser.add_argument('--batch-size', type=int, default=32,
                       help='Batch size')
    parser.add_argument('--image-size', type=int, default=224,
                       help='Image size (square)')
    parser.add_argument('--model-type', type=str, default='lightweight',
                       choices=['standard', 'lightweight'],
                       help='Model type')
    
    args = parser.parse_args()
    
    model, history, class_names = train_model(
        train_dir=args.train_dir,
        val_dir=args.val_dir,
        epochs=args.epochs,
        batch_size=args.batch_size,
        image_size=args.image_size,
        model_type=args.model_type
    )
