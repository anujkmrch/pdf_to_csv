# Generated by Django 2.2.6 on 2020-04-03 10:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Csv',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('npa_key', models.CharField(blank=None, default=None, max_length=100, null=True)),
                ('npa_val', models.CharField(blank=None, default=None, max_length=100, null=True)),
                ('csv', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='varapp.Csv')),
            ],
        ),
    ]
