# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-24 09:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myfinalapp', '0006_aparcamiento_seleccionado'),
    ]

    operations = [
        migrations.RenameField(
            model_name='css',
            old_name='contenido',
            new_name='titulo',
        ),
    ]
