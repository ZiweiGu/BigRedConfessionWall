from django import forms
from .models import Post, Comment

class PostForm(forms.Form):
    slug = forms.SlugField()
    content = forms.CharField(widget=forms.Textarea)

class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields=['content']
        # fields = ['slug', 'content', 'publish_date']
        # fields = ['slug', 'image', 'content', 'publish_date']
    def __init__(self, *args, **kwargs):
        super(PostModelForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget.attrs.update({'class' : 'form-control form-control-lg', 'placeholder': 'Write my own confession post!', 'id': 'exampleFormControlTextarea1', 'rows': '4'})

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

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)

