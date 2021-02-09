# Generated by Django 3.1.3 on 2020-11-12 18:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('media_server', '0005_remove_tvepisode_versions'),
    ]

    operations = [
        migrations.AddField(
            model_name='mediafile',
            name='library',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='media_server.medialibrary'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tvepisode',
            name='library',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='media_server.medialibrary'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tvseason',
            name='library',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='media_server.medialibrary'),
            preserve_default=False,
        ),
    ]
