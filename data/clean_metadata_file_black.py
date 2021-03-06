"""
Clean up data collection csv file.
Errors noticed:
1. The classes are not numeric, which came over from the previous
   data uploaded e.g. 'Other', 'car-OR-truck', etc.
2. The classes are not of the same data type, some are strings e.g.
   '11', others are numeric.
3. The class ids do not start at 0. Instead they start at 1 and end at 19, 
    with class 'Other' being 19
4. There is test data included in the csv (data with the 'Noise-Comment' as
    something similar to 'Test')
5. Some media files are duplicated and should no longer appear in the
    csv file after deduplication has been done

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
]
NOISE_CLASS_COLUMNS = [
    "Noise-Noise_Source",
    "Noise-Noise_Source_2",
    "Noise-Noise_Source_3"
]

meta_data = pd.read_csv(META_FILE)
original_len = len(meta_data)

# Cleaning of column types and names
for column in NOISE_CLASS_COLUMNS:
    # Remove rows with string classes
    meta_data = meta_data[
        ~meta_data[column].isin(STRING_CLASSES)
    ]
    # Convert class labels to numeric and fill in null values
    meta_data[column] = (
        pd.to_numeric(meta_data[column], errors="coerce")
        .fillna(999)
        .astype(np.int64)
    )
    # Convert the category 'Other' from class id 19 to class id 0
    meta_data.loc[meta_data[column] == 19, column] = 0

# Remove test data (data with "Test" comments in the Noise_Comment column)
meta_data = meta_data[meta_data["Noise-Comment"].str.contains("Test", na=False, regex=True) == False]

# Create subset of metadata file with corresponding audio wav
# files in the de-duplicated folder.
audio_files = [str(f.name) for f in BASE_DIR.glob("*.wav")]
audio_meta_data = meta_data[meta_data["Noise-audio"].isin(audio_files)]

# Remove duplicated audio file names
audio_meta_data.drop_duplicates(subset=["Noise-audio"], inplace=True)

audio_meta_data.to_csv("noise_metadata.csv", index=False)

print(
    f"Cleaning resulted in a decrease in datapoints from {original_len} to {len(audio_meta_data)}."
)
print("New metadata file saved to: noise_metadata.csv")
