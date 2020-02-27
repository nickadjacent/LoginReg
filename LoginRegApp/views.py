from django.shortcuts import render, redirect

from django.contrib import messages

from .models import *

import bcrypt


# ********** functions that render page **********


def index(request):
    print('rendering the index page')

    uid = request.session.get('email_session_id')
    if uid is not None:
        print('rendering the user dashboard page')

        return redirect('/user_dashboard')

    return render(request, 'index.html')


def user_dashboard(request):
    # only allow user into dashboard if they have session id
    if request.session.get('email_session_id') == None:
        print('no session in email_session_id')
        return redirect('/')

    context = {
        'user': User.objects.get(email=request.session['email_session_id'])
    }
    # load all users in DB

    print('rendering the user dashboard page')
    return render(request, 'user_dashboard.html', context)


# ***** functions that redirect to render page *****


def register(request):
    print(request.POST)
    print('registering a new user')

    # check first for validations (password match, etc...)
    if len(request.POST['password']) < 3:
        messages.error(request, 'Password is too short')
    if request.POST['password_confirm'] != request.POST['password']:
        messages.error(request, 'Passwords do not match')
    if len(request.POST['email']) < 3:
        messages.error(request, 'Email is too short')

    error_messages = messages.get_messages(request)
    error_messages.used = False
    if len(error_messages) > 0:
        return redirect('/')

    # code some stuff to register a user in DB
    # before creating a user, check for uniqueness
    # check DB for the email
    user_in_db = User.objects.filter(email=request.POST['email'])
    if len(user_in_db) > 0:
        print('Email already exists')
        messages.error(request, "There was a problem.")
        return redirect('/')
    else:
        hashed_pw = bcrypt.hashpw(
            request.POST['password'].encode(), bcrypt.gensalt()).decode()
        print('hashed_pw:', hashed_pw)
        user = User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            password=hashed_pw,
        )
        # add new user to session
        request.session['email_session_id'] = user.email
        return redirect('/user_dashboard')


def login(request):
    print(request.POST)
    print('logging in a user')

    # check to see if email exists in DB
    user = User.objects.filter(email=request.POST['email'])
    if len(user) == 1:
        print('user found -> logging user in')
        if bcrypt.checkpw(request.POST['password'].encode(), user[0].password.encode()):
            print("password match")
            # start a session when a user logs in
            print('creating email_session_id for user')
            request.session['email_session_id'] = user[0].email
            return redirect('/user_dashboard')
        else:
            print("failed password")
            messages.error(request, "There was an error.")
        return redirect('/')
    else:
        print('no user found')
        messages.error(request, "There was an error.")
        return redirect('/')


def logout(request):
    print('loggin out user')
    print('clearing session email_session_id')
    request.session.clear()
    return redirect('/')
