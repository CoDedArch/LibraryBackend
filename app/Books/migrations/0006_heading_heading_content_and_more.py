# Generated by Django 5.0.7 on 2024-08-18 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Books', '0005_heading_subheading'),
    ]

    operations = [
        migrations.AddField(
            model_name='heading',
            name='heading_content',
            field=models.TextField(blank=True, max_length=1500, null=True),
        ),
        migrations.AddField(
            model_name='subheading',
            name='subheading_content',
            field=models.TextField(blank=True, max_length=1500, null=True),
        ),
    ]