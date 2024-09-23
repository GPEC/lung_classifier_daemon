import os, db_connection as db, query_redcap as rc, password as pwd, send_email as se

# this function check if submission is new or not
# @input rc_record (list)
# @input output_dir (string; output folder)
# @return TRUE if submission is new and FALSE if submission it not a new one i.e. it has been processed or in the middle of processing
#
def is_submission_new(rc_record, output_dir):
    # check to see if folder exists
    record_id = rc_record['record_id']
    return not os.path.isdir(os.path.join(output_dir,"submission",str(record_id)))


# main function to process submission
#
# @input rc_record (list)
# @input api_url
# @input api_token
# @input database connection
# @input output_dir (string; output folder)
# @return null
def process_submission(rc_record, api_url, api_token, conn, output_dir):
    app_title = "Methylation Classifier for Squamous Cell Carcinoma Site of Origin"

    if is_submission_new(rc_record, output_dir):
        record_id = rc_record['record_id']

        ### setup ###
        # connect to email server
        smtp_user = "samuel.leung@ubc.ca"
        email_server = se.connect_to_email_server("smtp.mail.ubc.ca",587,pwd.smtp_user,pwd.smtp_password)

        # 1. create folder
        os.mkdir(os.path.join(output_dir,"submission",str(record_id)))

        # 2a. download file and store in folder
        rc.get_rc_file(\
            record_id, \
                api_url, \
                    api_token, \
                        os.path.join(output_dir,"submission",str(record_id),rc_record['data_file']))

        # 2b. save info: name, email address, record_id
        if db.record_exists(conn,rc_record):
            raise Exception("Record exist in database already:"+record_id)
        
        user_email = rc_record["user_email"]
        sql_stm = "INSERT INTO rc_record (record_id,last_name,first_name,email) VALUES("+\
            record_id+",'"+\
                rc_record['last_name']+"','"+\
                    rc_record["first_name"]+"','"+\
                        user_email+"')"
        db.sql(conn,sql_stm)
        
        
        # 3. REDCap will send confirmation email to user indicating that their files are received and will be processed
        # nothing to do here

        # 4. run classifier code

        # 5. email user back the results
        email_subject = app_title+" - analysis result attached."
        email_body = "Thank you for submitting your data to the "+app_title+" for analysis.  Your analysis result is attached."
        se.send_email(email_subject,email_body,smtp_user,user_email,email_server)

        ### cleanup ###
        # disconnect from email server
        se.disconnect_email_server(email_server)
