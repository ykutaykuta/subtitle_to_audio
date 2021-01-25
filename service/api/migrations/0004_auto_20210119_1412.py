# Generated by Django 3.1.5 on 2021-01-19 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20210106_0325'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ttsaudio',
            name='audio',
        ),
        migrations.AddField(
            model_name='ttsaudio',
            name='duration',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
