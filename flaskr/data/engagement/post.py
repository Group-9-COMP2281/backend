class EngagementPost:
    def __init__(self, service_id, author, content, posted, found, url):
        self.service_id = service_id
        self.author = author
        self.content = content
        self.posted = posted
        self.found = found
        self.url = url

    def __str__(self):
        return "EngagementPost[{},{},{},{},{},{}]".format(
            self.service_id, self.author, self.content, self.posted, self.found, self.url
        )


class TwitterPost(EngagementPost):
    def __init__(self, service_id, author, content, posted, found, url):
        super().__init__(service_id, author, content, posted, found, url)
