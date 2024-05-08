# Generated by Django 4.1 on 2023-04-11 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videoapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('video_file', models.FileField(upload_to='videos/')),
            ],
        ),
        migrations.DeleteModel(
            name='Movie',
        ),
    ]
