# Generated by Django 3.1.3 on 2020-11-12 21:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('media_server', '0013_auto_20201112_1605'),
    ]

    operations = [
        migrations.AddField(
            model_name='tvshowdetail',
            name='tv_show',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='media_server.tvshowdetail'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tvshow',
            name='tv_show_details',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='media_server.tvshowdetail'),
        ),
    ]