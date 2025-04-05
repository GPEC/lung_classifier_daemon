# Lung Classifier Daemon
Software daemon for monitoring and executing lung classifier codes

REDCap url: https://redcap.link/squamous_cell_carcinomas_classifier

Python codes


The software daemon assumes the following folder structure

[home directory]
|-src
|   |-config
|   |-data (contains probe list and saved neural net model)
|-main.py (code entry poit)

[data directory] - these contains data/config files .. DO NOT push to github
|-REDCAP_TOKEN.csv
|-user_data (contains user input files as well as the output/result files)
|   - lcd.sqlite (database to store user input)



Setup needed for this software daemon:
- install the following packages: numpy, pandas, torch
- create and populate a file src/password.py
    - file content:
    
        smtp_user = [username for email server]

        smtp_password = [password to email server]
- update main.py and constants.py with the relevant folder paths
- create the following folders on the output folder e.g. 
    - C:\Users\samleung\Documents\workspace-py\lung_classifier_daemon_data\user_data
- make sure start_daemon.sh is exectuable
> chmod +x start_daemon.sh

Run daemon on Ubuntu
> ./start_daemon.sh

To run classifier manually e.g.
> python3 /mnt/c/Users/samle/Documents/workspace/py/lung_classifier_daemon/src/classifier/classifier_wrapper.py -i test
_data.tsv -s selected_probes.txt -n nn_state.pt

