# To start up the application in terminal
	#export FLASK_APP=verify_sites
	#export FLASK_DEBUG=1
	#flask run

# To initialize the db in terminal
	#flask --app=flaskr initdb

# all the imports
import os
import psycopg2
import psycopg2.extras
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

# create our little application :)
app = Flask(__name__, static_url_path = "/static")
app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    SECRET_KEY='development key'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    """Connects to the specific database."""
    conn_string = "host='localhost' dbname='HomeDB' user='postgres' password='postgres'"
    conn = psycopg2.connect(conn_string)
    return conn

def init_db():
    db = get_db()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'psql_db'):
        g.psql_db = connect_db()
    return g.psql_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'psql_db'):
        g.psql_db.close()

@app.route('/')
def show_sites():
    db = get_db()
    rows = db.cursor('cursor_websites', cursor_factory=psycopg2.extras.DictCursor)
    sql = """SELECT
                 url,
                 status_code,
                 save_as
             FROM
                 usfcw.site_status
             ORDER BY
                  url"""
    rows.execute(sql)
    return render_template('show_sites.html', rows=rows)

# UNCOMMENT THIS AND COMMENT FUNCTION BELOW IF YOU CHOOSE TO UPDATE ON CHANGE OF DROPDOWN
@app.route('/update', methods=['POST'])
def update_status():
    db = get_db()
    sql = 'update usfcw.site_status set status_code = \'%s\' where url = \'%s\'' % (request.form['input_status_code'], request.form['input_url'])
    cur_update = db.cursor()
    cur_update.execute(sql)

    db.commit()
    cur_update.close()

    return redirect(url_for('show_sites')+"#"+request.form['input_url'])

# UNCOMMENT THIS AND COMMENT FUNCTION ABOVE IF YOU CHOOSE TO BATCH UPDATE
"""@app.route('/update', methods=['POST'])
def update_status():
    db = get_db()
    rows = db.cursor('cursor_websites', cursor_factory=psycopg2.extras.DictCursor)
    sql = SELECT
                 url,
                 status_code
             FROM
                 usfcw.site_status
    rows.execute(sql)
    for idx, row in enumerate(rows):
        sql = 'update usfcw.site_status set status_code = \'%s\' where url = \'%s\'' % (request.form[row[0]], row[0])
        cur_update = db.cursor()
        cur_update.execute(sql)

    db.commit()
    cur_update.close()

    return redirect(url_for('show_sites'))"""




