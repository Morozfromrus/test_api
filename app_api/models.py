from django.conf import settings
from django.db import models
from model_utils import Choices


class Partner(models.Model):
    class Meta:
        verbose_name = 'Партнер'
        verbose_name_plural = 'Партнеры'

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='partner',
        on_delete=models.SET_NULL,
        verbose_name='Пользователь',
        null=True
    )
    name = models.CharField('Название', max_length=50)
    description = models.TextField('Описание')

    def __str__(self):
        return self.name


class CreditOrganization(models.Model):
    class Meta:
        verbose_name = 'Кредитная организация'
        verbose_name_plural = 'Кредитные организации'

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='credit_organization',
        on_delete=models.SET_NULL,
        verbose_name='Пользователь',
        null=True
    )
    name = models.CharField('Название', max_length=50)
    description = models.TextField('Описание')

    def __str__(self):
        return self.name


class Offer(models.Model):
    class Meta:
        verbose_name = 'Предложение'
        verbose_name_plural = 'Предложения'

    TYPES = Choices(
        ('consumer', 'Потребительское'),
        ('mortgage', 'Ипотека'),
        ('car_loan', 'Автокредит'),
    )
    create_datetime = models.DateTimeField('Дата и время создания', auto_now_add=True)
    update_datetime = models.DateTimeField('Дата и время изменения', auto_now=True)
    rotation_start_datetime = models.DateTimeField('Дата и время начала ротации')
    rotation_end_datetime = models.DateTimeField('Дата и время окончания ротации')
    name = models.CharField('Название предложения', max_length=50)
    type = models.CharField('Тип предложения', max_length=20, choices=TYPES)
    minimum_score = models.IntegerField('Минимальный скоринговый балл')
    maximum_score = models.IntegerField('Максимальный скоринговый балл')
    credit_organization = models.ForeignKey(
        'CreditOrganization',
        related_name='offers',
        on_delete=models.CASCADE,
        verbose_name='Кредитная организация'
    )

    def is_owner(self, user):
        return hasattr(user, 'credit_organization') and user.credit_organization == self.credit_organization

    def __str__(self):
        return self.name


class CustomerProfile(models.Model):
    class Meta:
        permissions = (
            ('send_request', 'Can send to credit organization'),
        )
        verbose_name = 'Анкета клиента'
        verbose_name_plural = 'Анкеты клиентов'

    create_datetime = models.DateTimeField('Дата и время создания', auto_now_add=True)
    update_datetime = models.DateTimeField('Дата и время изменения', auto_now=True)
    second_name = models.CharField('Фамилия', max_length=20)
    first_name = models.CharField('Имя', max_length=20)
    middle_name = models.CharField('Отчество', max_length=20)
    birthday = models.DateField('Дата рождения')
    phone = models.IntegerField('Номер телефона')
    passport = models.IntegerField('Номер паспорта')
    score = models.IntegerField('Скоринговый балл')
    partner = models.ForeignKey(
        'Partner',
        related_name='customer_profiles',
        on_delete=models.CASCADE,
        verbose_name='Партнер'
    )

    def is_owner(self, user):
        return hasattr(user, 'partner') and user.partner == self.partner

    def __str__(self):
        return '{} {} {}'.format(self.second_name, self.first_name, self.middle_name)


class Request(models.Model):
    class Meta:
        permissions = (
            ('change_status_request', 'Can change status after received'),
        )
        verbose_name = 'Заявка в кредитную организацию'
        verbose_name_plural = 'Заявки в кредитные организации'

    STATUSES = Choices(
        ('new', 'Новая'),
        ('approved', 'Одобрено'),
        ('denied', 'Отказано'),
        ('granted', 'Выдано'),
    )
    create_datetime = models.DateTimeField('Дата и время создания')
    send_datetime = models.DateTimeField('Дата и время отправки')
    customer_profile = models.ForeignKey(
        'CustomerProfile',
        related_name='requests',
        on_delete=models.CASCADE,
        verbose_name='Анкета клиента'
    )
    offer = models.ForeignKey(
        'Offer',
        related_name='requests',
        on_delete=models.CASCADE,
        verbose_name='Предложение'
    )
    status = models.CharField('Статус', max_length=20, choices=STATUSES, default=STATUSES.new)

    def is_owner(self, user):
        return (
            (hasattr(user, 'partner') and user.partner == self.customer_profile.partner) or
            (hasattr(user, 'credit_organization') and user.credit_organization == self.offer.credit_organization)
        )
