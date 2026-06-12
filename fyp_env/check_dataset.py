import pandas as pd
import os

FILE_NAME = "custom_webcam_data.csv"

print("\n📊 BridgeSign AI: Dataset Inspector")
print("="*40)

if not os.path.exists(FILE_NAME):
    print(f"❌ Could not find '{FILE_NAME}'. Make sure you are in the right folder!")
else:
    # Load the dataset
    df = pd.read_csv(FILE_NAME)
    
    # Get the total number of frames
    total_frames = len(df)
    
    # Get the count of each individual letter
    # The label is the last column, we count how many times each letter appears
    counts = df['label'].value_counts()
    
    print(f"🧬 Total Frames Recorded: {total_frames}\n")
    print("🎯 Breakdown by Letter:")
    print("-" * 20)
    
    for letter, count in counts.items():
        # Calculate roughly how many "sessions" of 200 frames this represents
        sessions = count / 200
        print(f"   Sign '{letter}': {count} frames (~{sessions:.1f} sessions)")
        
    print("-" * 20)
    print("💡 Pro-Tip: Try to keep the number of frames roughly equal for all letters!")
    print("="*40 + "\n")