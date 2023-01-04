# Generated by Django 4.1.3 on 2022-11-17 16:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('photologue', '0012_alter_photo_effect'),
        ('taggit', '0005_auto_20220424_2025'),
        ('core', '0004_alter_postblog_favourite'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='postblog',
            options={'verbose_name': 'Посты', 'verbose_name_plural': 'Работы'},
        ),
        migrations.AlterField(
            model_name='postblog',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='postblog',
            name='favourite',
            field=models.ManyToManyField(blank=True, related_name='favourite', to=settings.AUTH_USER_MODEL, verbose_name='Избранное'),
        ),
        migrations.AlterField(
            model_name='postblog',
            name='images',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='photologue.gallery', verbose_name='Галерея'),
        ),
        migrations.AlterField(
            model_name='postblog',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Теги'),
        ),
    ]
