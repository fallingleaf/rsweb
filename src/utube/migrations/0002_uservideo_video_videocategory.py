# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('utube', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserVideo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('video_id', models.CharField(max_length=128)),
                ('is_like', models.BooleanField(default=False)),
                ('is_favorite', models.BooleanField(default=False)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('youtube_id', models.CharField(max_length=128)),
                ('title', models.TextField(blank=True)),
                ('thumbnail_url', models.TextField(blank=True)),
                ('channel_id', models.CharField(max_length=128, blank=True)),
                ('category_id', models.IntegerField(null=True, blank=True)),
                ('view_count', models.IntegerField(default=0)),
                ('like_count', models.IntegerField(default=0)),
                ('dislike_count', models.IntegerField(default=0)),
                ('favorite_count', models.IntegerField(default=0)),
                ('comment_count', models.IntegerField(default=0)),
                ('fetched_time', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='VideoCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('youtube_id', models.IntegerField(unique=True)),
                ('title', models.CharField(max_length=256)),
            ],
        ),
    ]
