
import requests
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


if __name__ == "__main__":

    user_page = get_url(1674) #1674
