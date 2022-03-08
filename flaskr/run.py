import datetime

import twint
from flask import Flask
from flaskext.mysql import MySQL

import config
from data import handler
from data.engagement import post

app = Flask(__name__)
app.config.from_object(config.get_config('dev'))  # todo dynamically load from command line

mysql = MySQL()
mysql.init_app(app)

c = twint.Config()
c.Limit = 20

c.Store_object = True
c.Hide_output = True

# Full list
uni_list = ['Aberdeen', 'Abertay', 'Aberystwyth', 'Anglia Ruskin', 'Aston', 'Bangor', 'Bath', 'Bath Spa',
            'Bedfordshire', 'Birmingham', 'Birmingham City', 'Bolton', 'Bournemouth', 'Bradford', 'Brighton', 'Bristol',
            'Brunel', 'Bucks New University', 'Cambridge', 'Canterbury Christ Church', 'Cardiff', 'Cardiff Met',
            'Central Lancashire', 'Chester', 'Chichester', 'City', 'Coventry', 'Cumbria', 'De Montfort', 'Derby',
            'Dundee', 'Durham', 'East London', 'Edge Hill', 'Edinburgh', 'Edinburgh Napier', 'Essex', 'Exeter',
            'Falmouth', 'Glasgow', 'Glasgow Caledonian', 'Gloucestershire', 'Glyndwr', 'Goldsmiths', 'Greenwich',
            'Heriot-Watt', 'Hertfordshire', 'Huddersfield', 'Hull', 'Imperial College', 'Keele', 'Kent',
            "King's College London", 'Kingston', 'Lancaster', 'Leeds', 'Leeds Beckett', 'Leeds Trinity', 'Leicester',
            'Lincoln', 'Liverpool', 'Liverpool Hope', 'Liverpool John Moores', 'London Met',
            'London School of Economics', 'London South Bank', 'Loughborough', 'Manchester', 'Manchester Met',
            'Middlesex', 'Newcastle', 'Newman', 'Northampton', 'Northumbria', 'Nottingham', 'Nottingham Trent',
            'Oxford', 'Oxford Brookes', 'Plymouth', 'Portsmouth', 'Queen Margaret', 'Queen Mary', "Queen's, Belfast",
            'Reading', 'Robert Gordon', 'Roehampton', 'Royal Holloway', 'Salford', 'Sheffield', 'Sheffield Hallam',
            'SOAS', 'Solent', 'South Wales', 'Southampton', 'St Andrews', "St Mary's, Twickenham", 'Staffordshire',
            'Stirling', 'Strathclyde', 'Suffolk', 'Sunderland', 'Surrey', 'Sussex', 'Swansea', 'Teesside',
            'Trinity Saint David', 'UCL', 'UEA', 'Ulster', 'University for the Creative Arts',
            'University of the Arts London', 'UWE Bristol', 'Warwick', 'West London', 'West of Scotland', 'Westminster',
            'Winchester', 'Wolverhampton', 'Worcester', 'York', 'York St John']
uni_list = [x.lower().strip() for x in uni_list]

# Shorten list for testing
uni_list = uni_list[:38:]

# Run a search for each different university
for uni in uni_list:
    c.Search = 'IBM university ("' + uni + '") -filter:replies'
    twint.run.Search(c)

h = handler.DatabaseHandler(mysql)
for tweet_object in twint.output.tweets_list:
    p = post.TwitterPost(tweet_object.id, tweet_object.username, tweet_object.tweet, tweet_object.datestamp,
                            datetime.datetime.now(), tweet_object.link)

    h.insert_post(p)

h.close()

print("Data committed")
