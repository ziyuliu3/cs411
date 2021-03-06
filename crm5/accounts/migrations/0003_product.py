# Generated by Django 3.0.8 on 2020-08-01 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20200801_0445'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('productName', models.CharField(max_length=50)),
                ('price', models.FloatField()),
                ('gender', models.CharField(max_length=50)),
                ('depreciation', models.FloatField()),
                ('category', models.CharField(choices=[('Lifestyle', 'Lifestyle'), ('Kitchen', 'Kitchen'), ('Fashion', 'Fashion'), ('Beauty', 'Beauty'), ('Study', 'Study')], max_length=500)),
            ],
        ),
    ]
