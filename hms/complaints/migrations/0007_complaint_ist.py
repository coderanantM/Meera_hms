# Generated by Django 5.0.6 on 2025-01-30 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('complaints', '0006_remove_complaint_bitsid_remove_complaint_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint',
            name='ist',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
