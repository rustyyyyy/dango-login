# Generated by Django 4.0.5 on 2022-06-10 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0002_rename_emailvefification_emailverification'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailverification',
            name='verified',
            field=models.BooleanField(default=False),
        ),
    ]