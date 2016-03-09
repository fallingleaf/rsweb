# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.CharField(max_length=128)),
                ('event_date', models.DateTimeField()),
                ('event_type', models.CharField(default=b'comment', max_length=128, choices=[(b'enter', b'enter'), (b'highfive', b'highfive'), (b'comment', b'comment'), (b'leave', b'leave')])),
                ('comment', models.TextField(null=True)),
                ('otheruser', models.CharField(max_length=128, null=True)),
            ],
        ),
    ]
