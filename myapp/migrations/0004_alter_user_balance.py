# Generated by Django 5.0.2 on 2024-02-23 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_alter_ticketbooked_ticket_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='balance',
            field=models.IntegerField(verbose_name=''),
        ),
    ]
