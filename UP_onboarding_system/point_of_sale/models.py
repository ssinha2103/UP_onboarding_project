from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    MERCHANT = 1
    CONSUMER = 2

    ROLE_CHOICES = (
        (MERCHANT, 'MERCHANT'),
        (CONSUMER, 'CONSUMER')
    )

    name = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=2)

    def __str__(self):
        return self.name


class Stores(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    lat = models.FloatField()
    lng = models.FloatField()
    merchant = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="stores")

    def __str__(self):
        return "{}: {}".format(self.name, self.address)

    class Meta:
        verbose_name_plural = 'Stores'


class Items(models.Model):
    name = models.CharField(max_length=50, unique=False)
    price = models.IntegerField()
    description = models.TextField()
    stores = models.ForeignKey(Stores, on_delete=models.CASCADE, related_name="items")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Items"
        unique_together = ('name', 'stores',)


class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    merchant = models.ForeignKey(Profile, on_delete=models.CASCADE)
    store = models.ForeignKey(Stores, on_delete=models.CASCADE)
    items = models.ManyToManyField(Items)

    class Meta:
        verbose_name_plural = "Orders"
