import matplotlib.pyplot as plt
from pathlib import Path
import pandas as pd
import numpy as np
import shapely
import os

raw_data_dir = Path('dataset/drone_dataset/Drone_data_raw/raw')

scene_list = raw_data_dir.glob('landmark/*.csv')

unit = 'meters' # meter


def bounding_box(x_center, y_center, heading_deg, length, width, px2meter):
    heading_rad = np.pi * heading_deg / 180
    length_cos = 0.5 * length * np.cos(heading_rad)
    length_sin = 0.5 * length * np.sin(heading_rad)
    width_cos = 0.5 * width * np.cos(heading_rad)
    width_sin = 0.5 * width * np.sin(heading_rad)
 
    pos1 = np.array([x_center - length_cos - width_sin, y_center - length_sin + width_cos]) / px2meter
    pos2 = np.array([x_center - length_cos + width_sin, y_center - length_sin - width_cos]) / px2meter
    pos3 = np.array([x_center + length_cos + width_sin, y_center + length_sin - width_cos]) / px2meter
    pos4 = np.array([x_center + length_cos - width_sin, y_center + length_sin + width_cos]) / px2meter

    return shapely.Polygon((pos1, pos2, pos3, pos4))

tot_stat = []

for scene_landmark in scene_list:

    # scene_stat = []

    fig, ax = plt.subplots(1, 1)

    scene_id = scene_landmark.name.split('_')[0]

    landmarks = pd.read_csv(scene_landmark)
    frame_list = landmarks['frame'].dropna().to_list()
 
    tracks = pd.read_csv(raw_data_dir / f'tracks/{scene_id}_tracks.csv')
    tracks_meta = pd.read_csv(raw_data_dir / f'tracksMeta/{scene_id}_trackMeta.csv')
    tot_stat.append(tracks_meta['class'].value_counts())

    fname = [f for f in os.listdir(raw_data_dir / 'mapSegmentation/') if scene_id in f][0]
    map_seg = pd.read_csv(raw_data_dir / f'mapSegmentation/{fname}')

    ped_ids = tracks_meta.loc[tracks_meta['class'] == 'pedestrian']
    parked_car_ids = tracks_meta.loc[tracks_meta['class'] == 'parked car']
    car_ids = tracks_meta.loc[tracks_meta['class'] == 'car']
    bicycle_ids = tracks_meta.loc[tracks_meta['class'] == 'bicycle']

    recording_meta = pd.read_csv(raw_data_dir / f'recordingMeta/{scene_id}_recordingMeta.csv')
    px2meter = recording_meta['px2meter'][0]

    if unit == 'pixel':
        scale = px2meter
    elif unit == 'meters':
        scale = 1.0

    # Draw lane segments
    for col_index in np.arange(0, len(map_seg.columns), 2):
        segment_type = map_seg.columns[col_index].split('_')[0]
        x_col = map_seg.iloc[:, col_index].dropna().to_numpy() # pixel
        y_col = map_seg.iloc[:, col_index+1].dropna().to_numpy() # pixel
        ax.fill(x_col*px2meter/scale, -y_col*px2meter/scale, color='magenta' if segment_type == 'intersection' else 'grey', alpha=0.5)

    # Draw tracked objects
    for frame in frame_list:
        frame_idx = int(frame.split('_')[1])

        rows_in_frame = tracks.loc[tracks['frame'] == frame_idx]

        peds_in_frame = rows_in_frame[rows_in_frame['trackId'].isin(ped_ids['trackId'])]
        parked_cars_in_frame = rows_in_frame[rows_in_frame['trackId'].isin(parked_car_ids['trackId'])]
        cars_in_frame = rows_in_frame[rows_in_frame['trackId'].isin(car_ids['trackId'])]
        bicycles_in_frame = rows_in_frame[rows_in_frame['trackId'].isin(bicycle_ids['trackId'])]

        # bicycle and pedestrians
        ped_x, ped_y = peds_in_frame['xCenter'].to_numpy()/scale, peds_in_frame['yCenter'].to_numpy()/scale
        bic_x, bic_y = bicycles_in_frame['xCenter'].to_numpy()/scale, bicycles_in_frame['yCenter'].to_numpy()/scale

        ax.scatter(ped_x, ped_y, color='green')
        ax.scatter(bic_x, bic_y, color='orange')
        
        # cars
        for idx, car in cars_in_frame.iterrows():
            heading_deg = car['heading'] # degree
            x_pos = car['xCenter'] # meters
            y_pos = car['yCenter'] # meters

            length = car['length'] # meters
            width = car['width'] # meters

            car_bb = bounding_box(x_pos, y_pos, heading_deg, length, width, scale)
            # ax.fill(*car_bb.exterior.xy, color='blue', alpha=0.2)

        # parked cars
        for idx, p_car in parked_cars_in_frame.iterrows():
            heading_deg = p_car['heading'] # degree
            x_pos = p_car['xCenter'] # meters
            y_pos = p_car['yCenter'] # meters

            length = p_car['length'] # meters
            width = p_car['width'] # meters

            print('parked car available!')
            p_car_bb = bounding_box(x_pos, y_pos, heading_deg, length, width, scale)
            # ax.fill(*p_car_bb.exterior.xy, color='cyan', alpha=0.5)


    # plt.axis('equal')
    # plt.show()
tot_stat = pd.concat(tot_stat, axis=1).fillna(value=0)
print('done')