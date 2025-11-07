from django.utils import timezone
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
import datetime as dt
from .models import Planet, MagicalHour, WeekdayStart

GENERAL_PRAYER = (
    "O Lord All Powerful, Eternal God and Father of all Creatures, shed upon me the Divine Influence of Thy Mercy, "
    "for I am Thy Creature. I beseech Thee to defend me from mine Enemies, and to confirm in me true and steadfast faith. "
    "O Lord, I commit my Body and my Soul unto Thee, seeing I put my trust in none beside Thee; it is on Thee alone that I rely; "
    "O Lord my God aid me; O Lord hear me in the day and hour wherein I shall invoke Thee."
)


def current_prayer(request: HttpRequest) -> HttpResponse:
    now = timezone.localtime()  # localized to Africa/Lagos via settings

    day_index = now.weekday()   # Monday=0..Sunday=6
    hour = now.hour             # 0..23

    # Get starting planet for the weekday
    try:
        start = WeekdayStart.objects.select_related("planet").get(day=day_index)
    except WeekdayStart.DoesNotExist:
        return render(request, "timetable/current.html", {
            "now": now,
            "day_name": now.strftime("%A"),
            "hour_range": f"{now.replace(minute=0, second=0, microsecond=0).strftime('%I:%M %p')} - "
                           f"{(now.replace(minute=0, second=0, microsecond=0) + dt.timedelta(hours=1)).strftime('%I:%M %p')}",
            "magical_hour": f"Hour {hour}",
            "planet": "(not configured)",
            "angel": "(add in Admin)",
            "purpose": "Please load initial data or configure planets and weekday starts in Admin.",
            "general_prayer": GENERAL_PRAYER,
        })

    total_planets = Planet.objects.count() or 7
    planet_idx = (start.planet.order_index + hour) % total_planets

    try:
        planet = Planet.objects.get(order_index=planet_idx)
    except Planet.DoesNotExist:
        planet = start.planet  # fallback to starting planet

    try:
        hour_obj = MagicalHour.objects.get(index=hour)
        magical_hour_name = hour_obj.name
        hour_details = hour_obj.details
    except MagicalHour.DoesNotExist:
        magical_hour_name = f"Hour {hour}"
        hour_details = ""

    context = {
        "now": now,
        "day_name": now.strftime("%A"),
        "hour_range": f"{now.replace(minute=0, second=0, microsecond=0).strftime('%I:%M %p')} - "
                        f"{(now.replace(minute=0, second=0, microsecond=0) + dt.timedelta(hours=1)).strftime('%I:%M %p')}",
        "magical_hour": magical_hour_name,
        "planet": planet.name,
        "angel": planet.angel,
        "purpose": planet.purpose,
        "general_prayer": GENERAL_PRAYER,
        "hour_details": hour_details,
    }

    return render(request, "timetable/current.html", context)
