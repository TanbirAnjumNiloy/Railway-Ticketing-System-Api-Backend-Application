# Generated by Django 5.0.2 on 2024-02-24 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_alter_trainstop_arrival_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainstop',
            name='train_stop_id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]