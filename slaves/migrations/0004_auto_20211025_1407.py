# Generated by Django 3.2.8 on 2021-10-25 14:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('slaves', '0003_auto_20211025_1307'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userinfo',
            old_name='growth',
            new_name='height',
        ),
        migrations.AlterUniqueTogether(
            name='userinfo',
            unique_together={('name', 'sur_name')},
        ),
        migrations.DeleteModel(
            name='Slave',
        ),
        migrations.RemoveField(
            model_name='userinfo',
            name='position',
        ),
    ]