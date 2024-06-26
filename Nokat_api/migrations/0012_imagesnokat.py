# Generated by Django 4.2 on 2024-04-24 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Nokat_api', '0011_delete_imagesnokat'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImagesNokat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('NokatTypes', models.CharField(max_length=20, null=True)),
                ('new_nokat', models.CharField(choices=[('0', '0'), ('1', '1')], default='1', max_length=2, null=True)),
                ('pic', models.ImageField(upload_to='nokat/')),
                ('image_url', models.URLField(blank=True, null=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('new_msgs_text', models.CharField(choices=[('0', '0'), ('1', '1')], default='1', max_length=1, null=True)),
                ('created_at_new_msgs_text', models.DateField(null=True)),
                ('updated_at_new_msgs_text', models.DateField(null=True)),
                ('my_time_auto', models.TimeField(auto_now_add=True)),
            ],
        ),
    ]
