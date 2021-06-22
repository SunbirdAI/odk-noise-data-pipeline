"""
Clean up data collection csv file.
Errors noticed:
1. The classes are not numeric, I think this came over from the previous
   data uploaded e.g. 'Other', 'car-OR-truck', etc.
2. The classes are not of the same data type, some are strings e.g.
   '11', others are numeric.

If you notice any other errors update this file.
"""

from pathlib import Path
import pandas as pd
import numpy as np

META_FILE = "build_Noise-Capture-Form_1614927724.csv"
BASE_DIR = Path("./media/")
STRING_CLASSES = [
    "Other",
    "car-OR-truck",
    "Mobile-music",
]  # TODO: Make this all string classes.

meta_data = pd.read_csv(META_FILE)
original_len = len(meta_data)

# Remove rows with string classes
meta_data = meta_data[
    ~meta_data["Noise-Noise_Source"].isin(STRING_CLASSES)
]  # Cleaning based only on primary class

# Convert class labels to numeric
meta_data["Noise-Noise_Source"] = (
    pd.to_numeric(meta_data["Noise-Noise_Source"], errors="coerce")
    .fillna(0)
    .astype(np.int64)
)
meta_data["Noise-Noise_Source_2"] = (
    pd.to_numeric(meta_data["Noise-Noise_Source_2"], errors="coerce")
    .fillna(0)
    .astype(np.int64)
)
meta_data["Noise-Noise_Source_3"] = (
    pd.to_numeric(meta_data["Noise-Noise_Source_3"], errors="coerce")
    .fillna(0)
    .astype(np.int64)
)

# Create subset of metadata file with corresponding audio wav
# files in the de-duplicated folder.
audio_files = [str(f.name) for f in BASE_DIR.glob("*.wav")]
audio_meta_data = meta_data[meta_data["Noise-audio"].isin(audio_files)]

audio_meta_data.to_csv("noise_metadata.csv", index=False)

print(
    f"Cleaning resulted in a decrease in datapoints from {original_len} to {len(audio_meta_data)}."
)
print("New metadata file saved to: noise_metadata.csv")
