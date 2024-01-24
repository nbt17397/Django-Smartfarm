# Generated by Django 4.0.7 on 2024-01-23 03:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hatchery', '0003_area_alter_building_description_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuildingDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('id_box', models.SmallIntegerField(null=True)),
                ('is_running', models.BooleanField(default=True)),
                ('building_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='detail_ids', to='hatchery.building')),
            ],
            options={
                'unique_together': {('name', 'id_box')},
            },
        ),
    ]