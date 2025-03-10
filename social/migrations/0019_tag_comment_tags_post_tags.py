# Generated by Django 4.2 on 2024-11-25 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0018_alter_post_options_post_shared_body_post_shared_on_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='tags',
            field=models.ManyToManyField(blank=True, to='social.tag'),
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(blank=True, to='social.tag'),
        ),
    ]
