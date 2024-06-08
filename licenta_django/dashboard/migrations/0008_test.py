# Generated by Django 5.0.6 on 2024-05-21 20:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_courseproject_delete_project'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('questions', models.JSONField()),
                ('enrollment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tests', to='dashboard.enrollment')),
            ],
        ),
    ]
