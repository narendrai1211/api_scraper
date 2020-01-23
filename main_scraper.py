from bs4 import BeautifulSoup
import requests
import pandas as pd
dictionary = {}
headers = ['Sr. No', 'API Name', 'API URL', 'API Category', 'API Description']


def scrape_pages():
    cnt = 0
    base_url = 'https://www.programmableweb.com'
    url = 'https://www.programmableweb.com/category/all/apis'
    while True:
        data = requests.get(url)
        soup = BeautifulSoup(data.text, 'lxml')
        whole_table = soup.find('table', class_='views-table cols-4 table')
        table_body = whole_table.find('tbody')
        all_rows = table_body.find_all('tr')
        next_page = soup.find('li', class_='pager-last')
        next_page_url = ''
        for i in next_page:
            next_endpoint = i.get('href')
            next_page_url = base_url + next_endpoint
        for i in all_rows:
            api_name = i.find('td', class_='views-field views-field-pw-version-title').text
            api__link_outer = i.find('td', class_='views-field views-field-pw-version-title')
            endpoint = api__link_outer.find('a').get('href')
            final_api_link = base_url + endpoint
            api_category_tag = i.find('td', class_='views-field views-field-field-article-primary-category')
            api_category = api_category_tag.text
            api_description = i.find('td', class_='views-field-field-api-description').text
            cnt += 1
            dictionary[cnt] = [cnt, api_name, final_api_link, api_category, api_description]
        url = next_page_url
        print(url)
        if url == 'https://www.programmableweb.com/category/all/apis?page=10':
            break
        else:
            if next_page_url == '#':
                break


def write_to_csv():
    data_frame = pd.DataFrame.from_dict(data=dictionary,
                                        orient='index',
                                        columns=headers)
    print(data_frame.head())
    data_frame.to_csv('scraped_udemy.csv', index=False)


scrape_pages()
write_to_csv()
