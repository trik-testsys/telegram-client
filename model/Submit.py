import peewee as pw
from bot.loader import db


class Submit(pw.Model):
    submit_id = pw.CharField(unique=True, primary_key=True)
    student_id = pw.CharField()
    task_name = pw.CharField()
    result = pw.CharField()

    class Meta:
        database = db

