# Generated by Django 4.1.3 on 2023-01-16 18:14

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0003_alter_postnews_image_avatar'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Avatar',
            new_name='UserAvatar',
        ),
    ]