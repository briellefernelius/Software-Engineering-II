from django.db import models
from users.models import CustomUser
# Create your models here.


MONTH_CHOICES = (
    (1, '01 (Jan)'),
    (2, '02 (Feb)'),
    (3, '03 (Mar)'),
    (4, '04 (Apr)'),
    (5, '05 (May)'),
    (6, '06 (Jun)'),
    (7, '07 (Jul)'),
    (8, '08 (Aug)'),
    (9, '09 (Sep)'),
    (10, '10 (Oct)'),
    (11, '11 (Nov)'),
    (12, '12 (Dec)'),
)

YEAR_CHOICES = (
    (2022, '2022'),
    (2023, '2023'),
    (2024, '2024'),
    (2025, '2025'),
    (2026, '2026'),
    (2027, '2027'),
    (2028, '2028'),
    (2029, '2029'),
    (2030, '2030'),
    (2031, '2031'),
    (2032, '2032'),
    (2033, '2033'),
    (2034, '2034'),
    (2035, '2035'),
)


class Account(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    cardholder_name = models.CharField(max_length=50, default="", null=True)
    card_number = models.IntegerField()
    expiration_date = models.DateField(null=True)
    expiration_month = models.IntegerField(null=True, choices=MONTH_CHOICES)
    expiration_year = models.IntegerField(null=True, choices=YEAR_CHOICES)
    cvc_number = models.IntegerField(max_length=4)
    amount = models.IntegerField(null=True)

    def __str__(self):
        return str(self.user) + " Cardholder name: " + self.cardholder_name
