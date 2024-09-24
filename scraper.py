
from bs4 import BeautifulSoup
import requests
from io import StringIO
import pandas as pd


def get_url(id):
    url = f'https://www.parkrun.org.uk/parkrunner/{id}/5k'

    headers={
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }

    page = requests.get(url,headers=headers, verify=False) #verify= False to stop issue with limit

    return page

def convert_to_seconds(time_str: str):

    """
    converts strings of time in format 10:33 or 01:01:42 into time in seconds
    """

    parts = time_str.split(':')
    if len(parts) == 2:
        time_str = '00:' + time_str

    return pd.to_timedelta(time_str).total_seconds()

    


def extract_results_table(page):

    soup = BeautifulSoup(page.text, 'html.parser')

    # The third table is the table of 5k results
    results_table = soup.find_all('table')[2]

    html_string_io = StringIO(str(results_table))
    results_table_df = pd.read_html(html_string_io)[0]

    # Step 1: Convert the date and time strings
    results_table_df['Run Date'] = pd.to_datetime(results_table_df['Run Date'], format='%d/%m/%Y')
    
    results_table_df['Time'] = results_table_df['Time'].apply(convert_to_seconds)

    return results_table_df


def get_results_table(id):

    page = get_url(id)

    results_table_df = extract_results_table(page)

    return results_table_df

if __name__ == "__main__":

    # the functions get us the html for 5k times for a specified parkrun users
    user_page = get_url(3430977) #1674
    
    # we can view the structure of the page using 
    soup = BeautifulSoup(user_page.text, 'html.parser')
    print(soup.prettify())

    # user name
    user_string = soup.h2.get_text()
    print(user_string)

    name_string = user_string.split('\xa0')[0]
    print(name_string)
    

    # we can check the captions for the tables in the document (expect 3 tables)
    for table in soup.find_all('table'):
        print(table.caption)

    # we can extract and print a table
    print(extract_results_table(user_page))
