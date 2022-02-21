import peewee as pw


class User(pw.Model):
    user_id = pw.CharField(unique=True, primary_key=True)
    role = pw.CharField()

    class Meta:
        database = pw.SqliteDatabase("C:\\Users\\mi\\Desktop\\trik-testsys-client\\user.sqlite", pragmas={
            'journal_mode': 'wal',
            'synchronous': 'normal'
        })
