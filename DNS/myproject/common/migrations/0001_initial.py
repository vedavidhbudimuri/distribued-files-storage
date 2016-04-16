# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-14 08:01
from __future__ import unicode_literals

import common.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('doc_name', models.CharField(max_length=1000, primary_key=True, serialize=False)),
                ('docfile', models.FileField(upload_to=b'documents/')),
            ],
        ),
        migrations.CreateModel(
            name='FileSystem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=b'Untitled Folder', max_length=1000)),
                ('type', models.CharField(choices=[(b'FILE', b'FILE'), (b'FOLDER', b'FOLDER')], default=b'Folder', max_length=1000)),
                ('docfile', models.FileField(blank=True, null=True, upload_to=common.models.get_upload_path)),
                ('path', models.CharField(blank=True, default=b'/home', max_length=10000, null=True)),
                ('creation_datetime', models.DateTimeField(auto_now=True, null=True)),
                ('location', models.CharField(blank=True, default=b'', max_length=1000, null=True)),
                ('parent', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='common.FileSystem')),
            ],
        ),
    ]
