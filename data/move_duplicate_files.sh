# Script to run fdupes and copy duplicates files

#!/bin/bash

noise_data_dir=./media
duplicates_dir=duplicated-files/

for file in $(fdupes -f $noise_data_dir | grep -v '^$')
do
  mv "$file" $duplicates_dir
done