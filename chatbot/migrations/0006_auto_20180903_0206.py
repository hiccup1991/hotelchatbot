# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-02 17:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0005_auto_20180902_2227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[(b'customer', b'customer'), (b'frontdesk', b'frontdesk'), (b'concierge', b'concierge'), (b'activitiesdesk', b'activitiesdesk'), (b'operator', b'operator')], default=b'customer', max_length=20),
        ),
    ]
