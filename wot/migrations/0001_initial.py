# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-16 06:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clan',
            fields=[
                ('clan_id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('tag', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('account_id', models.IntegerField(primary_key=True, serialize=False)),
                ('access_token', models.TextField(blank=True, null=True)),
                ('access_token_expires_at', models.CharField(blank=True, max_length=10, null=True)),
                ('account_name', models.CharField(max_length=250)),
                ('clan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='members', to='wot.Clan')),
            ],
            options={
                'ordering': ['account_name'],
            },
        ),
        migrations.CreateModel(
            name='PlayerData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('joined_clan_date', models.DateTimeField(blank=True, null=True)),
                ('role_in_clan', models.CharField(blank=True, max_length=250, null=True)),
                ('battles_on_random', models.IntegerField(blank=True, null=True)),
                ('battles_all', models.IntegerField(blank=True, null=True)),
                ('battles_stronghold', models.IntegerField(blank=True, null=True)),
                ('last_battle_time', models.DateTimeField(blank=True, null=True)),
                ('total_resources_earned', models.IntegerField(blank=True, null=True)),
                ('week_resources_earned', models.IntegerField(blank=True, null=True)),
                ('player', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player', to='wot.Player')),
            ],
            options={
                'get_latest_by': 'created',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('name', models.TextField()),
                ('short_name', models.TextField()),
                ('tank_id', models.IntegerField(primary_key=True, serialize=False)),
                ('tier', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='playerdata',
            name='tank',
            field=models.ManyToManyField(blank=True, related_name='tanks', to='wot.Vehicle'),
        ),
    ]
