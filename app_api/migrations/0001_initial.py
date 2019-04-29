# Generated by Django 2.2 on 2019-04-29 00:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CreditOrganization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='credit_organization', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Кредитная организация',
                'verbose_name_plural': 'Кредитные организации',
            },
        ),
        migrations.CreateModel(
            name='CustomerProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')),
                ('update_datetime', models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения')),
                ('second_name', models.CharField(max_length=20, verbose_name='Фамилия')),
                ('first_name', models.CharField(max_length=20, verbose_name='Имя')),
                ('middle_name', models.CharField(max_length=20, verbose_name='Отчество')),
                ('birthday', models.DateField(verbose_name='Дата рождения')),
                ('phone', models.IntegerField(verbose_name='Номер телефона')),
                ('passport', models.IntegerField(verbose_name='Номер паспорта')),
                ('score', models.IntegerField(verbose_name='Скоринговый балл')),
            ],
            options={
                'verbose_name': 'Анкета клиента',
                'verbose_name_plural': 'Анкеты клиентов',
                'permissions': (('send_request', 'Can send to credit organization'),),
            },
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')),
                ('update_datetime', models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения')),
                ('rotation_start_datetime', models.DateTimeField(verbose_name='Дата и время начала ротации')),
                ('rotation_end_datetime', models.DateTimeField(verbose_name='Дата и время окончания ротации')),
                ('name', models.CharField(max_length=50, verbose_name='Название предложения')),
                ('type', models.CharField(choices=[('consumer', 'Потребительское'), ('mortgage', 'Ипотека'), ('car_loan', 'Автокредит')], max_length=20, verbose_name='Тип предложения')),
                ('minimum_score', models.IntegerField(verbose_name='Минимальный скоринговый балл')),
                ('maximum_score', models.IntegerField(verbose_name='Максимальный скоринговый балл')),
                ('credit_organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offers', to='app_api.CreditOrganization', verbose_name='Кредитная организация')),
            ],
            options={
                'verbose_name': 'Предложение',
                'verbose_name_plural': 'Предложения',
            },
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_datetime', models.DateTimeField(verbose_name='Дата и время создания')),
                ('send_datetime', models.DateTimeField(verbose_name='Дата и время отправки')),
                ('status', models.CharField(choices=[('new', 'Новая'), ('sent', 'Отправлена'), ('received', 'Получена'), ('approved', 'Одобрено'), ('denied', 'Отказано'), ('granted', 'Выдано')], default='new', max_length=20, verbose_name='Статус')),
                ('customer_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to='app_api.CustomerProfile', verbose_name='Анкета клиента')),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to='app_api.Offer', verbose_name='Предложение')),
            ],
            options={
                'verbose_name': 'Заявка в кредитную организацию',
                'verbose_name_plural': 'Заявки в кредитные организации',
                'permissions': (('change_status_request', 'Can change status after received'),),
            },
        ),
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='partner', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Партнер',
                'verbose_name_plural': 'Партнеры',
            },
        ),
        migrations.AddField(
            model_name='customerprofile',
            name='partner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_profiles', to='app_api.Partner', verbose_name='Партнер'),
        ),
    ]