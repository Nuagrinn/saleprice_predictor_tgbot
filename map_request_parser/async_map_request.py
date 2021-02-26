from PointRectangleClasses import Rectangle, Point
import aiohttp
import asyncio
import csv
from datetime import datetime
from crutch import crutch

crutch()

def read_json(json_data):
    flat_coords_and_id = []

    # Script to take all coords and announcment's id
    data_list = list(json_data['data']['points'])

    for i in data_list:
        offers_list = list(json_data['data']['points'][i]['offers'])
        for k in range(0, len(offers_list)):
            flat_coords_and_id.append([offers_list[k]['id'], i.split()])

    return flat_coords_and_id

async def make_cian_map_req(coords, item_num):
    try:
        ids_coords_fromsquare = []
        url = f'https://map.cian.ru/ajax/map/roundabout/?deal_type=sale&engine_version=2&object_type%5B0%5D=1&offer_type=flat&region=1&room1=1&room2=1&room3=1&room4=1&room5=1&room6=1&room7=1&room9=1' \
              f'&engine_version=2&in_polygon[0]={str(round(coords[item_num][0].lat, 6))}_{str(round(coords[item_num][0].long, 6))},{str(round(coords[item_num][1].lat, 6))}_{str(round(coords[item_num][1].long, 6))},{str(round(coords[item_num][2].lat, 6))}_{str(round(coords[item_num][2].long, 6))},' \
              f'{str(round(coords[item_num][3].lat, 6))}_{str(round(coords[item_num][3].long, 6))}&_=1466708040958'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    json_data = await response.json()
                    if json_data["status"] == 'ok':
                        temp_list = read_json(json_data)
                        if len(temp_list) != 0:
                            ids_coords_fromsquare.extend(temp_list)
                            print(len(ids_coords_fromsquare))
                    else:
                        print(url)
                else:
                    print('Smth went wrong')
        return ids_coords_fromsquare
    except IndexError:
        pass


async def request_gather(coords, i, j):
    tasks = []
    try:
        async with aiohttp.ClientSession() as session:
            for item_num in range(i, j):
                tasks.append(
                    asyncio.create_task(
                        make_cian_map_req(coords, item_num)
                    )
                )
    except IndexError:
        pass
    return await asyncio.gather(*tasks)


def make_cycled_async_request(rectangle_coords):
    all_coords_and_ids = []
    dt_start = datetime.now()
    for i in range(0, len(rectangle_coords), 30):
        j = i + 30
        all_coords_and_ids.extend(asyncio.run(request_gather(rectangle_coords, i, j)))
        print(f'Time gone: {[str(datetime.now() - dt_start)]}, Got rectangle #{j}')
    return all_coords_and_ids


def parse_coords_and_ids():
    genr = Rectangle(0.36, 0.57, Point(55.5550383110236, 37.32541797666712))
    r1 = Rectangle(0.0045, 0.0095, Point(55.5550383110236, 37.32541797666712))
    rectangle_coords = r1.get_all_coords(genr)
    print(f"Will request {len(rectangle_coords)} rectangles")

    nested_list_coords_and_id = make_cycled_async_request(rectangle_coords)
    all_coords_and_ids = []
    try:
        for i in nested_list_coords_and_id:
            all_coords_and_ids.extend(i)
    except TypeError:
        print(f"Guess that's all. Collected {len(all_coords_and_ids)} ids and coords")
        pass
    return all_coords_and_ids

