import os, shlex, db_connection as db, query_redcap as rc, password as pwd, send_email as se, pandas as pd
import config.constants as cst
from smtplib import SMTPServerDisconnected

# this function check if submission is new or not
# @input rc_record (list)
# @input output_dir (string; output folder)
# @return TRUE if submission is new and FALSE if submission it not a new one i.e. it has been processed or in the middle of processing
#
def is_submission_new(rc_record, output_dir):
    # check to see if folder exists
    record_id = rc_record['record_id']
    return not os.path.isdir(os.path.join(output_dir,"submission",str(record_id)))


# QC input file
#
# @input template_fname: location of template file (contains the probe names)
# @input input_fname: location of input data file from user
#
# @return tuple: QC status (T/F), error_msg (string containing info about the error(s) encountered)
def qc_input(template_fname, input_fname):
    # testing
    template_fname = cst.input_template_fname

    template = pd.read_csv(template_fname, delimiter='\t')
    input_data = pd.read_csv(input_fname, delimiter='\t')

    # initialize error message
    error_msg = ""

    # make sure all probes are presents
    input_probes = set(input_data.iloc[:,0])
    all_probes = set(template.iloc[:,0])
    missing_probes = all_probes - input_probes

    if len(missing_probes)>0:
        error_msg = error_msg + "\nThe following probes are MISSING from input file:"
        for i in missing_probes:
            error_msg = error_msg +"\n    "+i
        error_msg = error_msg + "\n"

    return (len(error_msg)==0, error_msg)

# send email to user with error message
#
# @input app_title - title of app
# @input err_msg - the actual error message/content
# @input user_email - user's email address
# @input email_server - email server
#
# @return null
def send_failed_email(app_title, err_msg, user_email, email_server):
    email_subject = app_title+" - error encountered."
    email_body = "Thank you for submitting your data to the "+app_title+" for analysis.  The following error(s) was detected in the input file.  Please kindly check your data file and re-submit."
    email_body = email_body + "\n\n" + err_msg
    se.send_email(email_subject, email_body, cst.mapcore_email, user_email, email_server)

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
        email_server = se.connect_to_email_server(cst.smtp_server_url,cst.smtp_server_port,pwd.smtp_user,pwd.smtp_password)

        # 1. create folder
        if not os.path.exists(os.path.join(output_dir,"submission")):
            os.mkdir(os.path.join(output_dir,"submission"))
        os.mkdir(os.path.join(output_dir,"submission",str(record_id)))

        # 2a. download file and store in folder
        record_output_dir = os.path.join(output_dir,"submission",str(record_id))
        # note: we change file name since user may upload file name with spaces or special character
        # that would create issues with os.system()
        input_fname = os.path.join(record_output_dir,"input.txt") # rc_record['data_file'])
        rc.get_rc_file(\
            record_id, \
                api_url, \
                    api_token, \
                        input_fname)

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
        
        
        # REDCap will send confirmation email to user indicating that their files are received and will be processed
        # nothing to do here

        # 3. check to make sure file format is correct e.g. all required probe names are present
        qc_result = qc_input(cst.input_template_fname,input_fname)
        if not qc_result[0]:
            # failed QC
            # 5. email user back the results
            send_failed_email(app_title, qc_result[1],user_email,email_server)
        else:
            # 4. run classifier code
            classifier_py_fname = os.path.join(cst.WORKING_FOLDER,"classifier","classifier_wrapper.py")
            probe_fname = os.path.join(cst.WORKING_FOLDER,"data","selected_probes.txt")
            nn_fname = os.path.join(cst.WORKING_FOLDER,"data","nn_state.pt")
            out_fname = os.path.join(record_output_dir,"output.tsv")
            input_fname = input_fname
            sys_cmd = cst.PYTHON_EXE + " " + classifier_py_fname + " -i " + input_fname + " -s " + probe_fname + " -n " + nn_fname + " -o " + out_fname
            print(sys_cmd)
            return_code = os.system(sys_cmd)
            if return_code !=0:
                # error encountered.
                err_msg = "\n*** error log ***"
                err_fname = os.path.join(record_output_dir,"validation_errors.log")
                err_f = open(err_fname,mode="r")
                for l in err_f.readlines():
                    err_msg = err_msg+"\n"+l
                send_failed_email(app_title, err_msg, user_email,email_server)
            else:
                # 5. email user back the results
                email_subject = app_title+" - analysis result attached."
                email_body = "Thank you for submitting your data to the "+app_title+" for analysis.  Your analysis result is attached."
                se.send_email(email_subject,email_body,cst.mapcore_email,user_email,email_server,out_fname)

        ### cleanup ###
        # disconnect from email server
        try:
            se.disconnect_email_server(email_server)
        except SMTPServerDisconnected:
            # ignore error since email was sent already
            print("SMTPServerDisconnected encountered.")

if __name__ == '__main__':
    import pandas as pd, os
    os.chdir("C:\\Users\\samleung\\Documents\\workspace-py\\lung_classifier_daemon\\src")
    import config.constants as cst
   
    input_fname = "G:\\MAPcore\\jira\\mapcore-1588\\2024-09-15_allen\\input_beta_example_BAD.txt"
    result = qc_input(cst.input_template_fname,input_fname)
    print(result[1])
