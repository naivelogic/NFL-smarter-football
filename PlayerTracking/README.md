# NFL Player Detection and Tracking (real-time)

## Overview

__Objective:__ Using a camera running a tensorflow model locally,

1. __detect__ known objects from training set
2. __track__ detected object's location and assign unique identifier

The detection and tracking pipeline is straight forward:

- _Step 1:_ initialize detector and tracker
- _Step 2:_ the detector localized the object(s) in the real-time
- _Step 3:_ a tracking algorithm (Kalman Filter) uses detected object and updates with detection results
- _Step 4:_ the tracking results are annotated and display on video feed _(TODO:) and archived in database_

## Usage

### Setting Up Environment

1. Get python3 and Anaconda 
2. Clone Repository
3. cd to this directory 
4. _Install required packages_ Create a virtual environment via conda called `nfl`, using `./environment.yml`. This can be achieved by running the command: `conda env create --name nfl --file environment.yml`
5. Get models and put in `./models` folder

```commandline
$ cd ~/NFL-smarter-football/PlayerTracking
$ conda create env --name nfl --file environment.yml
$ conda activate nfl
$ 
```

run: `python main.py`



`git push -u origin player-tracking`