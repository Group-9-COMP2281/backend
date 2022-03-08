from datetime import date
from flask import Flask
from flaskext.mysql import MySQL
import twint

app = Flask(__name__)
mysql = MySQL()
#I don't know if root will work for everyone but it worked for me (Rathin) because I created the db
app.config['MYSQL_DATABASE_USER'] = 'root'
#I assume this is the local mysql root/user password?
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'engagement-db'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_CHARSET'] = 'utf8mb4'
mysql.init_app(app)

conn = mysql.connect()
cursor =conn.cursor()

add_post = ("INSERT INTO Post (post_id, post_author, post_text, date_posted, date_found, url) VALUES (%s, %s, %s, %s, %s, %s)")

c = twint.Config(Limit=20)
c.Store_object = True
c.Hide_output = True

#Full list
uni_list = ['Aberdeen', 'Abertay', 'Aberystwyth', 'Anglia Ruskin', 'Aston', 'Bangor', 'Bath', 'Bath Spa', 'Bedfordshire', 'Birmingham', 'Birmingham City', 'Bolton', 'Bournemouth', 'Bradford', 'Brighton', 'Bristol', 'Brunel', 'Bucks New University', 'Cambridge', 'Canterbury Christ Church', 'Cardiff', 'Cardiff Met', 'Central Lancashire', 'Chester', 'Chichester', 'City', 'Coventry', 'Cumbria', 'De Montfort', 'Derby', 'Dundee', 'Durham', 'East London', 'Edge Hill', 'Edinburgh', 'Edinburgh Napier', 'Essex', 'Exeter', 'Falmouth', 'Glasgow', 'Glasgow Caledonian', 'Gloucestershire', 'Glyndwr', 'Goldsmiths', 'Greenwich', 'Heriot-Watt', 'Hertfordshire', 'Huddersfield', 'Hull', 'Imperial College', 'Keele', 'Kent', "King's College London", 'Kingston', 'Lancaster', 'Leeds', 'Leeds Beckett', 'Leeds Trinity', 'Leicester', 'Lincoln', 'Liverpool', 'Liverpool Hope', 'Liverpool John Moores', 'London Met', 'London School of Economics', 'London South Bank', 'Loughborough', 'Manchester', 'Manchester Met', 'Middlesex', 'Newcastle', 'Newman', 'Northampton', 'Northumbria', 'Nottingham', 'Nottingham Trent', 'Oxford', 'Oxford Brookes', 'Plymouth', 'Portsmouth', 'Queen Margaret', 'Queen Mary', "Queen's, Belfast", 'Reading', 'Robert Gordon', 'Roehampton', 'Royal Holloway', 'Salford', 'Sheffield', 'Sheffield Hallam', 'SOAS', 'Solent', 'South Wales', 'Southampton', 'St Andrews', "St Mary's, Twickenham", 'Staffordshire', 'Stirling', 'Strathclyde', 'Suffolk', 'Sunderland', 'Surrey', 'Sussex', 'Swansea', 'Teesside', 'Trinity Saint David', 'UCL', 'UEA', 'Ulster', 'University for the Creative Arts', 'University of the Arts London', 'UWE Bristol', 'Warwick', 'West London', 'West of Scotland', 'Westminster', 'Winchester', 'Wolverhampton', 'Worcester', 'York', 'York St John']

#Shorten list for testing
uni_list = uni_list[:38:]

#Run a search for each different university
for uni in uni_list:
    c.Search = 'IBM university ("' + uni + '") -filter:replies'
    twint.run.Search(c)

#Write each tweet to database
for tweet_object in twint.output.tweets_list:
    new_post = (tweet_object.id, tweet_object.username, tweet_object.tweet, tweet_object.datestamp, date.today().strftime('%Y-%m-%d'), tweet_object.link)
    cursor.execute(add_post, new_post)

conn.commit()
conn.close()
print("Data commited")
