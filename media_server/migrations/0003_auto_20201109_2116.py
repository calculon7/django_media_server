# Generated by Django 3.1.3 on 2020-11-10 02:16

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('media_server', '0002_tvepisode_filepath_temp'),
    ]

    operations = [
        migrations.CreateModel(
            name='MediaFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filepath', models.CharField(max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='tvepisode',
            name='filepath_temp',
        ),
        migrations.AddField(
            model_name='tvepisode',
            name='versions',
            field=jsonfield.fields.JSONField(default=[], max_length=200),
        ),
        migrations.AlterField(
            model_name='medialibrary',
            name='paths',
            field=jsonfield.fields.JSONField(default=[], max_length=200),
        ),
    ]