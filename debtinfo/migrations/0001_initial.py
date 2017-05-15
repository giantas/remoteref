# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-15 09:57
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Debtor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_number', models.CharField(max_length=10)),
                ('cell', models.CharField(max_length=12)),
                ('debtor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='debtor', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'tbl_due_listing',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_number', models.CharField(max_length=10)),
                ('cell', models.CharField(max_length=12)),
                ('debtor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile_debtor', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'tb_profiles',
            },
        ),
    ]
