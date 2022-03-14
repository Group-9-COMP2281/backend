from typing import List

from data.engagement import post
from data.engagement import university


class DatabaseHandler:
    def __init__(self, conn):
        self.conn = conn  # todo update, use connection pool.

    def _get_cursor(self, cursor=None):
        if not cursor:
            cursor = self.conn.cursor()

        return cursor

    def insert_posts(self, univ_posts: List[university.UniversityPost], cursor=None, commit=False):
        cursor = self._get_cursor(cursor)

        with cursor:
            for univ_post in univ_posts:
                post_o = univ_post.post_o

                cursor.execute(
                    "INSERT INTO `Post` (`service_id`, `post_author`, `post_text`, `date_posted`, `date_found`, "
                    "`url`) VALUES "
                    "(%s, %s, %s, %s, %s, %s);",
                    (post_o.service_id, post_o.author, post_o.content, post_o.posted, post_o.found, post_o.url),
                )

                insert_univ_query = "INSERT INTO `University` (`university_name`, `post_id`) VALUES (%s, {})"
                f = lambda univ_name: cursor.execute(
                    insert_univ_query.format(
                        '%s' if post_o.post_id != -1 else 'LAST_INSERT_ID()'
                    ),
                    (univ_name, post_o.post_id) if post_o.post_id != -1 else (univ_name)
                )

                for name in univ_post.names:
                    f(name)

        if commit:
            self.conn.commit()

    def insert_post(self, univ_post: university.UniversityPost, cursor=None, commit=False):
        return self.insert_posts([univ_post], cursor=cursor, commit=commit)

    def delete_all_posts(self, cursor=None, commit=False):
        cursor = self._get_cursor(cursor)

        with cursor:
            cursor.execute(
                "DELETE FROM `Post`"
            )

        if commit:
            self.conn.commit()

    def delete_all_universities(self, cursor=None, commit=False):
        cursor = self._get_cursor(cursor)

        with cursor:
            cursor.execute(
                "DELETE FROM `University`"
            )

        if commit:
            self.conn.commit()

    def get_posts_where(self, cursor=None, min_id=-1):
        cursor = self._get_cursor(cursor)

        query = "SELECT * FROM `Post` JOIN `University` ON `Post`.`post_id` = `University`.`post_id`"
        vars = []

        if min_id > -1:
            query += " WHERE `Post`.`post_id` >= %s"
            vars.append(min_id)

        query += ';'

        with cursor:
            cursor.execute(query, tuple(vars))
            res = cursor.fetchall()

            return map(post.EngagementPost.from_row, res)

    def close(self):
        self.conn.commit()
        self.conn.close()
