from dataclasses import replace
from tkinter.ttk import Separator
import requests
from bs4 import BeautifulSoup
from POO_get_URL import get_url

def get_html(url):
    try:
        data = requests.get(url)
        data.raise_for_status()
        return data.text
    except(requests.RequestException, ValueError):
        print ('сетевая ошибка')
        return False

def get_data():
    url_list = get_url()
    poo_data = []
    for url in url_list:
        try:
            print (url)
            html = get_html(url['url'])
            if html:
                soup = BeautifulSoup(html, 'html.parser')
                name = soup.find('div', class_='reestr').find('h3').text
                birth = soup.find('div', class_='reestr').find('p').text.replace('\t', ' ')
                data = soup.find('div', class_='reestr').findAll('tr')
                members = []
                
                if data[0].get_text(separator='\n').split()[0] != 'Исключен':
                
                    tiket = data[0].find('td', class_='posrel').text.replace(data[0].find('div', class_='ch_sole').text, "").replace('\n', ' ')
                    inner_id_and_regdate_raw = data[3].find('td', class_='posrel').get_text(separator='\n').split('\n')
                    inner_id_and_regdate = f'{inner_id_and_regdate_raw[0]} {inner_id_and_regdate_raw[1]}'
                    region = data[4].find('td', class_='posrel').text.replace(data[4].find('div', class_='ch_sole').text, "").replace('\xa0\n', ' ')
                    contacts = data[5].find('td', class_='posrel').text.replace(data[5].find('div', class_='ch_sole').text, "").replace('\n', ' ')
                    insurance_raw = data[8].find('td', class_='posrel').get_text(separator='\n').split('\n')
                    insurance = f'{insurance_raw[2]} {insurance_raw[3]} {insurance_raw[4]}; {insurance_raw[26]} {insurance_raw[27]} {insurance_raw[28]}'
                    inn = data[15].find('td', class_='posrel').text.replace(data[15].find('div', class_='ch_sole').text, "").replace('\n', ' ')



                    members.append({
                        'name': name,
                        'birth': birth,
                        'tiket': tiket,
                        'inner_id_and_regdate': inner_id_and_regdate,
                        'region': region,
                        'contacts': contacts,
                        'insurance': insurance,
                        'inn': inn
                    })
                    poo_data.append(members)
        except(IndexError, AttributeError):
            print ('Неверно заполненна таблица') 
    return poo_data
    
    
if __name__ == '__main__':
    print (get_data())