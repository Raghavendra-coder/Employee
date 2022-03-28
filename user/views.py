from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import Leaves, User
from .forms import UserForm, EditUserForm, LeaveForm, LoginForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required


def index(request):
    context = {

    }
    return render(request, 'user/index.html', context)


def employee_signup(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect('home')
    form = UserForm()
    login_form = LoginForm()
    if request.method == 'POST':
        if 'signup' in request.POST:
            form = UserForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.role = 'E'
                password = form.cleaned_data['password']
                user.set_password(password)
                user.save()
                login(request, user)
                messages.success(request, f'Congratulations {user.first_name}! Your account has been created successfully')
                return redirect('home')
        elif 'login' in request.POST:
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                user = login_form.login(request)
                login(request, user)
                messages.success(request, "You have been logged in.")
                return redirect('home')

    context = {
        'form': form,
        'login_form': login_form,
    }
    return render(request, 'user/signup.html', context)


def user_logout(request):
    logout(request)
    messages.success(request, "Logout successfully!")
    return redirect('home')


@login_required(login_url='employee_signup')
def edit_profile(request):
    form = EditUserForm(instance=request.user)
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile has been updated successfully')
            return redirect('home')

    context = {
        'form': form,
    }
    return render(request, 'user/signup.html', context)


@login_required(login_url='employee_signup')
def leave_request(request):
    form = LeaveForm()
    if request.user.is_superuser:
        leaves_qry = Leaves.objects.all().select_related('user')
    else:
        leaves_qry = Leaves.objects.filter(user=request.user).select_related('user')

    paginator = Paginator(leaves_qry, 15)
    page = request.GET.get('page')
    try:
        leaves = paginator.get_page(page)
    except PageNotAnInteger:
        leaves = paginator.get_page(1)
    except EmptyPage:
        leaves = paginator.get_page(paginator.num_pages)
    page_range = list(paginator.page_range)
    if request.method == 'POST':
        if 'leave-request' in request.POST:
            form = LeaveForm(request.POST, request.FILES)
            if form.is_valid():
                leave = form.save(commit=False)
                leave.user = request.user
                leave.save()
                messages.success(request, 'Your leave application has been submitted successfully.')
                return redirect('home')
        elif 'leave-status' in request.POST:
            leave_pk = request.POST['pk']
            leave_status = request.POST['status']
            leave_qry = Leaves.objects.filter(pk=leave_pk).first()
            if leave_qry:
                leave_qry.status = leave_status
                leave_qry.save()
                messages.success(request, f'Status has been updated for leave request "{leave_pk}"')
                return redirect('leave_request')

    context = {
        'form': form,
        'leaves': leaves,
        'page_range': page_range,
    }
    return render(request, 'user/leaves.html', context)


