from django.db import models
from ckeditor.fields import RichTextField


class Planet(models.Model):
    name = models.CharField(max_length=20, unique=True)
    angel = models.CharField(max_length=50)
    purpose = models.TextField()
    order_index = models.PositiveSmallIntegerField(unique=True, help_text="Order in 7-planet cycle (0-6)")

    class Meta:
        ordering = ["order_index"]

    def __str__(self) -> str:
        return f"{self.order_index}: {self.name} ({self.angel})"


class MagicalHour(models.Model):
    index = models.PositiveSmallIntegerField(unique=True, help_text="0-23")
    name = models.CharField(max_length=30, unique=True)
    details = RichTextField(blank=True, help_text="Rich text notes for this hour; appears after the general prayer on the page.")

    class Meta:
        ordering = ["index"]

    def __str__(self) -> str:
        return f"{self.index}: {self.name}"


class WeekdayStart(models.Model):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

    DAY_CHOICES = (
        (MONDAY, "Monday"),
        (TUESDAY, "Tuesday"),
        (WEDNESDAY, "Wednesday"),
        (THURSDAY, "Thursday"),
        (FRIDAY, "Friday"),
        (SATURDAY, "Saturday"),
        (SUNDAY, "Sunday"),
    )

    day = models.PositiveSmallIntegerField(choices=DAY_CHOICES, unique=True)
    planet = models.ForeignKey(Planet, on_delete=models.CASCADE, related_name="weekday_starts")

    class Meta:
        ordering = ["day"]
        verbose_name = "Weekday start"
        verbose_name_plural = "Weekday starts"

    def __str__(self) -> str:
        return f"{self.get_day_display()} → {self.planet.name}"
