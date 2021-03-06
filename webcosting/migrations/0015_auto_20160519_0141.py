# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-18 23:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webcosting', '0014_auto_20160519_0119'),
    ]

    operations = [
        migrations.AddField(
            model_name='projet',
            name='cplx',
            field=models.FloatField(blank=True, choices=[(0.7, 'tr\xe8s bas: 0.70'), (0.85, 'bas: 0.85'), (1.0, 'moyen: 1.00'), (1.15, '\xe9lev\xe9: 1.15'), (1.3, 'tr\xe8s \xe9lev\xe9: 1.30'), (1.65, 'tr\xe8s tr\xe8s \xe9lev\xe9: 1.65')], default=None, null=True),
        ),
        migrations.AlterField(
            model_name='projet',
            name='donn',
            field=models.FloatField(blank=True, choices=[(0.94, 'bas (0.94)'), (1.0, 'moyen (1.00)'), (1.08, '\xe9lev\xe9 (1.08)'), (1.16, 'tr\xe8s \xe9lev\xe9 (1.16)')], default=None, null=True),
        ),
        migrations.AlterField(
            model_name='projet',
            name='fiab',
            field=models.FloatField(blank=True, choices=[(0.75, 'tr\xe8s bas: 0.75'), (0.88, 'bas: 0.88'), (1.0, 'moyen: 1.00'), (1.15, '\xe9lev\xe9: 1.15'), (1.4, 'tr\xe8s \xe9lev\xe9: 1.40')], default=None, null=True),
        ),
    ]
