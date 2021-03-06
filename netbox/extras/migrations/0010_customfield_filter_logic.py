# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-21 19:48
from __future__ import unicode_literals

from django.db import migrations, models

from extras.constants import CF_FILTER_DISABLED, CF_FILTER_EXACT, CF_FILTER_LOOSE, CF_TYPE_SELECT


def is_filterable_to_filter_logic(apps, schema_editor):
    CustomField = apps.get_model('extras', 'CustomField')
    CustomField.objects.filter(is_filterable=False).update(filter_logic=CF_FILTER_DISABLED)
    CustomField.objects.filter(is_filterable=True).update(filter_logic=CF_FILTER_LOOSE)
    # Select fields match on primary key only
    CustomField.objects.filter(is_filterable=True, type=CF_TYPE_SELECT).update(filter_logic=CF_FILTER_EXACT)


def filter_logic_to_is_filterable(apps, schema_editor):
    CustomField = apps.get_model('extras', 'CustomField')
    CustomField.objects.filter(filter_logic=CF_FILTER_DISABLED).update(is_filterable=False)
    CustomField.objects.exclude(filter_logic=CF_FILTER_DISABLED).update(is_filterable=True)


class Migration(migrations.Migration):

    dependencies = [
        ('extras', '0009_topologymap_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='customfield',
            name='filter_logic',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Disabled'), (1, 'Loose'), (2, 'Exact')], default=1, help_text='Loose matches any instance of a given string; exact matches the entire field.'),
        ),
        migrations.AlterField(
            model_name='customfield',
            name='required',
            field=models.BooleanField(default=False, help_text='If true, this field is required when creating new objects or editing an existing object.'),
        ),
        migrations.AlterField(
            model_name='customfield',
            name='weight',
            field=models.PositiveSmallIntegerField(default=100, help_text='Fields with higher weights appear lower in a form.'),
        ),
        migrations.RunPython(is_filterable_to_filter_logic, filter_logic_to_is_filterable),
        migrations.RemoveField(
            model_name='customfield',
            name='is_filterable',
        ),
    ]
