# Generated by Django 4.1 on 2024-05-05 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_category_options_remove_course_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='image',
            field=models.ImageField(null=True, upload_to='courses/images'),
        ),
    ]
