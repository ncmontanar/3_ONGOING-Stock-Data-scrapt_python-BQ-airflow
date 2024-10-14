# 0. Creer enviromment viruel
pip install virtualenv
virtualenv <your-env>  (dont <your-env> cest le nom de mon virtenv)

## ------ Activate the virtual environment: (: challeng1)

<your-env>\Scripts\activate
<your-env>\Scripts\pip.exe install google-api-python-client

## ------ Deactivate the environment:

deactivate

## ------------
gpedit.msc
regedit
## --

##  Install the libraries:
pip install --upgrade pip setuptools
pip install python-dotenv
pip install ipykernel *(provides the IPython kernel for Jupyter)*
pip install ipykernel -U --force-reinstall *
pip install requests 
pip install beautifulsoup4
pip install bs4
pip install os-sys *
pip install pandas
pip install apache-airflow 
pip install scrapers
pip install selenium
pip install -e .
pip install google-cloud

##  Install the google-cloud-bigquery library:
pip install google-cloud-bigquery

## Installing the required libraries
pip install google-cloud-bigquery python-dotenv pandas

## n dump the data to BigQuery
pip install pyarrow

## Follow the steps

## how to check the pip extention 
pip list

## how to check my python version (on ipynb)
import sys
print(sys.version)
## -------------------------------------
# 1.  Scrapping the sources
pip install requests 
pip install bs4

# 2. Accessing BigQuery through Python


## option A : Creating Environment variables

$env:GOOGLE_APPLICATION_CREDENTIALS = "C:\Users\a895279\....chemin vers ma clé"
echo $env:GOOGLE_APPLICATION_CREDENTIALS


$env:GOOGLE_APPLICATION_CREDENTIALS = "C:\Users\a895279\AppData\Roaming\gcloud\application_default_credentials.json"
$env:GOOGLE_APPLICATION_CREDENTIALS ="C:\Users\a895279\llaves\nelsonmontanatest2-99f16f3b6b2a.json"

## opt B:  Créez votre fichier d'identifiants :
 gcloud auth application-default login 

Credentials saved to file: [C:\Users\a895279\AppData\Roaming\gcloud\application_default_credentials.json]
Credentials saved to file: [C:\Users\a895279\AppData\Roaming\gcloud\application_default_credentials.json]

## -------------------------
  Credentials
    Grant and revoke authorization to Google Cloud CLI

      o gcloud auth login: Authorize Google Cloud access for the gcloud tool
        with Google user credentials and set current account as active.
      o gcloud auth activate-service-account: Like gcloud auth login but with
        service account credentials.
      o gcloud auth list: List all credentialed accounts.
      o gcloud auth print-access-token: Display the current account's access
        token.
      o gcloud auth revoke: Remove access credentials for an account.
## -------------------------

- suivre les pas : 
  - Basic Setup
  - connect to BQ
  - Creating the dataset
  - Define the Schema
  - Create the table
  - Changing the Data
Dumping the data to BigQuery
  - Load data from DataFrame to BigQuery 

# ---------------------------- Dockerizing the Application
## 
Create a 'src' directory for your project and place your Python script (stock_data_scraper.py) inside it. Additionally, create a .env file to store your environment variables (PROJECT_ID, DATASET_ID, TABLE_ID)

## Build the Docker Image
*Open a terminal, navigate to your project directory, and run the following command to build your Docker image*:

docker build -t stock-data-scraper1 .

## Running the Docker Container
Once the Docker image is built successfully, you can run a Docker container using the following command:

docker run --env-file .env stock-data-scraper1 .

# ---------------------------- 
## Automate the process of scraping stock data and loading it into Google BigQuery using Apache Airflow and Astronomer

- log in on https://www.astronomer.io
- Access to Google Cloud Platform (GCP) with BigQuery enabled
- Astronomer CLI installed 
  - *winget install -e --id Astronomer.Astro*
  - *astro version*
  - astro dev init - astro dev init stock_scraper
  - astro dev kill
  - astro dev start  :start our server and launch airflow
  - astro dev stop
  - astro dev restart

- in astro CLI : Initialize the  New Airflow Project
astro dev init stock_scraper_ncmontanar
 
 - THEN 
Delete the existing dags
Create a scrapers folder inside the dags folder
Move the stock_data_scraper.py we created in previous articles to this folder
Create a new empty stock_scraper_dag.py file in the dags folder
Create two __init__.py files. One in dags folder and one in dags/scrapers folder 

Writing your first DAG
We will write our first dag (stock_scraper_dag.py) whose goal is to run the stock_data_scraper.py code on a scheduled basis.

## install airflow
pip install apache-airflow
## install scrapers :  easy to use HTML/XML scraper. It supports both XPath and Regular Expression retrieval. Once you have a file you want to extract information from, you can extract multiple pieces of information with a simple function call. You should obtain the files you want to scrape by your own ways. ## 
pip install scrapers
pip install selenium

- Start the Airflow Server
`astro dev start`


### --------------------------- 
# 4.  Serving Data using FastAPI with Google BigQuery
- Install the required libraries/credentials

*pip install fastapi uvicorn google-cloud-bigquery*

# 