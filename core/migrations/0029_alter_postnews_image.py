# Generated by Django 4.1.3 on 2022-12-07 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_alter_postnews_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postnews',
            name='image',
            field=models.ImageField(blank=True, max_length=200, upload_to='news_posts/'),
        ),
    ]
