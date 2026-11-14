from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView,
)
from .forms import EntryForm
from .models import Entry


class EntryListView(LoginRequiredMixin, ListView):
    model = Entry
    template_name = "diary/entry_list.html"
    context_object_name = "entries"
    paginate_by = 10

    def get_queryset(self):
        qs = Entry.objects.filter(user=self.request.user)
        query = self.request.GET.get("q", "").strip()
        if query:
            qs = qs.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "")
        return context


class EntryDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Entry
    template_name = "diary/entry_detail.html"

    def test_func(self):
        return self.get_object().user == self.request.user


class EntryCreateView(LoginRequiredMixin, CreateView):
    model = Entry
    form_class = EntryForm
    template_name = "diary/entry_form.html"
    success_url = reverse_lazy('diary:entry-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EntryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Entry
    form_class = EntryForm
    template_name = "diary/entry_form.html"
    success_url = reverse_lazy('diary:entry-list')

    def test_func(self):
        return self.get_object().user == self.request.user


class EntryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Entry
    template_name = "diary/entry_confirm_delete.html"
    success_url = reverse_lazy("diary:entry-list")

    def test_func(self):
        return self.get_object().user == self.request.user


class HomeView(TemplateView):
    template_name = 'home.html'