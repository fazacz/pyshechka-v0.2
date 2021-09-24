from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from gm2m import GM2MField


class Base(models.Model):
    name = models.CharField(unique=True, db_index=True, max_length=120)
    energy_value = models.FloatField(default=0)

    class Meta:
        abstract = True


class Product(Base):
    components = GM2MField(through='Portion', through_fields=('dish', 'component'))

    def __str__(self):
        return self.name


class Meal(Base):
    components = GM2MField(through='Portion', through_fields=('meal', 'component'))

    def __str__(self):
        return self.name


class Portion(models.Model):
    dish = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, blank=True, null=True)
    component = GenericForeignKey(ct_field='component_ct', fk_field='component_fk')
    component_ct = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    component_fk = models.CharField(max_length=255)
    amount = models.IntegerField(default=0)

    # def __str__(self):
    #     return self.name


'''
from main.models import Product, Meal, Portion
Product.objects.all()
Portion.objects.all()
Product.objects.create(name='Макароны отварные', energy_value=50)
m = Product.objects.all()[0]
mb = Product.objects.all()[1]
Portion.objects.create(dish=mb, component=m, amount=100)

por1 = Portion.objects.all()[0]

'''