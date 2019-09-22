from django.http import HttpResponse
from django.shortcuts import render

from datetime import date

from .forms import ContactForm
from wall.models import Post

today = date.today().strftime("%B %d, %Y")



def home_page(request):
	qs = Post.objects.all()[:5]
	context = {"title": "", 'post_list': qs, 'date': today}
	return render(request, "home.html", context)



def login_page(request):
	return render(request, 'login.html')

def contact_page(request):
	form = ContactForm(request.POST or None)
	if form.is_valid():
		print(form.cleaned_data)
		form = ContactForm()
	context = {
		'title': 'Contact Us',
		'form': form
	}
	return render(request, 'form.html', context)