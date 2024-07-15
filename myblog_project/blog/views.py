# blog/views.py

from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404
from .models import Page
from django.contrib.auth.decorators import login_required
from .forms import PageForm
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .models import Page, Comment
from .forms import CommentForm
from .forms import UserUpdateForm

def index(request):
    return render(request, 'blog/Index.html')

def about(request):
    return render(request, 'blog/about.html')

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Crear un nuevo usuario pero no guardarlo aún
            new_user = user_form.save(commit=False)
            # Establecer la contraseña proporcionada
            new_user.set_password(user_form.cleaned_data['password'])
            # Guardar el objeto User
            new_user.save()
            return render(request, 'blog/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'blog/register.html', {'user_form': user_form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # Redirige a la página principal después de iniciar sesión
            else:
                form.add_error(None, 'Usuario o contraseña incorrectos')
    else:
        form = AuthenticationForm()
    
    return render(request, 'blog/login.html', {'form': form})
            
def logout_view(request):
    logout(request)
    return redirect('index')  # Redirige a la página principal después de cerrar sesión         
       

def pages_list(request):
    pages = Page.objects.all()
    return render(request, 'blog/pages_list.html', {'pages': pages})


def page_detail(request, page_id):
    try:
        page = Page.objects.get(id=page_id)
    except Page.DoesNotExist:
        raise Http404("La página no existe.")

    comments = page.comments.all()

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.page = page
                comment.user = request.user
                comment.save()
                return redirect('page_detail', page_id=page.id)
        else:
            return redirect('login')
    else:
        form = CommentForm()

    return render(request, 'blog/page_detail.html', {'page': page, 'comments': comments, 'form': form})


@login_required
def page_edit(request, page_id):
    page = get_object_or_404(Page, pk=page_id)

    if request.method == 'POST':
        # Procesar el formulario de edición aquí
        # Ejemplo: Actualizar el título y contenido de la página
        page.title = request.POST.get('title')
        page.content = request.POST.get('content')
        page.save()
        return redirect('page_detail', page_id=page.id)

    return render(request, 'blog/page_edit.html', {'page': page})

@login_required
def page_delete(request, page_id):
    page = get_object_or_404(Page, pk=page_id)

    if request.method == 'POST':
        # Eliminar la página
        page.delete()
        return redirect('pages_list')

    return render(request, 'blog/page_delete.html', {'page': page})

@login_required
def page_create(request):
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save()  # Guardar la página en la base de datos
            return redirect('pages_list')  # Redirigir al listado de páginas
    else:
        form = PageForm()
    return render(request, 'blog/page_create.html', {'form': form})

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirigir a la página de perfil después de actualizar
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'blog/update_profile.html', {'form': form})

def profile(request):
    return render(request, 'blog/profile.html')