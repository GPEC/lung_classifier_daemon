# set constants

# read REDCap tokens
RC_TOKEN_FNNAME = "C:\\Users\\samleung\\Documents\\workspace-py\\REDCAP_TOKENS.csv"
rc_token_d = pd.read_csv(RC_TOKEN_FNNAME)
API_TOKEN = rc_token_d.query("server=='https://dev.rc.med.ubc.ca/' and pid==1089")['token']
RC_API_URL = "https://dev.rc.med.ubc.ca/redcap/api/"

MONITOR_TIME_INTERVAL_SEC = 300

# output folder
# - folder for downloading files, storing result files
OUTPUT_DIR = "C:\\Users\\samleung\\Downloads\\lung_classifier_daemon\\"