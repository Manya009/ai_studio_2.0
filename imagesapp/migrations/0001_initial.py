# Generated by Django 4.1 on 2023-04-09 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('story_text', models.CharField(max_length=200)),
                ('image_link', models.URLField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
