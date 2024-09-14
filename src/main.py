# lung classifier daemon
import os, time #, importlib

# set working directory:
os.chdir("C:\\Users\\samleung\\Documents\\workspace-py\\lung_classifier_daemon\\src")

# locally defined library functions
import config.constants as cst, query_redcap as rc, db_connection as db, process_submission as ps
# to manually/force reload library ... importlib.reload(rc)

# create or load database
conn = db.create_or_load_db(cst.SQLITE_FNAME)

# iterate through all rows in rc_d and check if it represents a new submission
# while file STOP_ME.txt does NOT exist
#   for i in rows of rc_d
#     get record_id
#     if folder with name=record_id does NOT exist
#        this is a new submission ...
#        - create folder
#        - create thread to process submission

while not os.path.isfile(os.path.join(cst.OUTPUT_DIR+"STOP_ME.txt")):
    # query redcap
    print("query redcap ...")
    all_rc_records = rc.get_rc_status(cst.RC_API_URL,cst.API_TOKEN)

    # iterate all rows in rc_d
    for rc_record in all_rc_records:
        ps.process_submission(rc_record, cst.RC_API_URL, cst.API_TOKEN, conn, cst.OUTPUT_DIR)
        

    # sleep for 5 min
    print("go back to sleep")
    time.sleep(cst.MONITOR_TIME_INTERVAL_SEC)


# process submission
# create a thread to do the processing


# email response