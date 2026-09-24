from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Note


# Home page
def home(request):
    return render(
        request,
        'home.html',
        {'username': request.user.username}
    )


# Notes list page + Search
def notes_list(request):
    query = request.GET.get('q')

    if query:
        notes = Note.objects.filter(
            Q(title__icontains=query) |
            Q(subject__icontains=query) |
            Q(description__icontains=query)
        ).order_by('-uploaded_at')
    else:
        notes = Note.objects.all().order_by('-uploaded_at')

    return render(request, 'notes_list.html', {'notes': notes})


# My Notes
@login_required
def my_notes(request):
    notes = Note.objects.filter(
        uploaded_by=request.user
    ).order_by('-uploaded_at')

    return render(request, 'my_notes.html', {'notes': notes})


# View Note
@login_required
def view_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)

    return render(
        request,
        'view_note.html',
        {'note': note}
    )


# Add Note
@login_required
def add_note(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        subject = request.POST.get('subject')
        description = request.POST.get('description')
        file = request.FILES.get('file')

        Note.objects.create(
            title=title,
            subject=subject,
            description=description,
            file=file,
            uploaded_by=request.user,
        )

        messages.success(request, 'Note uploaded successfully!')

        return redirect('/my-notes/')

    return render(request, 'add_note.html')


# Edit Note
@login_required
def edit_note(request, note_id):
    note = get_object_or_404(
        Note,
        id=note_id,
        uploaded_by=request.user
    )

    if request.method == 'POST':
        note.title = request.POST.get('title')
        note.subject = request.POST.get('subject')
        note.description = request.POST.get('description')

        if request.FILES.get('file'):
            note.file = request.FILES.get('file')

        note.save()

        messages.success(request, 'Note updated successfully!')

        return redirect('/my-notes/')

    return render(
        request,
        'edit_note.html',
        {'note': note}
    )


# Delete Note
@login_required
def delete_note(request, note_id):
    note = get_object_or_404(
        Note,
        id=note_id,
        uploaded_by=request.user
    )

    if request.method == 'POST':
        note.delete()

        messages.success(
            request,
            'Note deleted successfully!'
        )

        return redirect('/my-notes/')

    return render(
        request,
        'delete_note.html',
        {'note': note}
    )


# Register page
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(
                request,
                'Username already exists!'
            )
            return redirect('/register/')

        User.objects.create_user(
            username=username,
            password=password
        )

        messages.success(
            request,
            'Registration successful! Please login.'
        )

        return redirect('/login/')

    return render(request, 'register.html')


# Login page
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('/')

        messages.error(
            request,
            'Invalid username or password!'
        )

    return render(request, 'login.html')


# Logout
def user_logout(request):
    logout(request)
    return redirect('/')