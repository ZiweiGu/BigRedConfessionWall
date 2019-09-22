from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from .models import Post, Preference
from .forms import PostModelForm

# CRUD

def post_list_view(request):
	"""
	List out objects, (could be used in the search view as well)
	"""
	qs = Post.objects.all().published() # queryset: list of python objects
	if request.user.is_authenticated:
		my_qs = Post.objects.filter(user=request.user)
		qs = (qs | my_qs).distinct()
	template_name = 'post/list.html'
	context = {'object_list': qs}
	return render(request, template_name, context)

@login_required(login_url='/login')
@staff_member_required
def post_create_view(request):
	"""
	create objects using forms
	"""
	form = PostModelForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		# print(form.cleaned_data)
		# obj = form.save(commit=False)
		# obj.title = form.cleaned_data.get('title') + '0'
		# obj.save()
		obj = form.save(commit=False)
		obj.user = request.user
		obj.save()
		form = PostModelForm()
	template_name = 'form.html'
	context = {'form': form}
	return render(request, template_name, context)

def post_detail_view(request, slug):
	"""
	1 object -> detail view
	"""
	obj = get_object_or_404(Post, slug=slug)
	template_name = 'post/detail.html'
	context = {"object": obj}
	return render(request, template_name, context)

@staff_member_required
def post_update_view(request, slug):
	obj = get_object_or_404(Post, slug=slug)
	form = PostModelForm(request.POST or None, instance=obj)
	if form.is_valid():
		form.save()
	template_name = 'form.html'
	context = {'form': form, 'title': f'Update {obj.content}'}
	return render(request, template_name, context)

@staff_member_required
def post_delete_view(request, slug):
	obj = get_object_or_404(Post, slug=slug)
	template_name = 'post/delete.html'
	if request.method == 'POST':
		obj.delete()
		return redirect('/post')
	context = {"object": obj}
	return render(request, template_name, context)

def postpreference(request, postid, userpreference):
    if request.method == "POST":
        eachpost= get_object_or_404(Post, id=postid)
        # print(postid)
        obj=''
        valueobj=''
        try:
            obj= Preference.objects.get(user= request.user, post= eachpost)
            valueobj= obj.value #value of userpreference
            valueobj= int(valueobj)
            userpreference= int(userpreference)          
            if valueobj != userpreference:
                obj.delete()
                upref= Preference()
                upref.user= request.user
                upref.post= eachpost
                upref.value= userpreference
                if userpreference == 1 and valueobj != 1:
                    eachpost.likes += 1
                    eachpost.dislikes -=1
                elif userpreference == 2 and valueobj != 2:
                    eachpost.dislikes += 1
                    eachpost.likes -= 1
                upref.save()
                eachpost.save()
                return render(request, 'post/detail.html', {"object": eachpost})
            elif valueobj == userpreference:
                obj.delete()                       
                if userpreference == 1:
                    eachpost.likes -= 1
                elif userpreference == 2:
                    eachpost.dislikes -= 1
                eachpost.save()
                return render(request, 'post/detail.html', {"object": eachpost})
        except Preference.DoesNotExist:
            upref= Preference()
            upref.user= request.user
            upref.post= eachpost
            upref.value= userpreference
            userpreference= int(userpreference)
            if userpreference == 1:
                eachpost.likes += 1
            elif userpreference == 2:
                eachpost.dislikes +=1
            upref.save()
            eachpost.save()                            
            return render(request, 'post/detail.html', {"object": eachpost})
    else:
        return render(request, 'post/detail.html', {"object": eachpost})
              





