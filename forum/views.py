from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from .models import Thread, Post
from .forms import ThreadForm, PostForm


def _staff_check(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


def thread_list(request):
    """Display a list of all threads."""
    threads = Thread.objects.order_by("-created_at")
    return render(request, "forum/thread_list.html", {"threads": threads})


@login_required
def thread_detail(request, pk):
    """Show a single thread and its posts; allow logged-in users to reply."""
    thread = get_object_or_404(Thread, pk=pk)
    posts = thread.posts.order_by("created_at")

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.thread = thread
            post.created_by = request.user
            post.save()
            messages.success(request, "Your message has been posted.")
            return redirect("forum:thread_detail", pk=pk)
    else:
        form = PostForm()

    return render(
        request,
        "forum/thread_detail.html",
        {"thread": thread, "posts": posts, "form": form},
    )


@user_passes_test(_staff_check)
def create_thread(request):
    """Allow admins/moderators to create new threads."""
    if request.method == "POST":
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.created_by = request.user
            thread.save()
            messages.success(request, "Thread created successfully.")
            return redirect("forum:thread_detail", pk=thread.pk)
    else:
        form = ThreadForm()
    return render(request, "forum/thread_form.html", {"form": form, "action": "Create"})


@user_passes_test(_staff_check)
def edit_thread(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    if request.method == "POST":
        form = ThreadForm(request.POST, instance=thread)
        if form.is_valid():
            form.save()
            messages.success(request, "Thread updated successfully.")
            return redirect("forum:thread_detail", pk=pk)
    else:
        form = ThreadForm(instance=thread)
    return render(request, "forum/thread_form.html", {"form": form, "action": "Edit"})


@user_passes_test(_staff_check)
def delete_thread(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    if request.method == "POST":
        thread.delete()
        messages.success(request, "Thread deleted.")
        return redirect("forum:thread_list")
    return render(request, "forum/thread_confirm_delete.html", {"thread": thread})
