# Generated by Django 5.0.6 on 2024-05-19 20:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_alter_project_description_alter_project_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('description', models.CharField(max_length=1000)),
                ('requirements', models.JSONField()),
                ('enrollement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courseprojects', to='dashboard.enrollment')),
            ],
        ),
        migrations.DeleteModel(
            name='Project',
        ),
    ]
