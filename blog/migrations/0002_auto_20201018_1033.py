# Generated by Django 2.1.5 on 2020-10-18 02:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'ordering': ['created_time']},
        ),
    ]
