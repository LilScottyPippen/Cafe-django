from django.views.generic import TemplateView


class IndexView(TemplateView):
    """
    Класс шаблона главной страницы.
    """
    template_name = 'index/index.html'

    def get_context_data(self, **kwargs):
        """
        Инициализация шаблона.
        """
        context = super().get_context_data(**kwargs)
        return context
