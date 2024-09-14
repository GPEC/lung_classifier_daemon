# thread class to process submission
import threading, process_submission as ps, db_connection as db

class ProcessSubmissionThread(threading.Thread):

    # class initializer
    #
    # @input rc_record (list)
    # @input api_url
    # @input api_token
    # @input database filename
    # @input output_dir (string; output folder)
    # @return null
    def __init__(self, rc_record, api_url, api_token, sqlite_fname, output_dir):
        super().__init__()
        self.rc_record=rc_record
        self.api_url=api_url
        self.api_token=api_token
        self.sqlite_fname=sqlite_fname
        self.output_dir=output_dir

    # main function to process submission
    def run(self):
        # create or load database
        conn = db.create_or_load_db(self.sqlite_fname)

        ps.process_submission(self.rc_record, self.api_url, self.api_token, conn, self.output_dir)

        # close database connection
        conn.close()