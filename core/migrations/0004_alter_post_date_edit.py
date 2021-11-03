# Generated by Django 3.2.7 on 2021-10-25 15:55

import core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date_edit',
            field=models.DateTimeField(default=django.utils.timezone.now, validators=[core.validators.validate_date_edit]),
        ),
    ]
