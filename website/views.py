from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddNoteForm
from .models import Note 

# Create your views here.
def home(request):
    notes = []
    if request.user.is_authenticated:
        notes = Note.objects.filter(user = request.user).order_by("-created_at")
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        #authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully logged in")
            return redirect('home')
        else:
            messages.success(request, "There was an error logging you in. Pls try again.")
            return redirect('home')
    else:
        return render(request, 'home.html', {'notes': notes})

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect('home')

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            #authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You have successfully registered')
            return redirect('home')
    else:
        form = SignUpForm()
        # return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', {'form': form})
    
def add_note(request):
    form = AddNoteForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid:
                note = form.save(commit=False)
                note.user = request.user
                note.save()
                messages.success(request, "Note Added")
                return redirect('add_note')
        
        return render(request, 'add_note.html', {'form': form})
    
    else:
        messages.success(request, "You must be logged in")
        return redirect('home')

def view_note(request, pk):
    if request.user.is_authenticated:
        note = Note.objects.get(id = pk)
        return render(request, 'note.html', {'note': note})
    else:
        messages.success(request, "You must be logged in to view the notes")
        return redirect('home')
    
def delete_note(request, pk):
    if request.user.is_authenticated:
        note = Note.objects.get(id=pk)
        note.delete()
        messages.success(request, "Note Deleted Successfully")
        return redirect('home')
    else:
        messages.success(request, "You must be logged in to perform this action")
        return redirect('home')

def update_note(request, pk):
    if request.user.is_authenticated:
        old_note = Note.objects.get(id=pk)
        form = AddNoteForm(request.POST or None, instance=old_note)
        if form.is_valid():
            form.save()
            messages.success(request, "Note Updated Successfully")
            return redirect('home')
        return render(request, 'update_note.html', {'form': form})
    else:
        messages.success(request, "You must be logged in to perform this action")
        return redirect('home')
