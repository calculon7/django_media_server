# Generated by Django 3.1.3 on 2020-11-11 16:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('media_server', '0003_auto_20201109_2116'),
    ]

    operations = [
        migrations.AddField(
            model_name='mediafile',
            name='tv_episode',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='media_server.tvepisode'),
            preserve_default=False,
        ),
    ]
