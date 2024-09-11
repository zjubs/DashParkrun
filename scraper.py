
from bs4 import BeautifulSoup
import requests
from io import StringIO
import pandas as pd

def get_results_table(id):

    url = f'https://www.parkrun.org.uk/parkrunner/{id}/5k'

    headers={
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }

    page = requests.get(url,headers=headers, verify=False) #verify= False to stop issue with limit
    soup = BeautifulSoup(page.text, 'html.parser')

    # The third table is the table of 5k results
    results_table = soup.find_all('table')[2]
    #results_table_df = pd.read_html(str(results_table))

    html_string_io = StringIO(str(results_table))
    results_table_df = pd.read_html(html_string_io)[0]

    # Step 1: Convert the date and time strings
    results_table_df['Run Date'] = pd.to_datetime(results_table_df['Run Date'], format='%d/%m/%Y')
    results_table_df['Time'] = pd.to_timedelta('00:' + results_table_df['Time']).dt.total_seconds()

    #print(results_table_df)
    #results_table_df.info()
    return results_table_df