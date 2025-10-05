# created by Chirath R <chirath.02@gmail.com>
from django.http import Http404
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from technical_resources.models import Category, Link, File
from technical_resources.forms import CategoryForm, LinksForm, FilesForm


class CategoryListView(ListView):
    model = Category


class CategoryDetailView(DetailView):
    model = Category
    pk_url_kwarg = 'category'

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        links = Link.objects.filter(category=self.get_object())
        files = File.objects.filter(category=self.get_object())
        context['links'] = links
        context['files'] = files
        return context


class CategoryCreateView(CreateView):
    form_class = CategoryForm
    pk_url_kwarg = 'category'
    template_name = 'base/form.html'

    def get_context_data(self, **kwargs):
        context = super(CategoryCreateView, self).get_context_data(**kwargs)
        context['title'] = 'New Category'
        context['heading'] = 'Category'
        return context


class CategoryUpdateView(UpdateView):
    form_class = CategoryForm
    pk_url_kwarg = 'category'
    template_name = 'base/form.html'

    def get_context_data(self, **kwargs):
        context = super(CategoryUpdateView, self).get_context_data(**kwargs)
        context['title'] = self.get_object().name
        context['heading'] = 'Category'
        return context


class LinkCreateView(CreateView):
    form_class = LinksForm
    template_name = 'base/form.html'

    def get_success_url(self):
        return reverse('category_detail', kwargs={'category': self.kwargs.get('category', None)})

    def form_valid(self, form):
        try:
            category = Category.objects.get(id=str(self.kwargs.get('category', None)))
        except Category.DoesNotExist:
            raise Http404
        valid_form = super(LinkCreateView, self).form_valid(form)
        self.object.category = category
        self.object.save()
        return valid_form

    def get_context_data(self, **kwargs):
        context = super(LinkCreateView, self).get_context_data(**kwargs)
        context['title'] = 'New Link'
        context['heading'] = 'New Link'
        return context


class LinkUpdateView(UpdateView):
    form_class = LinksForm
    template_name = 'base/form.html'

    def get_success_url(self):
        return reverse('category_detail', kwargs={'category': self.kwargs.get('category', None)})

    def get_context_data(self, **kwargs):
        context = super(LinkUpdateView, self).get_context_data(**kwargs)
        context['title'] = self.get_object().name
        context['heading'] = 'Link'
        return context


class FileCreateView(CreateView):
    form_class = FilesForm
    template_name = 'base/form.html'

    def get_success_url(self):
        return reverse('category_detail', kwargs={'category': self.kwargs.get('category', None)})

    def form_valid(self, form):
        try:
            category = Category.objects.get(id=self.request.GET.get('category', None))
        except Category.DoesNotExist:
            raise Http404
        valid_form = super(FileCreateView, self).form_valid(form)
        self.object.category = category
        self.object.save()
        return valid_form

    def get_context_data(self, **kwargs):
        context = super(FileCreateView, self).get_context_data(**kwargs)
        context['title'] = 'New File'
        context['heading'] = 'New File'
        return context


class FileUpdateView(UpdateView):
    form_class = FilesForm
    template_name = 'base/form.html'

    def get_success_url(self):
        return reverse('category_detail', kwargs={'category': self.kwargs.get('category', None)})

    def get_context_data(self, **kwargs):
        context = super(FileUpdateView, self).get_context_data(**kwargs)
        context['title'] = self.get_object().name
        context['heading'] = 'File'
        return context
