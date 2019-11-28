# Generated by Django 2.2.7 on 2019-11-25 06:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0011_auto_20191125_0036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campuspartner',
            name='cec_partner_status',
            field=models.ForeignKey(blank=True, default=3, null=True, on_delete=django.db.models.deletion.CASCADE, to='partners.CecPartnerStatus', verbose_name='Campus CEC Partner Status'),
        ),
    ]