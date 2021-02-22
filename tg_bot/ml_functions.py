import pandas as pd
import numpy as np
from geopy.distance import geodesic
import joblib
import xgboost as xgb
from additional_ml_functions import get_azimuth, get_addres_coords, get_feature_names


def make_one_prediction(data):
    city_center_coordinates = [55.7522, 37.6156]
    address = f'Москва,{data.get("address")}'
    lat, long = get_addres_coords(address)
    distance = geodesic(city_center_coordinates, [lat, long]).meters
    azimuth = get_azimuth(lat, long)
    TotalArea = data.get('total_area')
    NumOfRooms = data.get('numofrooms')
    WalkAccess = data.get('walkmetroaccess')
    ConstrYear = data.get('constryear')
    AccomType = data.get('accomtype')
    RenovType = data.get('renovtype')
    FloorNum = data.get('floornum')
    FloorAmnt = data.get('flooramnt')

    flat_dict = {
        'Lat': lat,
        'Long': long,
        'TotalArea': TotalArea,
        'distance': distance,
        'azimuth': azimuth,
        'NumOfRooms': NumOfRooms,
        'WalkAccess': WalkAccess,
        'ConstrYear': ConstrYear,
        'AccomType': AccomType,
        'RenovType': RenovType,
        'FloorNum': FloorNum,
        'FloorAmnt': FloorAmnt
    }
    try:
        one_apartment = pd.DataFrame(flat_dict, index=[0])
        one_apartment['TotalArea'] = one_apartment['TotalArea'].str.replace(',', '.').astype(float)
        one_apartment['NumOfRooms'] = one_apartment['NumOfRooms'].astype(int)
        one_apartment['ConstrYear'] = one_apartment['ConstrYear'].astype(int)
        one_apartment['FloorNum'] = one_apartment['FloorNum'].astype(int)
        one_apartment['FloorAmnt'] = one_apartment['FloorAmnt'].astype(int)

        prod_pipe = joblib.load('prod_pipeline_file')
        XGB_best_reg = xgb.XGBRegressor()
        XGB_best_reg.load_model('XGB_best_reg.json')

        one_apartment_transformed = prod_pipe.transform(one_apartment)
        column_names = get_feature_names(prod_pipe[0])
        transformed_df = pd.DataFrame(one_apartment_transformed, columns=column_names)
        point_prediction = XGB_best_reg.predict(transformed_df)
        point_norm_pred = np.floor(np.expm1(point_prediction))
        point_norm_pred = point_norm_pred[0]
    except ValueError:
        point_norm_pred = '"Ошибка. Какие-то данные были введены некорректно"'

    return point_norm_pred




