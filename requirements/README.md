## This folder contains requirements and environments files to get the Kivy app running on any machine with Python

## Run with a Conda environment
If you have Anaconda or Miniconda installed and you use Conda to manage your packages and virtual environments, then you can simply create a new environment that has all the Kivy requirements:
* `conda env create -f kivy-development.yml`
* `conda activate kivy-development`
* `conda list` to see all the libraries installed to your Conda environment
* Then navigate to the directory that you cloned. It should be named "Kivy-Game"
* Run `python main.py`

## Run with Pipenv
If you use Pipenv then you can use the requirements.txt file included to run the Kivy app
* Clone this repo to get a directory called "Kivy-Game"
* Nagivate to that folder
* In your terminal, run `pipenv install -r requirements/requirements.txt`

This will create a new Pipenv environment named "Kivy-Game" which is the name of your current directory
* Run `pipenv shell` while you are still in "Kivy-Game" directory to activate the virtual environment
* Then simply run `python main.py` to run the game
