from data.engagement import post


class DatabaseHandler:
    def __init__(self, conn):
        self.conn = conn  # todo update, use connection pool.

    def _get_cursor(self, cursor=None):
        if not cursor:
            cursor = self.conn.cursor()

        return cursor

    def insert_post(self, post_o: post.EngagementPost, cursor=None, commit=False):
        cursor = self._get_cursor(cursor)

        with cursor:
            cursor.execute(
                "INSERT INTO `Post` (`service_id`, `post_author`, `post_text`, `date_posted`, `date_found`, "
                "`url`) VALUES "
                "(%s, %s, %s, %s, %s, %s);",
                (post_o.service_id, post_o.author, post_o.content, post_o.posted, post_o.found, post_o.url),
            )

        if commit:
            self.conn.commit()

    def close(self):
        self.conn.commit()
        self.conn.close()
