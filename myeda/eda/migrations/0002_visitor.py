# Generated by Django 3.1.4 on 2021-01-04 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eda', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=60)),
                ('content', models.CharField(default='', max_length=500)),
            ],
        ),
    ]
