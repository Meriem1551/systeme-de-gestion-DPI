# Generated by Django 5.1.4 on 2024-12-31 21:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestiondpi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consultation',
            name='ordonnance',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='consultation', to='gestiondpi.ordonnance'),
        ),
    ]