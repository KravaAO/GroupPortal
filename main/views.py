from django.http import Http404
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render


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
	{
		"slug": "developers",
		"title": "Про розробників",
		"description": "Дізнайтеся про команду, яка створила GroupPortal, та ключові ролі в розробці.",
		"image": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=1200&q=80",
	},
]


DEVELOPERS = [
	{
		"full_name": "Ковальов Назар Миколайович",
		"role": "main",
		"email": "nazark1306@gmail.com",
		"photo": "/static/main/nazar.jpg",
	},
	{
		"full_name": "Кравчук Артем",
		"role": "Лідер команди",
		"email": "???@gmail.com",
		"photo": "/static/main/artem.jpg",
	},
	{
		"full_name": "Ніколетта Ланґур",
		"role": "Користувачі",
		"email": "???@gmail.com",
		"photo": "/static/main/nikoleta.jpg",
	},
	{
		"full_name": "Олег Атрасевич",
		"role": "Портфоліо",
		"email": "???@gmail.com",
		"photo": "/static/main/oleg.jpg",
	},
	{
		"full_name": "Нікіта Зубенко",
		"role": "Пости",
		"email": "???@gmail.com",
		"photo": "/static/main/o.jpg",
	},
	{
		"full_name": "Кіріл Хлібородов",
		"role": "менеджер щоденника",
		"email": "???@gmail.com",
		"photo": "/static/main/kiril.jpg",
	},
]


def home(request):
	return render(request, "main/home.html", {"sections": SECTIONS})


def section_page(request, section_slug):
	section = next((item for item in SECTIONS if item["slug"] == section_slug), None)
	if section is None:
		raise Http404("Сторінку не знайдено")

	if section_slug == "calendar":
		return redirect("event_calendar:month_view")

	if section_slug == "developers":
		User = get_user_model()
		users = User.objects.filter(is_active=True).order_by("username")

		developers_from_db = []
		for user in users:
			full_name = user.get_full_name().strip() if hasattr(user, "get_full_name") else ""
			display_name = full_name or user.username
			role = "Адміністратор" if user.is_superuser else ("Модератор" if user.is_staff else "Учасник")
			email = user.email or "Не вказано"
			photo = f"https://ui-avatars.com/api/?name={display_name.replace(' ', '+')}&background=1f2937&color=ffffff&size=512"

			developers_from_db.append(
				{
					"full_name": display_name,
					"role": role,
					"email": email,
					"photo": photo,
				}
			)

		developers = developers_from_db if developers_from_db else DEVELOPERS

		return render(
			request,
			"main/developers_page.html",
			{"section": section, "developers": developers},
		)

	return render(request, "main/section_page.html", {"section": section})
