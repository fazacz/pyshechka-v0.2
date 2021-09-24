from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.dispatch import Signal
from gm2m import GM2MField

from .utilities import send_activation_notification

user_registrated = Signal(providing_args=['instance'])


def user_registrated_dispatcher(sender, **kwargs):
    send_activation_notification(kwargs['instance'])


user_registrated.connect(user_registrated_dispatcher)


class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Активен')
    send_messages = models.BooleanField(default=True, verbose_name='Отправлять сообщения')

    class Meta(AbstractUser.Meta):
        pass


class Entity(models.Model):
    name                 = models.CharField             (unique=True, db_index=True, max_length=120, verbose_name='Наименование')  # Need to fix to make it "unique" for each author
    description          = models.CharField             (default='', blank=True, max_length=250,   verbose_name='Описание')
    author               = models.ForeignKey            (AdvUser, on_delete=models.PROTECT,        verbose_name='Автор')
    creation_date        = models.DateTimeField         (auto_now_add=True, db_index=True,         verbose_name='Дата создания')
    update_date          = models.DateTimeField         (auto_now=True, db_index=True,             verbose_name='Дата правки')
    # image                = models.ImageField            (blank=True, upload_to=get_timestamp_path, verbose_name='Изображение')
    archived             = models.BooleanField          (default=False, db_index=True,             verbose_name='Архивирован')

    protein              = models.FloatField            (default=0,                                verbose_name='Белки')
    fat                  = models.FloatField            (default=0,                                verbose_name='Жиры')
    carbohydrate         = models.FloatField            (default=0,                                verbose_name='Углеводы')
    ethanol              = models.FloatField            (default=0,                                verbose_name='Алкоголь')
    organic_acids        = models.FloatField            (default=0,                                verbose_name='Органические кислоты')
    polyols              = models.FloatField            (default=0,                                verbose_name='Многоатомные спирты')
    fibre                = models.FloatField            (default=0,                                verbose_name='Пищевые волокна')
    energy_value         = models.FloatField            (default=0,                                verbose_name='Калорийность')
    popularity_general   = models.PositiveIntegerField  (default=0,                                verbose_name='Общее число использований')
    # popularity_by_author = models.PositiveIntegerField  (default=0,                                verbose_name='Число использований')  # Need to fix with Through

    # components = models.ManyToManyField(ContentType,  ####################### commented 2020.10.25
    #                                     through='Portion',
    #                                     # through_fields=('dish_meal', 'component'),
    #                                     default=False, blank=True,  # null=True,
    #                                     # related_name='component_of',
    #                                     related_name="%(app_label)s_%(class)s_related",
    #                                     related_query_name="%(app_label)s_%(class)ss",
    #                                     )
    # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # object_id = models.PositiveIntegerField()
    # content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        abstract = True
        ordering = ['creation_date']


class Product(Entity):
    components = GM2MField(through='Portion', through_fields=('dish', 'component'))
    # components.add_relation('Product')

    def __repr__(self):
        return '<P: {}>'.format(self.name)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Meal(Entity):
    components = GM2MField(through='Portion', through_fields=('meal', 'component'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Прием пищи'
        verbose_name_plural = 'Приемы пищи'


class Portion(models.Model):
    dish = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, blank=True, null=True)
    component = GenericForeignKey(ct_field='component_ct', fk_field='component_fk')
    component_ct = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    component_fk = models.CharField(max_length=255)

    amount = models.IntegerField(default=0, verbose_name='Количество')

    def __str__(self):
        print(self.dish)
        print(self.meal)
        print(self.component)
        return f'{self.dish or self.meal}: {self.component}, {self.amount} г'

    class Meta:
        verbose_name = 'Порция'
        verbose_name_plural = 'Порции'


# class Portion(models.Model):
#     dish_meal = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     component = models.ForeignKey(Product, on_delete=models.CASCADE)
#     amount = models.IntegerField(default=0, verbose_name='Количество')


# class Portion(models.Model):
#     dishmeal_content_type = models.ForeignKey(ContentType, editable=False, related_name='%(app_label)s_%(class)s_as_dishmeal', on_delete=models.CASCADE)
#     dishmeal_object_id = models.PositiveIntegerField()
#     dishmeal = GenericForeignKey('dishmeal_content_type', 'dishmeal_object_id')

#     comps_content_type = models.ForeignKey(ContentType, editable=False, related_name='%(app_label)s_%(class)s_as_comps', on_delete=models.CASCADE)
#     comps_object_id = models.PositiveIntegerField()
#     comps = GenericForeignKey('comps_content_type', 'comps_object_id')


# class MealPortion(models.Model):
#     meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
#     component = models.ForeignKey(Product, on_delete=models.CASCADE)
#     amount = models.IntegerField(default=0, verbose_name='Количество')