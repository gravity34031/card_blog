# Generated by Django 4.1.3 on 2022-11-15 12:01

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0003_alter_postblog_favourite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postblog',
            name='favourite',
            field=models.ManyToManyField(blank=True, related_name='favourite', to=settings.AUTH_USER_MODEL),
        ),
    ]
