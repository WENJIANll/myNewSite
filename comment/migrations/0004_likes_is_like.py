# Generated by Django 2.1.5 on 2020-10-26 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0003_auto_20201026_0821'),
    ]

    operations = [
        migrations.AddField(
            model_name='likes',
            name='is_like',
            field=models.IntegerField(default=1),
        ),
    ]