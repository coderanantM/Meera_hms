# Generated by Django 5.0.6 on 2025-01-30 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('complaints', '0007_complaint_ist'),
    ]

    operations = [
        migrations.CreateModel(
            name='TechnicalManager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('designation', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=15)),
            ],
        ),
    ]
