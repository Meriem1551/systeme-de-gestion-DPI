# Generated by Django 5.1.3 on 2024-12-22 12:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestiondpi', '0007_remove_consultation_ordonnance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='examen',
            name='consultation',
        ),
        migrations.RemoveField(
            model_name='examen',
            name='date_prescription',
        ),
        migrations.AddField(
            model_name='consultation',
            name='examen',
            field=models.ManyToManyField(blank=True, to='gestiondpi.examen'),
        ),
        migrations.AddField(
            model_name='examen',
            name='parametres',
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AlterField(
            model_name='consultation',
            name='prescription',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='consultation', to='gestiondpi.prescription'),
        ),
        migrations.AlterField(
            model_name='consultation',
            name='resume',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='consultation', to='gestiondpi.resume'),
        ),
    ]