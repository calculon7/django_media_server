# Generated by Django 3.1.3 on 2020-11-20 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media_server', '0025_auto_20201120_1403'),
    ]

    operations = [
        migrations.AddField(
            model_name='hls',
            name='stream_id',
            field=models.IntegerField(null=True),
        ),
    ]
