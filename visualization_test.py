import matplotlib.pyplot as plt
from pathlib import Path
import pandas as pd
import numpy as np
import glob
import shapely
import os

raw_data_dir = Path('dataset/drone_dataset/Drone_data_raw/raw')

scene_list = raw_data_dir.glob('landmark/*.csv')


def bounding_box(x_center, y_center, heading_deg, length, width, px2meter):
    heading_rad = np.pi * heading_deg / 180
    length_cos = 0.5 * length * np.cos(heading_rad)
    width_cos = 0.5 * width * np.cos(heading_rad)
    length_sin = 0.5 * length * np.sin(heading_rad)
    width_sin = 0.5 * width * np.sin(heading_rad)
 
    pos1 = np.array([x_center - length_cos - width_sin, y_center - length_sin + width_cos]) / px2meter
    pos2 = np.array([x_center - length_cos + width_sin, y_center - length_sin - width_cos])/ px2meter
    pos3 = np.array([x_center + length_cos + width_sin, y_center + length_sin - width_cos])/ px2meter
    pos4 = np.array([x_center + length_cos - width_sin, y_center + length_sin + width_cos])/ px2meter

    return shapely.Polygon((pos1, pos2, pos3, pos4))


fig, ax = plt.subplots(1, 1)

for scene_landmark in scene_list:
    scene_id = scene_landmark.name.split('_')[0]

    landmarks = pd.read_csv(scene_landmark)
    frame_list = landmarks['frame'].to_list()
 
    tracks = pd.read_csv(raw_data_dir / f'tracks/{scene_id}_tracks.csv')
    tracks_meta = pd.read_csv(raw_data_dir / f'tracksMeta/{scene_id}_trackMeta.csv')

    fname = [f for f in os.listdir(raw_data_dir / 'mapSegmentation/') if scene_id in f][0]
    map_seg = pd.read_csv(raw_data_dir / f'mapSegmentation/{fname}')

    ped_ids = tracks_meta.loc[tracks_meta['class'] == 'pedestrian']
    parked_car_ids = tracks_meta.loc[tracks_meta['class'] == 'parked car']
    car_ids = tracks_meta.loc[tracks_meta['class'] == 'car']
    bicycle_ids = tracks_meta.loc[tracks_meta['class'] == 'bicycle']

    recording_meta = pd.read_csv(raw_data_dir / f'recordingMeta/{scene_id}_recordingMeta.csv')
    px2meter = recording_meta['px2meter'][0]


    for col_index in np.arange(0, len(map_seg.columns), 2):
        x_col = map_seg.iloc[:, col_index].dropna().to_numpy() 
        y_col = map_seg.iloc[:, col_index+1].dropna().to_numpy() 
        ax.scatter(x_col, -y_col, color='black')

    for frame in frame_list:
        frame_idx = int(frame.split('_')[1])

        rows_in_frame = tracks.loc[tracks['frame'] == frame_idx]

        peds_in_frame = rows_in_frame[rows_in_frame['trackId'].isin(ped_ids['trackId'])]
        parked_cars_in_frame = rows_in_frame[rows_in_frame['trackId'].isin(parked_car_ids['trackId'])]
        cars_in_frame = rows_in_frame[rows_in_frame['trackId'].isin(car_ids['trackId'])]
        bicycles_in_frame = rows_in_frame[rows_in_frame['trackId'].isin(bicycle_ids['trackId'])]

        ax.scatter(peds_in_frame['xCenter'].to_numpy() / px2meter, peds_in_frame['yCenter'].to_numpy() / px2meter, color='green')
        ax.scatter(bicycles_in_frame['xCenter'].to_numpy() / px2meter, bicycles_in_frame['yCenter'].to_numpy() / px2meter, color='orange')
        
        for idx, car in cars_in_frame.iterrows():
            heading_deg = car['heading'] # degree
            x_pos = car['xCenter'] # meters
            y_pos = car['yCenter'] # meters

            length = car['length'] # meters
            width = car['width'] # meters

            car_bb = bounding_box(x_pos, y_pos, heading_deg, length, width, px2meter)
            ax.fill(*car_bb.exterior.xy, color='blue', alpha=0.5)


        for idx, p_car in parked_cars_in_frame.iterrows():
            heading_deg = p_car['heading'] # degree
            x_pos = p_car['xCenter'] # meters
            y_pos = p_car['yCenter'] # meters

            length = p_car['length'] # meters
            width = p_car['width'] # meters

            p_car_bb = bounding_box(x_pos, y_pos, heading_deg, length, width, px2meter)
            ax.fill(*p_car_bb.exterior.xy, color='blue', alpha=0.5)

        break
    plt.axis('equal')
    plt.show()