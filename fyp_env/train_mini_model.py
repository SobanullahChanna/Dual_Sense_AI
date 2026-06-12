import numpy as np
import os
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split

# 1. Setup our 3 words
DATA_PATH = os.path.join('extracted_data', 'WLASL')
actions = np.array(['book', 'computer', 'drink']) 

# 2. Load the data into memory
sequences, labels = [], []
label_map = {label:num for num, label in enumerate(actions)}

print("Loading data into memory...")
for action in actions:
    action_path = os.path.join(DATA_PATH, action)
    if not os.path.exists(action_path): 
        continue
    
    # Go through every .npy file we extracted
    for sequence_file in os.listdir(action_path):
        res = np.load(os.path.join(action_path, sequence_file))
        sequences.append(res)
        labels.append(label_map[action])

# 3. Pad Sequences (Make all videos the exact same length)
# We will cap all videos at 60 frames. Short videos get padded with zeros.
MAX_FRAMES = 60 
X = pad_sequences(sequences, maxlen=MAX_FRAMES, dtype='float32', padding='post', truncating='post')

# 4. Format Labels (Convert words into numbers the AI understands)
y = to_categorical(labels).astype(int)

# 5. Split into Training Data and "Final Exam" Testing Data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)

print(f"✅ Data packaged perfectly!")
print(f"X (Features) Shape: {X.shape}")
print(f"y (Labels) Shape: {y.shape}")


from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

print("\nBuilding the LSTM Neural Network...")

# 6. Build the Brain Architecture
model = Sequential()

# Layer 1: The First LSTM layer. It looks at the 60 frames and 258 coordinates.
model.add(LSTM(64, return_sequences=True, activation='relu', input_shape=(60, 258)))
# Layer 2 & 3: Deep learning layers to understand complex motions.
model.add(LSTM(128, return_sequences=True, activation='relu'))
model.add(LSTM(64, return_sequences=False, activation='relu'))

# Layer 4 & 5: Dense layers to consolidate the learned patterns.
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))

# Layer 6: The Output Layer. It has 3 neurons (one for each word) and uses 'softmax' 
# to output a confidence percentage (e.g., "I am 90% sure this is 'book'").
model.add(Dense(actions.shape[0], activation='softmax'))

# 7. Compile the Brain
# We use categorical_crossentropy because we are choosing between multiple categories.
model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])

# 8. Train the Model!
print("\n🚀 Starting AI Training Phase (100 Epochs)...")
# Epochs = How many times the AI will review the data to study it.
model.fit(X_train, y_train, epochs=100)

print("\n✅ Mini-Model Training Complete!")

# 9. Save the Brain to your hard drive
model.save('dual_sense_mini_model.h5')
print("Model saved as 'dual_sense_mini_model.h5'")