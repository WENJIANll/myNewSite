# Generated by Django 2.1.5 on 2020-10-26 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0007_auto_20201026_1229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='likes_count',
            name='like_count',
            field=models.IntegerField(default=0),
        ),
    ]
