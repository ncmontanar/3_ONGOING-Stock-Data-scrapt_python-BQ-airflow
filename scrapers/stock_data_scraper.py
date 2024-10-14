#stock_data_scraper.py

from requests import get        # pour effectuer des requêtes HTTP 
from bs4 import BeautifulSoup as bs # pour analyser le HTML
import re                       # pour les expressions régulières
import pandas as pd             #pour manipuler les données
import os                       # pour gérer les variables d’environnement.
from dotenv import load_dotenv
import requests
from google.cloud import bigquery
from google.api_core.exceptions import NotFound

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()


class StockDataScraper:
    def __init__(self, project_id, dataset_id, table_id):
        self.url = "https://www.investing.com"
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.table_id = table_id
        self.headers = []       # Initialize headers as an empty list    pour stocker les en-têtes de colonnes.
        self.total_data = []    # stocker toutes les données scrappées.
        
            # Utilisation des variables
        print(f"Project ID: {project_id}")
        print(f"Dataset ID: {dataset_id}")
        print(f"Table ID: {table_id}")
     
    # connect avec la source
    def get_soup(self, url):
        soup = None
        try:
            #url = "https://www.investing.com"
            response = get(url)
            response.raise_for_status()  # Raise an exception for non-200 status codes
            html = response.text
            soup = bs(html, "html.parser")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching the webpage: {e}")
        return soup

    # Extrait le lien et le nom de l’action depuis une ligne de tableau HTML.
    def get_stock_link(self, row):
        link_element = row.find("a")
        link = f"{link_element.get('href')}-historical-data"
        stock_name = link_element.text

        return {
            "stock_name": stock_name,
            "link": link
        }

    # Scrape les données historiques des actions et les stocke dans total_data
    def fetch_data(self):
        soup =  self.get_soup(self.url)     
        
        regex = re.compile('.*datatable.*')
        tbody = soup.find("tbody", class_=regex)
        #print(tbody)
        
        historical_data_links = [self.get_stock_link(row) for row in tbody.find_all("tr")]
        
        for stock in historical_data_links:
            link = stock['link']
            stock_name = stock['stock_name']
            soup = self.get_soup(link)
            
            regex = re.compile('.*freeze-column.*')
            table = soup.find("table", class_=regex)
            
            if not len(self.headers):
                thead = table.find("thead")
                header_cols = thead.find_all("th")
                self.headers = [ele.text.strip() for ele in header_cols]
            
            tbody = table.find("tbody")
            rows = tbody.find_all("tr")
            
            for row in rows :
                cols = row.find_all("td")
                cols = [ele.text.strip() for ele in cols]
                data = dict(zip(self.headers, cols))
                data['stock_name'] = stock_name
                self.total_data.append(data)
                
                print(f"Fetched data for {stock_name}")
    
    #  dataset et une table dans BigQuery si elles n’existent pas déjà
    def create_bigquery_table(self):
        client = bigquery.Client(project = self.project_id)
        
        dataset = bigquery.Dataset(f"{self.project_id}.{self.dataset_id}")
        dataset.location = "US"
        
        try:
            dataset = client.get_dataset(f"{self.project_id}.{self.dataset_id}")  # Make an API request.
            print("Dataset {} already exists".format(self.dataset_id))
        except NotFound:
            print("Dataset {} is not found".format(self.dataset_id))
            dataset = client.create_dataset(dataset, timeout=30)
            
        schema = [
            bigquery.SchemaField("stock_name", "STRING"),
            bigquery.SchemaField("Date", "DATE"),
            bigquery.SchemaField("Open", "FLOAT"),
            bigquery.SchemaField("High", "FLOAT"),
            bigquery.SchemaField("Low", "FLOAT"),
            bigquery.SchemaField("Price", "FLOAT"),
            bigquery.SchemaField("VOL", "FLOAT"),
            bigquery.SchemaField("Change", "FLOAT"),
        ]
        
        table_ref = dataset.table(self.table_id)
        table = bigquery.Table(table_ref, schema = schema)
        
        try:
            #client.get_table(table)
            self.table = client.get_table(table)
            print(f"Table {self.table_id} already exists")
        except NotFound:
            print(f"Table {self.table_id} is not found")
            #table = client.create_table(table)
            self.table = client.create_table(table)
            print(f"Created table {table.full_table_id}")
    
    #valeurs de volume en flottants, prenant en compte les suffixes
    def convert_to_float(self,x):
        if not x or x == 'nan':
            return None
        
        if x.endswith('M'):
            return float(x[:-1]) * 1e6
        elif x.endswith('B'):
            return float(x[:-1]) * 1e9
        elif x.endswith('K'):
            return float(x[:-1]) * 1e3
        else:
            return float(x)
    
    # Nettoie et transforme les données scrappées
    def process_data(self):
        data = pd.DataFrame(self.total_data)
        
        data['Date']= pd.to_datetime(data['Date'])
        data['Price'] = data['Price'].str.replace(',', '').astype(float)
        data['Open'] = data['Open'].str.replace(',', '').astype(float)
        data['High'] = data['High'].str.replace(',', '').astype(float)
        data['Low'] = data['Low'].str.replace(',', '').astype(float)
        
        data.rename(columns={'Change %': 'Change'}, inplace=True)
        data['Change'] = data['Change'].str.rstrip('%').astype(float)
        
        data['Vol.'] = data['Vol.'].astype(str)
        data.rename(columns={'Vol.': 'Vol'}, inplace=True)
        data['Vol'] = data['Vol'].apply(self.convert_to_float)
        
        self.total_data = data
        #return data
    
    # Load data from DataFrame to BigQuery
    def load_data_to_biquery(self):
        
        client = bigquery.Client(project= self.project_id)
        
        job_config = bigquery.LoadJobConfig()
        job = client.load_table_from_dataframe(self.total_data, self.table, job_config = job_config)
        print(f"Starting job {job.job_id}")
        job.result()
        print(f"Finished job {job.job_id}")

#executer 
if __name__ == "__main__":
    project_id = os.getenv("PROJECT_ID")
    dataset_id = os.getenv("DATASET_ID")
    table_id = os.getenv("TABLE_ID")
    
    scraper = StockDataScraper(project_id, dataset_id, table_id)
    print("Fetching data...")
    scraper.fetch_data()
    print("Processing data...")
    scraper.process_data()
    print("Creating BigQuery table...")
    scraper.create_bigquery_table()
    print("Loading data to BigQuery...")
    scraper.load_data_to_biquery()
    print("Data loaded to BigQuery")

#--------------------------------------------------#