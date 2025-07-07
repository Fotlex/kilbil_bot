from django.db import models


class User(models.Model):
    id = models.BigIntegerField('Идентификатор Телеграм', primary_key=True, blank=False)

    username = models.CharField('Юзернейм', max_length=64, null=True, blank=True)
    first_name = models.CharField('Имя', null=True, blank=True)
    last_name = models.CharField('Фамилия', null=True, blank=True)

    phone_namber = models.CharField('Номер телефона', blank=True, null=True)
    balance = models.IntegerField('Баланс', default=0)  
    api_id = models.BigIntegerField(null=True, blank=True)
    
    created_at = models.DateTimeField('Дата регистрации', null=True, blank=True)

    data = models.JSONField(default=dict, blank=True)

    api_first_name = models.CharField('Имя', null=True, blank=True)
    api_last_name = models.CharField('Фамилия', null=True, blank=True)
    api_middlename = models.CharField('Отчество', null=True, blank=True)
    api_date_born = models.CharField('Дата рождения', null=True, blank=True)
    api_email = models.CharField('Email', null=True, blank=True)
    
    def __str__(self):
        return f'id{self.id} | @{self.username or "-"} {self.first_name or "-"} {self.last_name or "-"}'

    class Meta:
        verbose_name = 'Телеграм пользователь'
        verbose_name_plural = 'Телеграм пользователи'


class Attachments(models.Model):
    types = {
        'photo': 'Фото',
        'video': 'Видео',
        'document': 'Документ'
    }

    type = models.CharField('Тип вложения', choices=types)
    file = models.FileField('Файл', upload_to='media/mailing')
    file_id = models.TextField(null=True)
    mailing = models.ForeignKey('Mailing', on_delete=models.SET_NULL, null=True, related_name='attachments')

    class Meta:
        verbose_name = 'Вложение'
        verbose_name_plural = 'Вложения'


class Mailing(models.Model):
    text = models.TextField('Текст', blank=True, null=True)
    datetime = models.DateTimeField('Дата/Время')
    is_ok = models.BooleanField('Статус отправки', default=False)

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        
        
class SupportHelp(models.Model):
    support_url = models.CharField(verbose_name='Укажите ссылку на аккаунт', blank=True, null=True)
    
    
    def __str__(self):
        return 'Техническая поддержка'
    
    
    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
    
    
    class Meta:
        verbose_name = 'Техническая поддержка'
        verbose_name_plural = 'Техническая поддержка'



class UserCode(models.Model):
    user_id = models.BigIntegerField(null=True, blank=True)
    qr_message_id = models.IntegerField(null=True, blank=True)