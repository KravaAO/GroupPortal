import calendar
import json
from collections import defaultdict
from datetime import date, datetime

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST

from .models import CalendarEvent


def month_view(request):
	today = date.today()

	try:
		year = int(request.GET.get("year", today.year))
	except (TypeError, ValueError):
		year = today.year

	try:
		month = int(request.GET.get("month", today.month))
	except (TypeError, ValueError):
		month = today.month

	if month < 1 or month > 12:
		month = today.month

	month_calendar = calendar.Calendar(firstweekday=0).monthdatescalendar(year, month)

	month_start = date(year, month, 1)
	month_end = date(year + (month // 12), ((month % 12) + 1), 1)

	events = CalendarEvent.objects.filter(date__gte=month_start, date__lt=month_end)
	events_by_day = defaultdict(list)
	for event in events:
		events_by_day[event.date].append(event)

	prev_month = 12 if month == 1 else month - 1
	prev_year = year - 1 if month == 1 else year
	next_month = 1 if month == 12 else month + 1
	next_year = year + 1 if month == 12 else year

	weeks_data = []
	for week in month_calendar:
		week_data = []
		for day in week:
			week_data.append(
				{
					"date": day,
					"in_month": day.month == month,
					"is_today": day == today,
					"events": events_by_day.get(day, []),
				}
			)
		weeks_data.append(week_data)

	context = {
		"year": year,
		"month": month,
		"month_name": calendar.month_name[month],
		"weeks_data": weeks_data,
		"today": today,
		"week_day_names": ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Нд"],
		"prev_month": prev_month,
		"prev_year": prev_year,
		"next_month": next_month,
		"next_year": next_year,
	}
	return render(request, "event_calendar/calendar.html", context)


@require_GET
def day_events(request):
	date_str = request.GET.get("date", "")
	try:
		day = datetime.strptime(date_str, "%Y-%m-%d").date()
	except ValueError:
		return JsonResponse({"error": "Invalid date"}, status=400)

	events = CalendarEvent.objects.filter(date=day)
	data = [
		{
			"id": e.id,
			"title": e.title,
			"start_time": e.start_time.strftime("%H:%M") if e.start_time else None,
			"end_time": e.end_time.strftime("%H:%M") if e.end_time else None,
			"description": e.description,
		}
		for e in events
	]
	return JsonResponse({"events": data})


@require_POST
def add_event(request):
	try:
		body = json.loads(request.body)
	except json.JSONDecodeError:
		return JsonResponse({"error": "Invalid JSON"}, status=400)

	title = body.get("title", "").strip()
	date_str = body.get("date", "")
	start_time = body.get("start_time") or None
	end_time = body.get("end_time") or None
	description = body.get("description", "")

	if not title:
		return JsonResponse({"error": "Назва події обов'язкова"}, status=400)

	try:
		day = datetime.strptime(date_str, "%Y-%m-%d").date()
	except ValueError:
		return JsonResponse({"error": "Невірна дата"}, status=400)

	event = CalendarEvent.objects.create(
		title=title,
		date=day,
		start_time=start_time,
		end_time=end_time,
		description=description,
	)

	def fmt_time(t):
		if t is None:
			return None
		# after .create() the field may still be a raw string
		if hasattr(t, 'strftime'):
			return t.strftime("%H:%M")
		return str(t)[:5]

	return JsonResponse({
		"id": event.id,
		"title": event.title,
		"start_time": fmt_time(event.start_time),
		"end_time": fmt_time(event.end_time),
		"description": event.description,
	})


@require_POST
def delete_event(request, event_id):
	try:
		event = CalendarEvent.objects.get(pk=event_id)
	except CalendarEvent.DoesNotExist:
		return JsonResponse({"error": "Подію не знайдено"}, status=404)
	event.delete()
	return JsonResponse({"ok": True})
