import pandas as pd
import os

INPUT_FILE = "custom_webcam_data.csv"
OUTPUT_FILE = "final_cleaned_data.csv"
TARGET_FRAMES = 1200

print("\n🧹 BridgeSign AI: Dataset Sanitizer")
print("="*45)

if os.path.exists(INPUT_FILE):
    df = pd.read_csv(INPUT_FILE)
    initial_count = len(df)
    
    # 1. Remove the accidental/old classes
    df = df[df['label'] != 'II']
    df = df[df['label'] != 'DEL']
    print("🗑️ Removed accidental 'II' and old 'DEL' classes.")
    
    # 2. Trim overweight classes down to 1200
    cleaned_frames = []
    grouped = df.groupby('label')
    
    for letter, group in grouped:
        count = len(group)
        if count > TARGET_FRAMES:
            print(f"✂️ Trimming '{letter}': {count} -> {TARGET_FRAMES}")
            trimmed = group.sample(n=TARGET_FRAMES, random_state=42)
            cleaned_frames.append(trimmed)
        else:
            print(f"✅ Keeping '{letter}': {count} frames")
            cleaned_frames.append(group)
            
    # 3. Combine and shuffle
    final_df = pd.concat(cleaned_frames)
    final_df = final_df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    # 4. Save the perfect dataset
    final_df.to_csv(OUTPUT_FILE, index=False)
    
    print("="*45)
    print(f"🎉 Success! Dataset is perfectly clean and balanced.")
    print(f"📁 Saved as: '{OUTPUT_FILE}'")
else:
    print(f"❌ Error: Could not find '{INPUT_FILE}'.")