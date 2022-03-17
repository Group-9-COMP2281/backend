import atexit
import threading

import flask
import waitress
from flask import Flask
from flask import request
from flaskext.mysql import MySQL

import config
import scraper
from data import handler
from scraper import Scraper


def create():
    app = Flask(__name__)
    app.config.from_object(config.get_config('default'))

    mysql = MySQL()
    mysql.init_app(app)

    conn = mysql.connect()
    h = handler.DatabaseHandler(conn)

    scrape_thread = None
    thread_time = 600  # ten minutes

    def scrape():
        global scrape_thread

        s = Scraper()
        posts = s.run_searches(scraper.uni_list)

        h.insert_posts(posts, commit=True)

        scrape_thread = threading.Timer(thread_time, scrape, ())
        scrape_thread.start()

    def interrupt():
        scrape_thread.cancel()

    scrape_thread = threading.Timer(thread_time, scrape, ())
    scrape_thread.start()

    atexit.register(interrupt)

    @app.route('/api/engagements', methods=['GET'])
    def engagements():
        min_id = request.args.get('min_id', type=int, default=-1)

        posts = [x.to_json() for x in h.get_posts_where(min_id=min_id)]
        return flask.jsonify({'posts': posts})

    @app.after_request
    def add_headers(response):
        response.headers.add('Access-Control-Allow-Origin', '*')

        return response

    return app
