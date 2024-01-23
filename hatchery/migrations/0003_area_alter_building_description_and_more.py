# Generated by Django 4.0.7 on 2024-01-19 01:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hatchery', '0002_alter_building_unique_together_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('nation', models.PositiveSmallIntegerField(choices=[(0, 'vietnam'), (1, 'thailand'), (2, 'cambodia')], default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='building',
            name='description',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='building',
            name='id_box',
            field=models.SmallIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='building',
            name='area_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hatchery.area'),
        ),
    ]
