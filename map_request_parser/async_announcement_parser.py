import fake_useragent
from bs4 import BeautifulSoup as bs
import aiohttp
import asyncio
import re
import csv
import lxml
from datetime import datetime
from async_map_request import parse_coords_and_ids

# Кустарная функция, чтобы гасить RunTimeError от aiohttp на Windows
from crutch import crutch

crutch()

# Создаем csv-файл и добавляем названия столбцов
with open('cian_data.csv', 'w', newline='', encoding='utf-8') as file:
    a_pen = csv.writer(file)
    a_pen.writerow(('AnnouncementID', 'Title', 'Address', 'Lat', 'Long', 'MetroStations', 'TimeToMetro', 'TotalArea',
                    'ConstructionYear', 'Price', 'Floor',
                    'Сonst/ComplYear', 'AccommodationType', 'Layout', 'Balconies', 'Renovation', 'Bathroom',
                    'WindowView',
                    'HouseType',
                    'FloorType', 'Entrances', 'Elevators', 'Heating', 'Emergency', 'Parking', 'GarbageChute'))


# Функция для записи полученных данных в таблицу
def file_writer(data_list):
    with open('cian_data.csv', 'a', newline='', encoding='utf-8') as file:
        a_pen = csv.writer(file)
        for item in data_list:
            a_pen.writerow(
                (item['AnnouncementID'], item['Title'], item['Address'],item['Lat'], item['Long'], item['MetroStations'], item['TimeToMetro'],
                 item['TotalArea'], item['ConstructionYear'], item['Price'], item['Floor'],
                 item['Сonst/ComplYear'], item['AccommodationType'], item['Layout'], item['Balconies'],
                 item['Renovation'], item['Bathroom'], item['WindowView'], item['HouseType'],
                 item['FloorType'], item['Entrances'], item['Elevators'], item['Heating'], item['Emergency'],
                 item['Parking'], item['GarbageChute']))


# Асинхронная функция для сбора данных по каждому объявлению
async def one_page_parser(coords_and_ids, headers):
    url = f'https://www.cian.ru/sale/flat/{str(int(coords_and_ids[0]))}/'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:

                html_body = await response.read()

                # Просто чтобы видеть, что процесс идет
                print(int(coords_and_ids[0]))

                inner_soup = bs(html_body, 'lxml')

                # Обновляемый список для занесения данных по каждому объвлению на каждой итерации
                data_list = []

                # Айдишник объявления, по которому можно будет его найти
                ancmnt_id = coords_and_ids[0]

                lat = float(coords_and_ids[1][0])

                long = float(coords_and_ids[1][1])

                # Адрес
                try:
                    address_list = []
                    inner_div = inner_soup.find_all('address', attrs={'class': 'a10a3f92e9--address--140Ec'})
                    for item in inner_div:
                        address = item.text
                        address_list.append(address)
                except AttributeError:
                    address_list = None

                # Обновляющаяся переменная для записи станций метро
                metro_stations_list = []
                try:
                    inner_div = inner_soup.find_all('a', attrs={'class': 'a10a3f92e9--underground_link--AzxRC'})
                    for item in inner_div:
                        metroSt = item.text
                        metro_stations_list.append(metroSt)
                except AttributeError:
                    metro_stations_list = None

                # Обновляющаяся переменная для записи времени до станций метро
                time_to_metro_list = []
                try:
                    inner_div = inner_soup.find_all('span', attrs={'class': 'a10a3f92e9--underground_time--1fKft'})
                    for item in inner_div:
                        time_to_metro = item.text
                        time_to_metro_list.append(time_to_metro)
                except AttributeError:
                    time_to_metro_list = None

                # Цена
                try:
                    prc = None
                    inner_div = inner_soup.find_all('div', attrs={
                        'class': 'a10a3f92e9--price--1HD9F a10a3f92e9--price--residential--2ev_G'})
                    for item in inner_div:
                        prc = item.find('span', attrs={'class': 'a10a3f92e9--price_value--1iPpd'}).text
                except AttributeError:
                    prc = None

                # Название объявлния
                try:
                    ttl = None
                    inner_div = inner_soup.find('div', attrs={'class': 'a10a3f92e9--container--fX4cE'})
                    for item in inner_div:
                        ttl = item.text.strip()
                except AttributeError:
                    ttl = None

                # Общая площадь
                try:
                    area = None
                    inner_div = inner_soup.find('div', attrs={'class': 'a10a3f92e9--description--3uuO6'})
                    for item in inner_div:
                        try:
                            area = item.find('div', text=re.compile("Общая")).find_parent('div', attrs={
                                'class': 'a10a3f92e9--info--3XiXi'}).text
                        except AttributeError:
                            pass
                except TypeError:
                    area = None

                # Этаж
                try:
                    flr = None
                    inner_div = inner_soup.find('div', attrs={'class': 'a10a3f92e9--description--3uuO6'})
                    for item in inner_div:
                        try:
                            flr = item.find('div', text=re.compile("Этаж")).find_parent('div', attrs={
                                'class': 'a10a3f92e9--info--3XiXi'}).text
                        except AttributeError:
                            pass
                except TypeError:
                    flr = None

                # Год постройки или сдачи дома
                try:
                    inner_div = inner_soup.find('div', attrs={'class': 'a10a3f92e9--description--3uuO6'})
                    cn_year = None
                    for item in inner_div:
                        try:
                            cn_year = item.find('div', text=re.compile("Срок")).find_parent('div', attrs={
                                'class': 'a10a3f92e9--info--3XiXi'}).text
                        except AttributeError:
                            pass
                        try:
                            cn_year = item.find('div', text=re.compile("Построен")).find_parent('div', attrs={
                                'class': 'a10a3f92e9--info--3XiXi'}).text
                        except AttributeError:
                            pass
                except TypeError:
                    cn_year = None

                # Тип жилья
                try:
                    accdn_type = None
                    inner_div = inner_soup.find('ul', attrs={'class': 'a10a3f92e9--list--2M4V-'})
                    for item in inner_div:
                        try:
                            accdn_type = item.find('span', text=re.compile('Тип жилья')).find_parent('li', attrs={
                                'class': 'a10a3f92e9--item--_ipjK'}).text
                        except AttributeError:
                            pass
                except TypeError:
                    accdn_type = None

                # Планировка
                try:
                    layout = None
                    inner_div = inner_soup.find('ul', attrs={'class': 'a10a3f92e9--list--2M4V-'})
                    for item in inner_div:
                        try:
                            layout = item.find('span', text=re.compile('Планировка')).find_parent('li', attrs={
                                'class': 'a10a3f92e9--item--_ipjK'}).text
                        except AttributeError:
                            pass
                except TypeError:
                    layout = None

                # Высота потолков
                try:
                    height = None
                    inner_div = inner_soup.find('ul', attrs={'class': 'a10a3f92e9--list--2M4V-'})
                    for item in inner_div:
                        try:
                            height = item.find('span', text=re.compile('Высота')).find_parent('li', attrs={
                                'class': 'a10a3f92e9--item--_ipjK'}).text
                        except AttributeError:
                            pass
                except TypeError:
                    height = None

                # Балкон / лоджия
                try:
                    blcn = None
                    inner_div = inner_soup.find('ul', attrs={'class': 'a10a3f92e9--list--2M4V-'})
                    for item in inner_div:
                        try:
                            blcn = item.find('span', text=re.compile('Балкон')).find_parent('li', attrs={
                                'class': 'a10a3f92e9--item--_ipjK'}).text
                        except AttributeError:
                            pass
                except TypeError:
                    blcn = None

                # Ремонт
                try:
                    renovation = None
                    inner_div = inner_soup.find('ul', attrs={'class': 'a10a3f92e9--list--2M4V-'})
                    for item in inner_div:
                        try:
                            renovation = item.find('span', text=re.compile('Ремонт')).find_parent('li', attrs={
                                'class': 'a10a3f92e9--item--_ipjK'}).text
                        except AttributeError:
                            pass
                except TypeError:
                    renovation = None

                # Ванная
                try:
                    inner_div = inner_soup.find('ul', attrs={'class': 'a10a3f92e9--list--2M4V-'})
                    bathroom = None
                    for item in inner_div:
                        try:
                            bathroom = item.find('span', text=re.compile('Санузел')).find_parent('li', attrs={
                                'class': 'a10a3f92e9--item--_ipjK'}).text
                        except AttributeError:
                            pass
                except TypeError:
                    bathroom = None

                # Вид из окна
                try:
                    view = None
                    inner_div = inner_soup.find('ul', attrs={'class': 'a10a3f92e9--list--2M4V-'})
                    for item in inner_div:
                        try:
                            view = item.find('span', text=re.compile('Вид')).find_parent('li', attrs={
                                'class': 'a10a3f92e9--item--_ipjK'}).text
                        except AttributeError:
                            pass
                except TypeError:
                    view = None

                try:  # пробует найти блок с информацией "О доме"
                    inner_div = inner_soup.find('div', attrs={'class': 'a10a3f92e9--column--2oGBs'})
                    # если находит, то пробует вернуть интересующий параметр, либо None

                    # Год постройки
                    cnstr_year = None
                    for item in inner_div:
                        try:
                            cnstr_year = item.find('div', text=re.compile('Год постройки')).find_parent('div',
                                                                                                        attrs={
                                                                                                            'class': 'a10a3f92e9--item--2Ig2y'}).text
                        except AttributeError:
                            pass
                    for item in inner_div:
                        try:
                            cnstr_year = item.find('div', text=re.compile('Сдача')).find_parent('div', attrs={
                                'class': 'a10a3f92e9--item--2Ig2y'}).text
                        except AttributeError:
                            pass

                    # Тип дома
                    h_type = None
                    for item in inner_div:
                        try:
                            h_type = item.find('div', text=re.compile('Тип дома')).find_parent('div', attrs={
                                'class': 'a10a3f92e9--item--2Ig2y'}).text
                        except AttributeError:
                            pass

                    # Тип перекрытий
                    flr_type = None
                    for item in inner_div:
                        try:
                            flr_type = item.find('div', text=re.compile('Тип перекрытий')).find_parent('div',
                                                                                                       attrs={
                                                                                                           'class': 'a10a3f92e9--item--2Ig2y'}).text
                        except AttributeError:
                            pass

                    # Подъезды
                    entrncs = None
                    for item in inner_div:
                        try:
                            entrncs = item.find('div', text=re.compile('Подъезды')).find_parent('div', attrs={
                                'class': 'a10a3f92e9--item--2Ig2y'}).text
                        except AttributeError:
                            pass

                    # Лифты
                    elvts = None
                    for item in inner_div:
                        try:
                            elvts = item.find('div', text=re.compile('Лифты')).find_parent('div', attrs={
                                'class': 'a10a3f92e9--item--2Ig2y'}).text
                        except AttributeError:
                            pass

                    # Отопление
                    htng = None
                    for item in inner_div:
                        try:
                            htng = item.find('div', text=re.compile('Отопление')).find_parent('div', attrs={
                                'class': 'a10a3f92e9--item--2Ig2y'}).text
                        except AttributeError:
                            pass

                    # Аварийность
                    emgc = None
                    for item in inner_div:
                        try:
                            emgc = item.find('div', text=re.compile('Аварийность')).find_parent('div', attrs={
                                'class': 'a10a3f92e9--item--2Ig2y'}).text
                        except AttributeError:
                            pass

                    # Парковка
                    prkng = None
                    for item in inner_div:
                        try:
                            prkng = item.find('div', text=re.compile('Парковка')).find_parent('div', attrs={
                                'class': 'a10a3f92e9--item--2Ig2y'}).text
                        except AttributeError:
                            pass

                    # Мусоропровод
                    g_chute = None
                    for item in inner_div:
                        try:
                            g_chute = item.find('div', text=re.compile('Мусоропровод')).find_parent('div', attrs={
                                'class': 'a10a3f92e9--item--2Ig2y'}).text
                        except AttributeError:
                            pass

                except TypeError:
                    cnstr_year = None
                    h_type = None
                    elvts = None
                    flr_type = None
                    entrncs = None
                    htng = None
                    emgc = None
                    prkng = None
                    g_chute = None

                # после сбора всех данных заносим их в словарь
                data_list.append({
                    'AnnouncementID': ancmnt_id,
                    'Title': ttl,
                    'Address': address_list,
                    'Lat': lat,
                    'Long': long,
                    'MetroStations': metro_stations_list,
                    'TimeToMetro': time_to_metro_list,
                    'ConstructionYear': cnstr_year,
                    'Price': prc,
                    'TotalArea': area,
                    'Floor': flr,
                    'Сonst/ComplYear': cn_year,
                    'AccommodationType': accdn_type,
                    'Layout': layout,
                    'CeilingHeight': height,
                    'Balconies': blcn,
                    'Renovation': renovation,
                    'Bathroom': bathroom,
                    'WindowView': view,
                    'HouseType': h_type,
                    'FloorType': flr_type,
                    'Entrances': entrncs,
                    'Elevators': elvts,
                    'Heating': htng,
                    'Emergency': emgc,
                    'Parking': prkng,
                    'GarbageChute': g_chute
                })

                # записываем данные по объявлению в таблицу
                file_writer(data_list)


# Функция, вызываю внутри себя выполнение асинхронного парсинга содержимого объявлений
async def main(coords_and_ids):
    dt_start = datetime.now()
    try:
        for i in range(0, len(coords_and_ids), 30):
            j = i + 30
            tasks = []
            async with aiohttp.ClientSession() as session:
                print(f'Time gone {str(datetime.now() - dt_start)}, {i} announcements collected')
                for item_num in range(i, j):
                    user = fake_useragent.UserAgent().random
                    headers = {'accept': '*/*',
                               'user-agent': user}
                    tasks.append(
                        asyncio.create_task(
                            one_page_parser(coords_and_ids[item_num], headers)
                        )
                    )
            await asyncio.gather(*tasks)
    except IndexError:
        pass
    print(f'Ended in {str(datetime.now() - dt_start)}')


coords_and_ids = parse_coords_and_ids()
asyncio.run(main(coords_and_ids))