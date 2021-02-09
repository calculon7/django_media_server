# Generated by Django 3.1.3 on 2020-11-12 19:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('media_server', '0006_auto_20201112_1354'),
    ]

    operations = [
        migrations.AddField(
            model_name='mediafile',
            name='tv_season',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='media_server.tvseason'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mediafile',
            name='tv_show',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='media_server.tvshow'),
            preserve_default=False,
        ),
    ]