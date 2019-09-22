from django import forms
from .models import Post

class PostForm(forms.Form):
	slug = forms.SlugField()
	content = forms.CharField(widget=forms.Textarea)

class PostModelForm(forms.ModelForm):
	class Meta:
		model = Post
		fields=['content']
		# fields = ['slug', 'content', 'publish_date']
		# fields = ['slug', 'image', 'content', 'publish_date']

	def clean_content(self, *args, **kwargs):
		# print(dir(self))
		instance = self.instance
		print(instance)
		content = self.cleaned_data.get('content')
		qs = Post.objects.filter(content__iexact=content)
		if instance:
			qs = qs.exclude(pk=instance.pk) # id=instance.id, avoid validation error on update
		if qs.exists():
			raise forms.ValidationError('This content already exists. Please try again.')
		return content

