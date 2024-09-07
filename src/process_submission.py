# this function check if submission is new or not
# @input rc_record (list)
# @return TRUE if submission is new and FALSE if submission it not a new one i.e. it has been processed or in the middle of processing
#
def is_submission_new(rc_record):
    # check to see if folder exists
    record_id = rc_record['record_id']
    data_file_name = rc_record['data_file']
    if not os.path.isdir(os.path.join(OUTPUT_DIR,"submission",str(record_id))):
        # this is new submission
        # 1. create folder
        os.mkdir(os.path.join(OUTPUT_DIR,"submission",str(record_id)))
        # 2. download file and store in folder
        get_rc_file(record_id, os.path.join(OUTPUT_DIR,"submission",str(record_id),data_file_name))
        # 3. email user indicating that their files are received and will be processed
        # 4. run classifier code
        # 5. email user back the results
