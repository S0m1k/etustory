import sqlite3

class Score_DB:
    def __init__(self, db):
        self.db = sqlite3.connect(db, check_same_thread=False)
        self.cursor = self.db.cursor()

    def user_exist(self, username):
        return bool(len(self.cursor.execute("SELECT * FROM 'score_rating' WHERE username = ?", (username, )).fetchall()))

    def new_score(self, username, score):
        if(self.user_exist(username)):
            self.cursor.execute(f"UPDATE 'score_rating' SET 'score' = ? WHERE username = ? AND score < ?",
                                (score, username, score, ))
        else:
            self.cursor.execute("INSERT INTO 'score_rating' ('username', 'score') VALUES (?, ?) ", (username, score, ))
        self.db.commit()

    def get_scores(self):
        ans = self.cursor.execute("SELECT username, score FROM 'score_rating' ORDER BY score").fetchall()
        return ans