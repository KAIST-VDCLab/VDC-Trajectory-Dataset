# Beyond the Data Imbalance: Employing the Heterogeneous Datasets for Vehicle Maneuver.

This page contains the drone dataset used in our paper: Beyond the Data Imbalance: Employing the
Heterogeneous Datasets for Vehicle Maneuver

<!-- ![Continuous integration](https://github.com/waymo-research/waymax/actions/workflows/ci-build.yml/badge.svg)
[![arXiv](https://img.shields.io/badge/cs.RO-2310.08710-b31b1b?logo=arxiv&logoColor=red)](https://arxiv.org/abs/2310.08710) -->

[**Paper**](paperlink)
| [**Documentation**](https://waymo-research.github.io/waymax/docs/)
| [**Download**](downloadpage)
| [**Tutorials**](https://waymo-research.github.io/waymax/docs/getting_started.html)

## Contents
1. [Overview](#overview)
2. [Getting Started](#getting-started)
3. [Dataset Information](#dataset-information)
## Overview

Drone dataset captured over several intersections in Daejeon, South Korea

## Getting Started


### Download

You can download the dataset from the releases page. Extract the zip files and make sure the dataset directory structure is as follows:

```
data_root
- processed
    - conversion
    - link_idx
    - maneuver_index
    - nearest_outlet_state
    - outlet_node_state
    - total_traj
    - plots
    - folder_tree
- raw
    - background
    - landmark
    - mapSegmentation
    - recordingMeta
    - segmentation
    - tracks
    - tracksMeta
```

### Examples

Please take a look at the colab files for examples on how to use the dataset

## Dataset Information

### Statistics

## Cite

If you found this drone dataset or our paper helpful for your own research, please cite:

```
cite
```