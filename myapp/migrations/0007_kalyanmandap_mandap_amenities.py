# Generated by Django 5.2.1 on 2025-05-19 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_remove_kalyanmandap_mandap_availability'),
    ]

    operations = [
        migrations.AddField(
            model_name='kalyanmandap',
            name='mandap_amenities',
            field=models.TextField(blank=True, null=True),
        ),
    ]
