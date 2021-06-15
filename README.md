# ODK Noise Data Pipeline
A pipeline for downloading, cleaning and transforming noise data from our ODK Central server

### Overview
This project uses the [ODK Central API](https://odkcentral.docs.apiary.io/#introduction/api-overview) to download the data. 

# Running the project
- Clone the repository: `git clone https://github.com/SunbirdAI/odk_noise_data_pipeline.git`
- Create a `.env` file in the project root folder and fill in the env variables as shown in the `env.example` file
- Run `python bulk_odk_download.py` to download the noise data from ODK