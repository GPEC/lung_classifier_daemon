# lung classifier daemon
import os, time, pandas as pd

# set working directory:
os.chdir("C:\\Users\\samleung\\Documents\\workspace-py\\lung_classifier_daemon\\src")

# load config
exec(open("config\\constants.py").read())

# load function to query redcap
exec(open("query_redcap.py").read())

# iterate through all rows in rc_d and check if it represents a new submission
# while file STOP_ME.txt does NOT exist
#   for i in rows of rc_d
#     get record_id
#     if folder with name=record_id does NOT exist
#        this is a new submission ...
#        - create folder
#        - create thread to process submission

while not os.path.isfile(os.path.join(OUTPUT_DIR+"STOP_ME.txt")):
    # query redcap
    print("query redcap ...")
    all_rc_records = get_rc_status()

    # iterate all rows in rc_d
    for rc_record in all_rc_records:
        record_id = rc_record["record_id"]

    # sleep for 5 min
    print("go back to sleep")
    time.sleep(MONITOR_TIME_INTERVAL_SEC)


# process submission
# create a thread to do the processing


# email response