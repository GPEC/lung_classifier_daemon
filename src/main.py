# lung classifier daemon
import os, time, logging #, importlib
from datetime import datetime

# some constants - SERVER-SPECIFIC / NEED UPDATE
WORKING_FOLDER = "C:\\Users\\samleung\\Documents\\workspace-py\\lung_classifier_daemon\\src"

# set working directory:
os.chdir(WORKING_FOLDER) 

# locally defined library functions
import config.constants as cst, query_redcap as rc, db_connection as db, ProcessSubmissionThread as pst
# to manually/force reload library ... importlib.reload(rc)

# iterate through all rows in rc_d and check if it represents a new submission
# while file STOP_ME.txt does NOT exist
#   for i in rows of rc_d
#     get record_id
#     if folder with name=record_id does NOT exist
#        this is a new submission ...
#        - create folder
#        - create thread to process submission

logging.basicConfig(
        filename=os.path.join(cst.DATA_FOLDER,"log_"+(datetime.today().strftime("%Y-%m-%d"))+".txt"),
        filemode='a',  # Append to existing log
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

while not os.path.isfile(os.path.join(cst.DATA_FOLDER,"STOP_ME.txt")):
    # query redcap
    logging.info("query redcap ...")
    all_rc_records = rc.get_rc_status(cst.RC_API_URL, cst.API_TOKEN, cst.MONITOR_TIME_INTERVAL_SEC)

    # iterate all rows in rc_d
    for rc_record in all_rc_records:
        thread = pst.ProcessSubmissionThread(rc_record, cst.RC_API_URL, cst.API_TOKEN, cst.SQLITE_FNAME, cst.OUTPUT_DIR)
        thread.start()
        
    # sleep for MONITOR_TIME_INTERVAL_SEC 
    #print(datetime.now(),end=" ")
    logging.info("sleeping for "+str(cst.MONITOR_TIME_INTERVAL_SEC)+" seconds ...")
    time.sleep(cst.MONITOR_TIME_INTERVAL_SEC)


logging.info("daemon stopped.  bye.")