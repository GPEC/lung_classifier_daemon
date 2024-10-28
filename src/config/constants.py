# set constants
import os, pandas as pd

# read REDCap tokens
RC_TOKEN_FNNAME = "C:\\Users\\samleung\\Documents\\workspace-py\\REDCAP_TOKENS.csv"
rc_token_d = pd.read_csv(RC_TOKEN_FNNAME)
API_TOKEN = rc_token_d.query("server=='https://rc.med.ubc.ca/' and pid==1423")['token'][1]
RC_API_URL = "https://rc.med.ubc.ca/redcap/api/"

MONITOR_TIME_INTERVAL_SEC = 3600*3 # 3 hours

# email related config
smtp_server_url = "smtp.mail.ubc.ca"
smtp_server_port = 587
mapcore_email = "map.core@ubc.ca"

# template input data file
input_template_fname = "data\\input_beta_example.txt"

# output folder
# - folder for downloading files, storing result files
OUTPUT_DIR = "C:\\Users\\samleung\\Downloads\\lung_classifier_daemon\\"
# name of SQLite database file (for storing info such as requestor names, emails)
SQLITE_FNAME = os.path.join(OUTPUT_DIR,"db","lcd.sqlite")