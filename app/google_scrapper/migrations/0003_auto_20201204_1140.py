# Generated by Django 3.1.4 on 2020-12-04 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('google_scrapper', '0002_auto_20201204_1137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='searchrecord',
            name='link',
            field=models.URLField(max_length=500),
        ),
    ]
