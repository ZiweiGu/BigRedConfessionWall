# Generated by Django 2.2.4 on 2019-09-01 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wall', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(default='abc', unique=True),
            preserve_default=False,
        ),
    ]
