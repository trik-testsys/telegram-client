from bot.conf import PATH_TO_USER
import peewee as pw


class User(pw.Model):
    user_id = pw.CharField(unique=True, primary_key=True)
    telegram_id = pw.CharField(unique=True)
    role = pw.CharField()

    class Meta:
        database = pw.SqliteDatabase(
            PATH_TO_USER, pragmas={"journal_mode": "wal", "synchronous": "normal"}
        )
