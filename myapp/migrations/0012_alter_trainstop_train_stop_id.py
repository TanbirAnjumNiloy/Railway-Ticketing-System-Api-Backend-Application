# Generated by Django 5.0.2 on 2024-02-24 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_alter_trainstop_train_stop_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainstop',
            name='train_stop_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]