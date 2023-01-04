# Generated by Django 4.1.3 on 2022-11-22 19:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_alter_comments_post_blog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='post_blog',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='post_blog', to='core.postblog'),
        ),
    ]
