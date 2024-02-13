import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# filenames = ['1001_0005', '1001_0006', '1001_0012', '1001_0013', '1001_0014']
root_dir = Path('dataset/drone_dataset/Drone_data_processed/processed')

file_list = root_dir.glob('maneuver_index/*.npy')

maneuvers = np.zeros(shape=4)

for file in file_list:
    filename = file.name
    conversion = np.load(root_dir / 'conversion' / filename)

    # index for maneuver table
    link_idx = np.load(root_dir / 'link_idx' / filename)

    # [others, LLC, LK, RLC]
    maneuver_index = np.load(root_dir / 'maneuver_index' / filename)

    # state from trajectory nearest to outlet
    nearest_outlet_state = np.load(root_dir / 'nearest_outlet_state' / filename)

    # intersection outlet node
    outlet_node_state = np.load(root_dir / 'outlet_node_state' / filename)
    
    # trajectories
    total_traj = np.load(root_dir / 'total_traj' / filename)

    outlet_index = np.where(total_traj[:, 0] == nearest_outlet_state[0, 0])[0][0]
    mod_traj = total_traj[:outlet_index + 1, :]

    maneuvers = maneuvers + maneuver_index

    plt.plot(total_traj[:, 0], total_traj[:, 1])
    plt.plot(mod_traj[:, 0], mod_traj[:, 1], 'r')
    plt.scatter(outlet_node_state[:, 0], outlet_node_state[:, 1], color='b')

print('Done')
