# Generated by Django 3.1.3 on 2020-11-20 19:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('media_server', '0026_hls_stream_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hls',
            name='stream_id',
        ),
    ]
