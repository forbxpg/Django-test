from django.shortcuts import render, redirect


def index(request):
    """Главная страница сайта."""
    return redirect("ads:ads-list")


def page_not_found(request, exception):
    """Обработчик страницы 404."""
    return render(request, "pages/404.html", status=404)


def server_error(request):
    """Отображение для Server Error."""
    return render(request, "pages/500.html", status=500)
