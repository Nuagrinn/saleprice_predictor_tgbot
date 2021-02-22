import requests
import fake_useragent
from PointRectangleClasses import Rectangle, Point


def json_reader(json_data):
    coords_and_id = []

    # Script to take all coords and announcment's id
    data_list = list(json_data['data']['points'])

    for i in data_list:
        offers_list = list(json_data['data']['points'][i]['offers'])
        for k in range(0, len(offers_list)):
            coords_and_id.append([offers_list[k]['id'], i.split()])

    print(len(coords_and_id))
    return coords_and_id


user = fake_useragent.UserAgent().random
headers = {'accept': '*/*',
           'user-agent': user}


def make_cian_map_req(header, req_num):
    genr = Rectangle(0.36, 0.57, Point(55.5550383110236, 37.32541797666712))
    r1 = Rectangle(0.0045, 0.0095, Point(55.5550383110236, 37.32541797666712))
    coords = r1.get_all_coords(genr)
    print(len(coords))
    all_idcoords_list = []
    for i in range(1, req_num):
        url = f'https://map.cian.ru/ajax/map/roundabout/?deal_type=sale&engine_version=2&object_type%5B0%5D=1&offer_type=flat&region=1&room1=1&room2=1&room3=1&room4=1&room5=1&room6=1&room7=1&room9=1' \
              f'&engine_version=2&in_polygon[0]={str(round(coords[i][0].lat, 6))}_{str(round(coords[i][0].long, 6))},{str(round(coords[i][1].lat, 6))}_{str(round(coords[i][1].long, 6))},{str(round(coords[i][2].lat, 6))}_{str(round(coords[i][2].long, 6))},' \
              f'{str(round(coords[i][3].lat, 6))}_{str(round(coords[i][3].long, 6))}&_=1466708040958'
        session = requests.Session()
        res = session.get(url, headers=header)
        if res.status_code == 200:
            json_data = res.json()
            if json_data["status"] == 'ok':
                temp_list = json_reader(json_data)
                if len(temp_list) != 0:
                    all_idcoords_list.extend(temp_list)
            else:
                print(url)
        else:
            print('Smth went wrong')
    print(len(all_idcoords_list))
    return all_idcoords_list


coordinates_list = make_cian_map_req(headers, 20)
