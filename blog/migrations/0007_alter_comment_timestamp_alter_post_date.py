# Generated by Django 4.0.4 on 2022-05-23 14:31

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_alter_comment_timestamp_alter_post_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 23, 14, 31, 0, 897916, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]