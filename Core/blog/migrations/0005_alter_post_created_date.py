# Generated by Django 4.2 on 2024-07-01 08:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0004_alter_post_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="created_date",
            field=models.DateField(
                default=datetime.datetime(
                    2024, 7, 1, 8, 39, 7, 806966, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
