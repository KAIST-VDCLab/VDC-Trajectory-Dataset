import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


scene_ids = ['1001_0005', '1001_0006', '1001_0012', '1001_0013', '1001_0014']
root_dir = Path('dataset/drone_dataset/Drone_data_processed/processed')

for scene_id in scene_ids:
    conversion = np.load(root_dir / Path(f'conversion/{scene_id}.npy'))
    link_idx = np.load(root_dir / Path(f'link_idx/{scene_id}.npy'))
    maneuver_index = np.load(root_dir / Path(f'maneuver_index/{scene_id}.npy'))
    nearest_outlet_state = np.load(root_dir / Path(f'nearest_outlet_state/{scene_id}.npy'))
    outlet_node_state = np.load(root_dir / Path(f'outlet_node_state/{scene_id}.npy'))
    total_traj = np.load(root_dir / Path(f'total_traj/{scene_id}.npy'))
    plt.scatter(total_traj[:, 0], total_traj[:, 1])


print('Done')