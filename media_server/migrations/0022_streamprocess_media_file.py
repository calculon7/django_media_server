# Generated by Django 3.1.3 on 2020-11-18 18:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('media_server', '0021_streamprocess'),
    ]

    operations = [
        migrations.AddField(
            model_name='streamprocess',
            name='media_file',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='media_server.mediafile'),
        ),
    ]