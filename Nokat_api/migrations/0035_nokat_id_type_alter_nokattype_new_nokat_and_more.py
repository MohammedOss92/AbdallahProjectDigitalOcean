# Generated by Django 4.2 on 2024-06-24 15:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Nokat_api', '0034_remove_nokat_id_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='nokat',
            name='ID_Type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Nokat_api.nokattype'),
        ),
        migrations.AlterField(
            model_name='nokattype',
            name='new_Nokat',
            field=models.CharField(default='1', max_length=2),
        ),
        migrations.AlterField(
            model_name='nokattype',
            name='new_Nokat_show',
            field=models.CharField(default='0', max_length=2),
        ),
    ]
