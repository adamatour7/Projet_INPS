# Generated by Django 4.2.15 on 2024-09-03 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mobile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeur',
            name='prenom',
            field=models.CharField(default=0, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='employe',
            name='numero_identification',
            field=models.IntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='employeur',
            name='numero_identification',
            field=models.IntegerField(unique=True),
        ),
    ]
