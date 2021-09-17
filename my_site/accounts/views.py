from django.shortcuts import redirect, render
from django.http import HttpResponse
from datetime import date, datetime
from .models import Post
from django.urls import reverse
from hitcount.views import HitCountDetailView
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


def home(request):
    posts = Post.published.all()

    context = {
        "title": "HOME PAGE",
        "posts": posts,
    }
    return render(request, template_name="blogs/home.html", context=context)


def about(request):
    return render(request, template_name="blogs/about.html")


class PostListView(ListView):
    model = Post
    queryset = Post.published.all()
    template_name = "blogs/home.html"
    context_object_name = "posts"
    ordering = ["-published_at"]
    paginate_by = 2

    # def get_queryset(self):
    #   qs = super().get_queryset()
    #  return qs.filter(status="published")
    #  return self.model.published.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data()
        context_data["title"] = "BLOG HOME PAGE"
        return context_data


post_list_view = PostListView.as_view()


class PostDetailView(HitCountDetailView):
    model = Post
    count_hit = True


post_detail_view = PostDetailView.as_view()


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "content", "status"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("post-detail", kwargs={"pk": self.object.pk})


post_create_view = PostCreateView.as_view()


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


post_update_view = PostUpdateView.as_view()


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


post_delete_view = PostDeleteView.as_view()
