# Generated by Django 3.2.6 on 2021-10-27 10:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20211027_1543'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='child_task',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.task'),
        ),
        migrations.DeleteModel(
            name='Child',
        ),
    ]
