# Generated by Django 3.1.3 on 2020-11-12 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media_server', '0010_auto_20201112_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tvshowdetails',
            name='overview',
            field=models.TextField(),
        ),
    ]