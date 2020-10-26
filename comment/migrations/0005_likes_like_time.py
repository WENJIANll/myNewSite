# Generated by Django 2.1.5 on 2020-10-26 04:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0004_likes_is_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='likes',
            name='like_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
