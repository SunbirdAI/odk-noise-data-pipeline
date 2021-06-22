"""
Get a sample of balanced classes from the noise dataset

"""

from pathlib import Path
import tarfile
import pandas as pd

NUM_SAMPLES = 100
META_FILE = "noise_metadata.csv"
BASE_DIR = Path("./media")
SAMPLEFILES_TAR = Path("./balancedsampledata_" + str(NUM_SAMPLES) + ".tar.xz")
SAMPLEFILES_META = "balancedsample_metadata_" + str(NUM_SAMPLES) + ".csv"

data = pd.read_csv(META_FILE)
sampled_data = pd.DataFrame()

for cls in data["Noise-Noise_Source"].unique():
    temp_df = data[data["Noise-Noise_Source"] == cls].sample(NUM_SAMPLES)
    sampled_data = pd.concat([sampled_data, temp_df])

# Save sampled data metadata
sampled_data.to_csv(SAMPLEFILES_META, index=False)

samplefilenames = list(sampled_data["Noise-audio"])
samplefilenames_fullpath = [BASE_DIR.joinpath(fpath) for fpath in samplefilenames]

# Save actual wav files in tar file
with tarfile.open(SAMPLEFILES_TAR, "w:xz") as tar:
    for ff in samplefilenames_fullpath:
        tar.add(ff)
