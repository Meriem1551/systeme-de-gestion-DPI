# Generated by Django 5.1.4 on 2024-12-31 12:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestiondpi', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prescription',
            name='medicament',
        ),
        migrations.DeleteModel(
            name='Medicament',
        ),
    ]