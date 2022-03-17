import datetime
import re

import twint

from data.engagement import post, university

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


class Scraper:
    def __init__(self):
        self.contents = []
        self.tweet_unis = {}

    def run_searches(self, uni_names):
        c = twint.Config()
        c.Limit = 20

        c.Store_object = True
        c.Hide_output = True

        uni_names = [x.lower().strip() for x in uni_names]
        posts = []

        for name in uni_names:
            posts.extend(self.posts_from_tweet(name, self.run_search(c, name)))

        return posts

    def run_search(self, cfg, uni_name):
        cfg.Search = 'IBM university ("' + uni_name + '") -filter:replies'
        twint.run.Search(cfg)
        found = []

        for tweet_object in twint.output.tweets_list:
            tweet_stripped = re.sub(r'\w+:/{2}[\d\w-]+(\.[\d\w-]+)*(?:/[^\s/]*)*', '', tweet_object.tweet).replace(
                "#", "")

            if tweet_stripped not in self.contents:
                self.contents.append(tweet_stripped)
                found.append(tweet_object)

                if tweet_object.id_str not in self.tweet_unis:
                    self.tweet_unis[tweet_object.id_str] = [uni_name]
                else:
                    self.tweet_unis[tweet_object.id_str].append(uni_name)
                    found.remove(tweet_object)

        return found

    def posts_from_tweet(self, uni_name, tweet_objects):
        o = []

        for tweet_object in tweet_objects:
            p = post.EngagementPost(tweet_object.id_str, 'Twitter', uni_name, tweet_object.username, tweet_object.tweet,
                                    tweet_object.datestamp,
                                    datetime.datetime.now(), tweet_object.link)

            o.append(university.UniversityPost(self.tweet_unis[tweet_object.id_str], p))

        return o
