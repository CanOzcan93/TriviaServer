# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-10-29 17:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('example', '0002_auto_20191024_1119'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(default='', max_length=500)),
                ('correct_answer', models.CharField(default='', max_length=100)),
                ('wrong_answer_one', models.CharField(default='', max_length=100)),
                ('wrong_answer_two', models.CharField(default='', max_length=100)),
                ('wrong_answer_three', models.CharField(default='', max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='currentQuestion',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='game',
            name='room',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AddField(
            model_name='game',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='membership',
            name='answer_eight',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='membership',
            name='answer_eleven',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='membership',
            name='answer_five',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='membership',
            name='answer_four',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='membership',
            name='answer_nine',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='membership',
            name='answer_one',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='membership',
            name='answer_seven',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='membership',
            name='answer_six',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='membership',
            name='answer_ten',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='membership',
            name='answer_three',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='membership',
            name='answer_twelwe',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='membership',
            name='answer_two',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='game',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='membership',
            name='isFailed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='membership',
            name='used_wildcard',
            field=models.BooleanField(default=False),
        ),
    ]
