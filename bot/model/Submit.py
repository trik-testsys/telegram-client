from bot.conf import PATH_TO_SUBMIT
import peewee as pw


class Submit(pw.Model):
    submit_id = pw.CharField(unique=True, primary_key=True)
    student_id = pw.CharField()
    task_name = pw.CharField()
    result = pw.CharField()

    class Meta:

        database = pw.SqliteDatabase(
            PATH_TO_SUBMIT, pragmas={"journal_mode": "wal", "synchronous": "normal"}
        )
