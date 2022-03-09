import peewee as pw


class User(pw.Model):
    user_id = pw.CharField(unique=True, primary_key=True)
    role = pw.CharField()

    class Meta:
        database = pw.SqliteDatabase("/data/user.sqlite", pragmas={
            'journal_mode': 'wal',
            'synchronous': 'normal'
        })
