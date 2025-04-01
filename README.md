# Lung Classifier Daemon
Software daemon for monitoring and executing lung classifier codes

REDCap url: https://redcap.link/squamous_cell_carcinomas_classifier

Python codes


The software daemon assumes the following folder structure

[home directory]
|-src
|   |-config
|-main.py (code entry poit)

[data directory] - these contains data/config files .. DO NOT push to github
|-REDCAP_TOKEN.csv
|-data (contains probe list and saved neural net model)
|-user_data (contains user input files as well as the output/result files)
|   - lcd.sqlite (database to store user input)