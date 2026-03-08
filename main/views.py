from django.http import Http404
from django.shortcuts import render


SECTIONS = [
	{
		"slug": "forum",
		"title": "Форум",
		"description": "Обговорюйте теми, ставте запитання та діліться ідеями з командою.",
		"image": "https://images.unsplash.com/photo-1516321497487-e288fb19713f?auto=format&fit=crop&w=1200&q=80",
	},
	{
		"slug": "e-diary",
		"title": "Е-щоденник",
		"description": "Переглядайте оцінки, дедлайни та важливі записи в одному місці.",
		"image": "https://images.unsplash.com/photo-1455390582262-044cdead277a?auto=format&fit=crop&w=1200&q=80",
	},
	{
		"slug": "calendar",
		"title": "Календар подій",
		"description": "Плануйте зустрічі, контрольні та групові активності.",
		"image": "https://images.unsplash.com/photo-1506784983877-45594efa4cbe?auto=format&fit=crop&w=1200&q=80",
	},
	{
		"slug": "gallery",
		"title": "Галерея",
		"description": "Переглядайте фотоальбоми та медіа матеріали вашої групи.",
		"image": "https://images.unsplash.com/photo-1440581572325-0bea30075d9d?auto=format&fit=crop&w=1200&q=80",
	},
	{
		"slug": "portfolio",
		"title": "Портфоліо",
		"description": "Зберігайте свої роботи та відслідковуйте особистий прогрес.",
		"image": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1200&q=80",
	},
	{
		"slug": "vote-system",
		"title": "Голосування",
		"description": "Проводьте опитування та приймайте рішення більшістю голосів.",
		"image": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=1200&q=80",
	},
]


def home(request):
	return render(request, "main/home.html", {"sections": SECTIONS})


def section_page(request, section_slug):
	section = next((item for item in SECTIONS if item["slug"] == section_slug), None)
	if section is None:
		raise Http404("Сторінку не знайдено")

	return render(request, "main/section_page.html", {"section": section})
