import requests
import logging
from decouple import config
from pathlib import Path

logging.basicConfig(filename='app.log', 
    format='%(asctime)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

base_url = config('ODK_PROJECT_URL')
headers = {}
service_params = {
    'projectId': config('ODK_PROJECT_ID'),
    'xmlFormId': config('ODK_FORM_ID')
}

def authenticate():
    email = config('ODK_EMAIL')
    password = config('ODK_PASSWORD')
    login_url = f'{base_url}v1/sessions'

    try:
        response = requests.post(
            login_url,
            json={'email': email, 'password': password}
        )
    except requests.exceptions.RequestException as err:
        logger.error(f'Authentication error: {err}')

    if response.status_code != 200:
        logger.error(f'Authentication failed')
        return None

    logger.info('Authenticated')
    return response.json()['token']

def save_dataset(data_response):
    dataset_file = Path('data/dataset.zip')
    dataset_file.touch(exist_ok=True)

    with open(dataset_file, 'wb') as f:
        f.write(data_response.content)

def get_submissions():
    token = authenticate()
    headers = {'Authorization': f'Bearer {token}'}

    service_doc_url = f'{base_url}v1/projects/{service_params["projectId"]}/forms/{service_params["xmlFormId"]}.svc'

    try:
        service_doc_response = requests.get(service_doc_url, headers=headers)
        if service_doc_response.status_code != 200:
            logger.error(f'Service document error: {service_doc_response.text}')
        logger.info('Service document response fetched')
    except requests.exceptions.RequestException as err:
        logger.error(f'Service document error: {err}')


    # get ODK form submissions csv
    csv_url = f'{base_url}v1/projects/{service_params["projectId"]}/forms/{service_params["xmlFormId"]}/submissions.csv.zip'
    logger.info(csv_url)

    try:
        data_response = requests.get(csv_url, headers=headers, params={'attachments': 'true'})
        if data_response.status_code != 200:
            logger.error(f'Error fetching data: {data_response.text}')
        logger.info('Media and csv zip response fetched')
        save_dataset(data_response)
    except requests.exceptions.RequestException as err:
        logger.error(f'Error fetching data: {err}')


if __name__=='__main__':
    get_submissions()