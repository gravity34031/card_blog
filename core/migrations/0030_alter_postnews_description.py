# Generated by Django 4.1.3 on 2022-12-07 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_alter_postnews_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postnews',
            name='description',
            field=models.CharField(max_length=100),
        ),
    ]
