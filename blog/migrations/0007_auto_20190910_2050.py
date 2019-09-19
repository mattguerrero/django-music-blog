# Generated by Django 2.2.5 on 2019-09-11 03:50

import django.core.validators
from django.db import migrations, models
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('blog', '0006_auto_20190909_1508'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='category',
        ),
        migrations.RemoveField(
            model_name='post',
            name='title',
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(verbose_name='Your thoughts'),
        ),
        migrations.AlterField(
            model_name='post',
            name='link',
            field=models.CharField(help_text="Format: 'https://open.spotify.com/(track|album|artist)/.*'", max_length=100, validators=[django.core.validators.RegexValidator(message='Please enter a valid link.', regex='(https://open.spotify.com/){1}(track|album|artist|embed/track|embed/album|embed/artist){1}/.*')], verbose_name='Spotify Link'),
        ),
        migrations.AlterField(
            model_name='post',
            name='rating',
            field=models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)]),
        ),
    ]