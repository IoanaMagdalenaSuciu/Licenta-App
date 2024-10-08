# Generated by Django 4.0.1 on 2024-05-19 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0004_student_vark_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='choices',
            field=models.ManyToManyField(to='student.Choice'),
        ),
        migrations.AlterField(
            model_name='student',
            name='goals',
            field=models.ManyToManyField(to='student.Goal'),
        ),
        migrations.AlterField(
            model_name='student',
            name='interests',
            field=models.ManyToManyField(to='student.Interest'),
        ),
    ]
