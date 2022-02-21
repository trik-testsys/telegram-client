import os

import peewee as pw


class Submit(pw.Model):
    submit_id = pw.CharField(unique=True, primary_key=True)
    student_id = pw.CharField()
    task_name = pw.CharField()
    result = pw.CharField()

    class Meta:

        database = pw.SqliteDatabase("C:\\Users\\mi\\Desktop\\trik-testsys-client\\submit.sqlite", pragmas={
            'journal_mode': 'wal',
            'synchronous': 'normal'
        })
