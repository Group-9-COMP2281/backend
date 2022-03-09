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

# Shorten list for testing
uni_list = uni_list[:38:]

uni_list = [x.lower().strip() for x in uni_list]

tweet_unis = {}
all_tweets = []
counter = 0

# Run a search for each different university
for uni in uni_list:
    c.Search = 'IBM university ("' + uni + '") -filter:replies'
    twint.run.Search(c)
    # Get the last-added tweets
    new_tweets = twint.output.tweets_list[counter::]

    for tweet_object in new_tweets[:]:
        if tweet_object.id_str not in tweet_unis:
            tweet_unis[tweet_object.id_str] = [uni]

        # If tweet already exists because of mention of another uni name
        else:
            # Append current uni name to list of uni names of this tweet
            tweet_unis[tweet_object.id_str].append(uni)
            new_tweets.remove(tweet_object)
    
    all_tweets += new_tweets
    
    # Update counter to length of entire list, to be able to slice from this point in the next loop
    counter = len(twint.output.tweets_list)

conn = mysql.connect()
h = handler.DatabaseHandler(conn)

# Uncomment if you want to delete all rows in Post and University table before adding new rows
#h.delete_all_posts()
#h.delete_all_universities()

for tweet_object in all_tweets:
    p = post.TwitterPost(tweet_object.id_str, tweet_object.username, tweet_object.tweet, tweet_object.datestamp,
                            datetime.datetime.now(), tweet_object.link)

    post_id = h.insert_post(p)

    for uni_name in tweet_unis[tweet_object.id_str]:
        h.insert_university(uni_name, post_id)
h.close()

print("Data committed")
