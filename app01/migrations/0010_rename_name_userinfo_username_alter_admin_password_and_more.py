# Generated by Django 5.1 on 2024-09-05 03:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0009_city'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userinfo',
            old_name='name',
            new_name='username',
        ),
        migrations.AlterField(
            model_name='admin',
            name='password',
            field=models.CharField(max_length=64, verbose_name='Password'),
        ),
        migrations.AlterField(
            model_name='admin',
            name='username',
            field=models.CharField(max_length=32, verbose_name='Username'),
        ),
        migrations.AlterField(
            model_name='boss',
            name='age',
            field=models.IntegerField(verbose_name='Age'),
        ),
        migrations.AlterField(
            model_name='boss',
            name='img',
            field=models.CharField(max_length=128, verbose_name='Avatar'),
        ),
        migrations.AlterField(
            model_name='boss',
            name='name',
            field=models.CharField(max_length=32, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='city',
            name='count',
            field=models.IntegerField(verbose_name='Population'),
        ),
        migrations.AlterField(
            model_name='city',
            name='name',
            field=models.CharField(max_length=32, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='order',
            name='admin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.admin', verbose_name='Administrator'),
        ),
        migrations.AlterField(
            model_name='order',
            name='oid',
            field=models.CharField(max_length=64, verbose_name='Order Number'),
        ),
        migrations.AlterField(
            model_name='order',
            name='price',
            field=models.IntegerField(verbose_name='Price'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.SmallIntegerField(choices=[(1, 'Pending Payment'), (2, 'Paid')], default=1, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='order',
            name='title',
            field=models.CharField(max_length=32, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='prettynum',
            name='level',
            field=models.SmallIntegerField(choices=[(1, 'Level 1'), (2, 'Level 2'), (3, 'Level 3'), (4, 'Level 4')], default=1, verbose_name='Level'),
        ),
        migrations.AlterField(
            model_name='prettynum',
            name='mobile',
            field=models.CharField(max_length=11, verbose_name='Mobile Number'),
        ),
        migrations.AlterField(
            model_name='prettynum',
            name='price',
            field=models.IntegerField(default=0, verbose_name='Price'),
        ),
        migrations.AlterField(
            model_name='prettynum',
            name='status',
            field=models.SmallIntegerField(choices=[(1, 'Occupied'), (2, 'Unused')], default=2, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='task',
            name='detail',
            field=models.TextField(verbose_name='Details'),
        ),
        migrations.AlterField(
            model_name='task',
            name='level',
            field=models.SmallIntegerField(choices=[(1, 'Urgent'), (2, 'Important'), (3, 'Temporary')], default=1, verbose_name='Level'),
        ),
        migrations.AlterField(
            model_name='task',
            name='title',
            field=models.CharField(max_length=64, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='task',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.admin', verbose_name='Person in Charge'),
        ),
        migrations.AlterField(
            model_name='xx',
            name='image',
            field=models.FileField(upload_to='avatar/', verbose_name='Avatar'),
        ),
        migrations.AlterField(
            model_name='xx',
            name='title',
            field=models.CharField(max_length=32, verbose_name='Title'),
        ),
    ]
