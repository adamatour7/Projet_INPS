# Generated by Django 4.2.15 on 2024-09-03 09:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employeur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255)),
                ('adresse', models.TextField()),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('numero_identification', models.CharField(max_length=50, unique=True)),
                ('date_enregistrement', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Employe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255)),
                ('prenom', models.CharField(max_length=255)),
                ('numero_identification', models.CharField(max_length=50, unique=True)),
                ('employeur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employes', to='mobile.employeur')),
            ],
        ),
        migrations.CreateModel(
            name='Cotisation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('periode_debut', models.DateField()),
                ('periode_fin', models.DateField()),
                ('montant_verse', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date_versement', models.DateField()),
                ('employe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cotisations', to='mobile.employe')),
            ],
        ),
    ]