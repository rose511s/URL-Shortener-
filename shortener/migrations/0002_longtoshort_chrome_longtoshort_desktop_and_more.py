# Generated by Django 4.1.2 on 2022-10-22 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortener', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='longtoshort',
            name='chrome',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='longtoshort',
            name='desktop',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='longtoshort',
            name='firefox',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='longtoshort',
            name='mobile',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='longtoshort',
            name='opera',
            field=models.IntegerField(default=0),
        ),
    ]
