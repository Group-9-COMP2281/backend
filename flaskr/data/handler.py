from typing import List

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

                f = None
                if post_o.post_id != -1:
                    f = lambda univ_name: cursor.execute(
                        "INSERT INTO `University` (`university_name`, `post_id`) VALUES (%s, %s)",
                        (univ_name, post_o.post_id)
                    )
                else:
                    f = lambda univ_name: cursor.execute(
                        "INSERT INTO `University` (`university_name`, `post_id`) VALUES (%s, {})".format(
                            "LAST_INSERT_ID()"
                        ), (univ_name)
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
            
    def close(self):
        self.conn.commit()
        self.conn.close()
