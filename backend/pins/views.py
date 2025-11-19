from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q, Count
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Pin, Board, Comment
from .forms import PinForm, BoardForm, CommentForm, RegisterForm, LoginForm, SearchForm


def home(request):
    """Главная страница с лентой пинов"""
    pins = Pin.objects.select_related('user', 'board').prefetch_related('likes').all()

    # Поиск
    search_form = SearchForm(request.GET)
    if search_form.is_valid() and search_form.cleaned_data.get('query'):
        query = search_form.cleaned_data['query']
        pins = pins.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__icontains=query)
        )

    context = {
        'pins': pins,
        'search_form': search_form
    }
    return render(request, 'pins/home.html', context)


def pin_detail(request, pk):
    """Детальная страница пина"""
    pin = get_object_or_404(Pin.objects.select_related('user', 'board'), pk=pk)
    comments = pin.comments.select_related('user').all()

    comment_form = CommentForm()
    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.pin = pin
            comment.user = request.user
            comment.save()
            messages.success(request, 'Комментарий добавлен')
            return redirect('pin_detail', pk=pin.pk)

    context = {
        'pin': pin,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'pins/pin_detail.html', context)


@login_required
def pin_create(request):
    """Создание нового пина"""
    if request.method == 'POST':
        form = PinForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            pin = form.save(commit=False)
            pin.user = request.user
            pin.save()
            messages.success(request, 'Пин успешно создан!')
            return redirect('pin_detail', pk=pin.pk)
    else:
        form = PinForm(user=request.user)

    return render(request, 'pins/pin_form.html', {'form': form, 'title': 'Создать пин'})


@login_required
def pin_edit(request, pk):
    """Редактирование пина"""
    pin = get_object_or_404(Pin, pk=pk, user=request.user)

    if request.method == 'POST':
        form = PinForm(request.POST, request.FILES, instance=pin, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пин успешно обновлен!')
            return redirect('pin_detail', pk=pin.pk)
    else:
        form = PinForm(instance=pin, user=request.user)

    return render(request, 'pins/pin_form.html', {'form': form, 'title': 'Редактировать пин'})


@login_required
def pin_delete(request, pk):
    """Удаление пина"""
    pin = get_object_or_404(Pin, pk=pk, user=request.user)

    if request.method == 'POST':
        pin.delete()
        messages.success(request, 'Пин удален')
        return redirect('home')

    return render(request, 'pins/pin_confirm_delete.html', {'pin': pin})


@login_required
@require_POST
def pin_like(request, pk):
    """Лайк/анлайк пина (AJAX)"""
    pin = get_object_or_404(Pin, pk=pk)

    if pin.likes.filter(id=request.user.id).exists():
        pin.likes.remove(request.user)
        liked = False
    else:
        pin.likes.add(request.user)
        liked = True

    return JsonResponse({
        'liked': liked,
        'like_count': pin.like_count()
    })


def board_list(request):
    """Список всех публичных досок"""
    boards = Board.objects.filter(is_private=False).select_related('user').annotate(
        pins_count=Count('pins')
    )

    return render(request, 'pins/board_list.html', {'boards': boards})


def board_detail(request, slug):
    """Детальная страница доски"""
    board = get_object_or_404(Board.objects.select_related('user'), slug=slug)

    # Проверка доступа к приватной доске
    if board.is_private and (not request.user.is_authenticated or board.user != request.user):
        messages.error(request, 'У вас нет доступа к этой доске')
        return redirect('home')

    pins = board.pins.select_related('user').prefetch_related('likes').all()

    return render(request, 'pins/board_detail.html', {'board': board, 'pins': pins})


@login_required
def board_create(request):
    """Создание новой доски"""
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.user = request.user
            board.save()
            messages.success(request, 'Доска создана!')
            return redirect('board_detail', slug=board.slug)
    else:
        form = BoardForm()

    return render(request, 'pins/board_form.html', {'form': form, 'title': 'Создать доску'})


@login_required
def board_edit(request, slug):
    """Редактирование доски"""
    board = get_object_or_404(Board, slug=slug, user=request.user)

    if request.method == 'POST':
        form = BoardForm(request.POST, instance=board)
        if form.is_valid():
            form.save()
            messages.success(request, 'Доска обновлена!')
            return redirect('board_detail', slug=board.slug)
    else:
        form = BoardForm(instance=board)

    return render(request, 'pins/board_form.html', {'form': form, 'title': 'Редактировать доску'})


@login_required
def board_delete(request, slug):
    """Удаление доски"""
    board = get_object_or_404(Board, slug=slug, user=request.user)

    if request.method == 'POST':
        board.delete()
        messages.success(request, 'Доска удалена')
        return redirect('profile', username=request.user.username)

    return render(request, 'pins/board_confirm_delete.html', {'board': board})


def profile(request, username):
    """Профиль пользователя"""
    user = get_object_or_404(User, username=username)
    pins = Pin.objects.filter(user=user).select_related('board').prefetch_related('likes')

    if request.user == user:
        boards = Board.objects.filter(user=user).annotate(pins_count=Count('pins'))
    else:
        boards = Board.objects.filter(user=user, is_private=False).annotate(pins_count=Count('pins'))

    context = {
        'profile_user': user,
        'pins': pins,
        'boards': boards,
    }
    return render(request, 'pins/profile.html', context)


def register(request):
    """Регистрация нового пользователя"""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})


def user_login(request):
    """Вход пользователя"""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect(request.GET.get('next', 'home'))
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})


def user_logout(request):
    """Выход пользователя"""
    logout(request)
    messages.info(request, 'Вы вышли из системы')
    return redirect('home')
