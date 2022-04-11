import requests
from bs4 import BeautifulSoup

def get_html(url):
    try:
        data = requests.get(url)
        data.raise_for_status()
        return data.text
    except(requests.RequestException, ValueError):
        print ('сетевая ошибка')
        return False

def get_url():

    pages_url = ['http://sroroo.ru/about/reestr/']
    page_number = 2
    while True:
        if  page_number <= 43:
            pages_url.append(f'http://sroroo.ru/about/reestr/?PAGEN_1={page_number}')
        else: break
        page_number += 1
    for page in pages_url:
        html = get_html(page)
        if html:        
            soup = BeautifulSoup(html, 'html.parser')
            members_list = soup.find('div', class_='member-table').findAll('tr')
            del members_list[0]
            members_table = []
            for member in members_list:
                name = member.find('a').text
                url = member.find('a')['href']
                members_table.append({
                    "name": name,
                    "url": f'http://sroroo.ru{url}'
                })
    del members_table[0]
    return members_table

if __name__ == '__main__':
    print (get_url())