# Generated by Django 4.1.3 on 2023-03-04 19:38

from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RuTag',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('taggit.tag',),
        ),
        migrations.CreateModel(
            name='RuTaggedItem',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('taggit.taggeditem',),
        ),
    ]
