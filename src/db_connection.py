# helper functions related to database operations
#
import sqlite3

# execuite sql comments
# @input conn - database connection
# @sql_stm - SQL statement
#
def sql(conn, sql_stm):
    res = conn.execute(sql_stm)
    if sql_stm.startswith(("SELECT","select")):
        return res.fetchall()
    else:
        # assume this is some statement that needs commit e.g. INSERT, UPDATE
        conn.commit()
        return None

# create table to hold redcap record id, requestor's name and email address
# @input conn - database connection
# @return none
def create_rc_record(conn):
    sql(conn,"CREATE TABLE IF NOT EXISTS rc_record (record_id INTEGER NOT NULL, last_name VARCHAR, first_name VARCHAR, email VARCHAR NOT NULL, PRIMARY KEY(record_id))")

# create/initali or load database
# @input sqlite_fname name of SQLite file
# @return a database connection
#
# note: sqlite file will be created if it is not found
#
def create_or_load_db(sqlite_fname): 
    conn = sqlite3.connect(sqlite_fname)
    conn.execute('PRAGMA journal_mode=WAL;') # Enable WAL mode - allow concurrent write
    conn.commit()

    # create tables
    create_rc_record(conn)
    return conn

# check if REDCap record exist in database already
# @input rc_record
# @return TRUE if rc_record exists in database, FALSE otherwise
def record_exists(conn,rc_record):
    record_count = sql(conn,"select count(record_id) from rc_record where record_id='"+rc_record['record_id']+"'")[0][0]
    return record_count!=0