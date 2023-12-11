from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.search import TrigramSimilarity
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import FormView, UpdateView
from django.views.generic import TemplateView
from django.core.mail import send_mail

from actions.utils import create_action
from .forms import AddNomenclatureForm, EmailNomenclatureForm,  AddCategoryForm, SearchForm
from .models import Nomenclature, Category, get_new_barcode


class NomenclatureHome(TemplateView):
    template_name = 'catalog/index.html'
    extra_context = {
        'title': 'Главная страница',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nomenclature_list'] = Nomenclature.objects.all()
        context['get_test_data'] = self.request.GET.get('test')
        return context


class NomenclatureListView(generic.ListView):
    model = Nomenclature
    paginate_by = 10
    queryset = Nomenclature.objects.all()
    context_object_name = 'nomenclature_list'
    template_name = 'catalog/nomenclature-list.html'


class CategoryListView(generic.ListView):
    model = Category
    paginate_by = 10
    queryset = Category.objects.all()
    context_object_name = 'cats'
    template_name = 'catalog/list-category.html'


class AddNomenclature(LoginRequiredMixin, FormView):
    form_class = AddNomenclatureForm
    template_name = 'catalog/add_nomenclature.html'
    success_url = reverse_lazy('nomenclature-list-view')
    extra_context = {
        'title': 'Добавление номенклатуры'
    }

    def __init__(self, **kwargs):
        self.initial = {'barcode': get_new_barcode()}

    def form_valid(self, form):
        form.instance.user = self.request.user
        nom = form.save(commit=False)
        form.save()
        create_action(self.request.user, 'Добавление номенклатуры', nom)
        messages.success(self.request, 'Создание номенклатуры: успешно')
        return super(AddNomenclature, self).form_valid(form)


class EditNomenclature(LoginRequiredMixin, UpdateView):
    model = Nomenclature
    fields = ['name', 'cost', 'weight_or_piece', 'barcode',
              'slug', 'user', 'category', 'country_made']
    template_name = 'catalog/add_nomenclature.html'
    success_url = reverse_lazy('nomenclature-list-view')
    extra_context = {
        'title': 'Изменение номенклатуры'
    }

    def form_valid(self, form):
        form.instance.user = self.request.user
        nom = form.save(commit=False)
        form.save()
        create_action(self.request.user, 'Изменение номенклатуры', nom)
        messages.success(self.request, 'Изменение номенклатуры: успешно')
        return super(EditNomenclature, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Page update failed')
        return super(EditNomenclature, self).form_valid(form)


class EditCategory(LoginRequiredMixin, UpdateView):
    model = Category
    fields = ['name', 'slug',]
    template_name = 'catalog/add_category.html'
    success_url = reverse_lazy('list-category')
    extra_context = {
        'title': 'Изменение категории'
    }

    def form_valid(self, form):
        form.instance.user = self.request.user
        category = form.save(commit=False)
        form.save()
        create_action(self.request.user, 'Изменение категории',
                      category)
        messages.success(self.request, 'Изменение категории: успешно')
        return super(EditCategory, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Category update failed')
        return super(EditCategory, self).form_valid(form)


class AddCategory(LoginRequiredMixin, FormView):
    form_class = AddCategoryForm
    template_name = 'catalog/add_category.html'
    success_url = reverse_lazy('list-category')

    def form_valid(self, form):
        messages.success(self.request, 'Добавление категории: успешно')
        form.save()
        create_action(self.request.user, 'Добавление категории',
                      self.request.category)
        return super().form_valid(form)


class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    model = Category


class NomenclatureDetailView(LoginRequiredMixin, generic.DetailView):
    model = Nomenclature


@login_required
def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    nomenclatures = Nomenclature.objects.filter(category_id=category.pk)
    data = {
        'title': f'Категория товара: {category.name}',
        'noms': nomenclatures,
        'cat_selected': category.pk,
    }
    return render(request, 'catalog/category.html', data)


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1> Страница не найдена! </h1>")


def nom_share(request, nom_id):
    nom = get_object_or_404(Nomenclature, id=nom_id)

    sent = False

    if request.method == 'POST':
        form = EmailNomenclatureForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            nom_url = request.build_absolute_uri(nom.get_absolute_url())
            subject = f"{cd['name']} recommends you read"\
                      f"{nom.name} {nom_url}"
            message = f"{nom.name}\n{nom.barcode}\n{nom.category}\n{nom.cost}"
            send_mail(subject, message, 'muqqyjmuqq@gmail.com',
                      [cd['to']])
            sent = True
    else:
        form = EmailNomenclatureForm()
    return render(request, 'catalog/share-nom.html', {'nom': nom, 'form': form, 'sent': sent})


def nom_search(request):
    form = SearchForm()
    query = None
    results = []
    print(request.GET)

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Nomenclature.objects.annotate(
                similarity=TrigramSimilarity('name', query),
            ).filter(similarity__gt=0.1).order_by('-similarity')

    return render(request,
                  'catalog/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})


def index(request):
    nomenclature_list = Nomenclature.objects.all()
    return render(request, 'catalog/index.html',
                  context={'nomenclature_list': nomenclature_list, })
