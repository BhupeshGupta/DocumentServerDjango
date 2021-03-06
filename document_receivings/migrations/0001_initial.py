# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-22 06:35
from __future__ import unicode_literals

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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref_no', models.CharField(blank=True, max_length=255)),
                ('doctype', models.CharField(max_length=255)),
                ('docname', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('status', models.IntegerField(choices=[(0, 'Pending'), (1, 'Verified'), (2, 'Rejected'), (3, 'Decision Pending')], default=0)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(max_length=255, null=True)),
                ('modified_by', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=b'')),
                ('size', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=255)),
                ('filename', models.CharField(max_length=255)),
                ('document', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='files', to='document_receivings.Document')),
            ],
        ),
        migrations.CreateModel(
            name='Verification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(0, 'Pending'), (1, 'Verified'), (2, 'Rejected')])),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(max_length=255, null=True)),
                ('modified_by', models.CharField(max_length=255, null=True)),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='document_receivings.Document')),
            ],
        ),
        migrations.AddField(
            model_name='file',
            name='verification',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='document_receivings.Verification'),
        ),
        migrations.AlterUniqueTogether(
            name='document',
            unique_together=set([('doctype', 'docname')]),
        ),
    ]
