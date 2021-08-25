from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

# Create your views here.
def index(request):
    return render(request,'index.html')

def success(request):
    return render(request,'success.html')

def register(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode())
        request.session['user_id'] = user.id
        request.session['greeting'] = user.first_name
        return redirect('/success')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.get(email=request.POST['login_email'])
        request.session['user_id'] = user.id
        request.session['greeting'] = user.first_name
        return redirect('/quotes')

def show_all(request):
    if "user_id" not in request.session:
        return redirect('/')
    else:
        context = {
            'all_quotes': Quote.objects.all(),
            'this_user': User.objects.get(id=request.session['user_id']),
        }
        return render(request,'quotes.html',context)

def create_quote(request):
    errors = Quote.objects.quote_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/quotes')
    else:
        user = User.objects.get(id=request.session["user_id"])
        quote = Quote.objects.create(
            quotee = request.POST['quotee'],
            message = request.POST['message'],
            creator = user
        )
        return redirect(f'/quotes')

def show_one(request, user_id):
    context = {
        'user': User.objects.get(id=user_id),
        'current_user': User.objects.get(id=request.session['user_id'])
    }
    return render(request,"users.html",context)

def edit(request,quote_id):
    context = {
        'quote': Quote.objects.get(id=quote_id)
    }
    return render(request,'edit.html',context)

def update(request, quote_id):
    errors = Quote.objects.quote_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/quotes/{quote_id}/edit')
    else:
        quote = Quote.objects.get(id=quote_id)
        quote.quotee = request.POST['quotee']
        quote.message = request.POST['message']
        quote.save()
    return redirect(f'/quotes')

def delete(request, quote_id):
    quote = Quote.objects.get(id=quote_id)
    quote.delete()
    return redirect(f'/quotes')

def favorite(request, quote_id):
    user = User.objects.get(id=request.session["user_id"])
    quote = Quote.objects.get(id=quote_id)
    user.favorited_quotes.add(quote)
    return redirect(f'/quotes')

def unfavorite(request, quote_id):
    user = User.objects.get(id=request.session["user_id"])
    quote = Quote.objects.get(id=quote_id)
    user.favorited_quotes.remove(quote)
    return redirect(f'/quotes')

def logout(request):
    request.session.flush()
    return redirect('/')