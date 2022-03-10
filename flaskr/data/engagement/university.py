from data.engagement import post


class UniversityPost:
    def __init__(self, names, post_o: post.EngagementPost):
        self.names = names
        self.post_o = post_o

    def __str__(self):
        return 'UniversityPost[{}, {}]'.format(self.names, str(self.post_o))
