# Passes 

Scraping information on Swiss Alpine passes and their cycling routes from quaeldich.de.html, presenting them in an interactive map. 

## Contents 
0. Motivation
1. Installation
2. Usage
3. Comments on code
4. Improvements

## Motivation
My friend, who's a keen road cyclist loves planning his next cycling tour. It was an idea of his to create a personalised map whereby he can easily plan his next tour. This led to the creation of a map with passes and routes clearly identified, and taking into account his preferences e.g. no gravel paths. 

## Installation 

Recommend a virtual environment 
python3 -m venv venv
source venv/bin/activate (for MacOS)

and install these dependencies: 

pip install -r requirements.txt

## Usage 

Follow this step:

python3 run.py

## Comments on code 

- passes_parent.py parses first webpage listing all passes and routes, and passes_child.py parses the individual pass URLs.
- End output data collected in full_pass_data.json, intermediate data from passes_parent.py is in parent_data.json.
- In passes_child.py, ensures no gravel paths are included
- Information collected: 
	- Pass name (name)
	- URL of pass (url_pass)
	- Route name (route_name)
	- Review score (review_score)
	- Number of reviews (number_of_reviews)
	- Maximum elevation (elevation)
	- GPS coordinates (GPS)
	- URL of route (url_route)
	- Elevation gain (elevation_gain)
	- Average gradient (gradient)
	- URL of route profile GIF (url_gif)
         - If route is a dead end(deadend)
         - Length of route (length)
- Jupyter Notebook "Map.ipynb" creates a new json file which adds a "difficulty" statistic, difficulty = (elevation_gain * gradient) / 100 + length * 5. Saved as "passes_with_composite_difficulty.json". This json file outputs an interactive html map of the Swiss passes. 
- Any "archive" directories contain code no longer relevant to final outcomes. 

## Improvements

- Currently show all passes available with n=600 in URL. Edit this in case more passes are added, by automatically clicking "show more" at bottom of page 
- Extract GIF data (GPS coordinates) (attempted, see Jupyter Notebook in archive)
- Distance to next major town calculated
