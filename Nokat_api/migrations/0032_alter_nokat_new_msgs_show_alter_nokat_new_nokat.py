# Generated by Django 4.2 on 2024-06-24 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Nokat_api', '0031_rename_nokatid_type_nokat_id_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nokat',
            name='new_msgs_show',
            field=models.IntegerField(default=0, max_length=2),
        ),
        migrations.AlterField(
            model_name='nokat',
            name='new_nokat',
            field=models.IntegerField(default=1, max_length=2),
        ),
    ]
