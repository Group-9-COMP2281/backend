class EngagementPost:
    def __init__(self, service_id, service, univ, author, content, posted, found, url, post_id=-1):
        # post_id having val -1 means that it has been constructed and not pulled from db.
        self.post_id = post_id
        self.service_id = service_id
        self.service = service
        self.univ = univ
        self.author = author
        self.content = content
        self.posted = posted
        self.found = found
        self.url = url

    @staticmethod
    def from_row(row):
        return EngagementPost(
            row[1], 'Twitter', row[7], row[2], row[3], row[4], row[5], row[6],
            post_id=row[0]
        )

    def to_json(self):
        return {
            'post_id': self.post_id,
            'service_id': self.service_id,
            'service': self.service,
            'univ': self.univ.capitalize(),
            'author': self.author,
            'content': self.content,
            'posted': self.posted,
            'found': self.found,
            'url': self.url,
        }

    def __str__(self):
        return "EngagementPost[{},{},{},{},{},{}]".format(
            self.service_id, self.author, self.content, self.posted, self.found, self.url
        )
