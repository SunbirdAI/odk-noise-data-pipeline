# ODK Noise Data Pipeline
A pipeline for downloading, cleaning and transforming noise data from our ODK Central server

### Overview
This project uses the [ODK Central API](https://odkcentral.docs.apiary.io/#introduction/api-overview) to download the data. 

# Running the project
- Clone the repository: `git clone https://github.com/SunbirdAI/odk-noise-data-pipeline.git`
- In your terminal, change directory to the repository folder: `cd odk-noise-data-pipeline`
- Create and run a virtual environment: `python3 -m virtualenv venv`, then `source venv/bin/activate`
- Create a `.env` file in the project root and fill in the environment variables as shown in the provided `env.example` file
- Run the script: `python bulk_odk_download.py`. The script downloads the ODK data and creates a `data` folder for it in the root folder of the project