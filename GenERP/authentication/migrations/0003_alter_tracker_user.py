# Generated by Django 4.2 on 2024-01-01 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_remove_tracker_content_type_remove_tracker_object_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tracker',
            name='user',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]