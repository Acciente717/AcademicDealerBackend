# Generated by Django 2.1.7 on 2019-05-26 13:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SeminarComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField()),
                ('modified_date', models.DateTimeField()),
                ('description', models.TextField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.UserAccount')),
            ],
        ),
        migrations.CreateModel(
            name='SeminarInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('create_date', models.DateTimeField()),
                ('modified_date', models.DateTimeField()),
                ('member_number_limit', models.PositiveIntegerField()),
                ('description', models.TextField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.UserAccount')),
            ],
        ),
        migrations.CreateModel(
            name='SeminarMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.UserAccount')),
                ('seminar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seminar.SeminarInfo')),
            ],
        ),
        migrations.AddField(
            model_name='seminarcomment',
            name='seminar',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seminar.SeminarInfo'),
        ),
    ]