from django.conf import settings
from django.db import models
from django.db.models import Q
from django.template.defaultfilters import slugify

from django.utils import timezone

User = settings.AUTH_USER_MODEL

class PostQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(publish_date__lte=now)

    def search(self, query):
        lookup = (Q(content__icontains=query) | 
                  Q(slug__icontains=query) |
                  Q(user__username__icontains=query) |
                  Q(user__email__iexact=query)
                )
        return self.filter(lookup)

class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()

    def search(self, query=None):
        if not query:
            return self.get_queryset().none()
        return self.get_queryset().published().search(query)


class Post(models.Model):
    user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)
    # image = models.ImageField(upload_to='image/', blank=True, null=True)
    slug = models.SlugField(unique=True)
    content = models.TextField(max_length=1000)
    publish_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    time_stamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    likes= models.IntegerField(default=0)
    dislikes= models.IntegerField(default=0)
    # comments = models.TextField(max_length=500)

    objects = PostManager()

    class Meta:
        ordering = ['-publish_date', '-updated', '-time_stamp']

    def get_absolute_url(self):
        return f'/post/{self.slug}'

    def get_edit_url(self):
        return f'{self.get_absolute_url()}/edit'

    def get_delete_url(self):
        return f'{self.get_absolute_url()}/delete'

    def get_comment_url(self):
        return f'{self.get_absolute_url()}/comment'

    def approved_comments(self):
        return self.comments.filter(approved=True)

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.content)

        super(Post, self).save(*args, **kwargs)

class Preference(models.Model):
    user= models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    post= models.ForeignKey(Post, null=True, on_delete=models.SET_NULL)
    value= models.IntegerField()
    date= models.DateTimeField(auto_now= True)

    def __str__(self):
        return str(self.user) + ':' + str(self.post) +':' + str(self.value)

    class Meta:
       unique_together = ("user", "post", "value")

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user= models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    approved= models.BooleanField(default=False)

    def approve(self):
        self.approved= True
        self.save()

    def __str__(self):
        return self.text
