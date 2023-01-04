# Generated by Django 4.1.3 on 2022-12-06 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_review_email_review_first_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='email',
            field=models.EmailField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='first_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
