import sqlite3
import aiogram
import json


class Connect:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def admin(self):
        result = self.cursor.execute("SELECT * FROM admins",)
        return result.fetchall()

    def change(self, message_id, text_admin, old_message_id):
        self.cursor.execute("UPDATE list "
                            "SET id = ?, text = ? "
                            "WHERE message_id = ?", (message_id, text_admin, old_message_id))
        return self.conn.commit()

    def create(self, admin_id):
        self.cursor.execute("INSERT INTO `admin` (`id_user`) VALUES (?)",(admin_id,))
        return self.conn.commit()

    def delete(self, admin_id):
        self.cursor.execute("DELETE FROM `admin` WHERE id_user = ?", (admin_id,))
        return self.conn.commit()
