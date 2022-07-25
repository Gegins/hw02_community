from django.db import models
from django.contrib.auth import get_user_model

class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=20, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title

User = get_user_model()





class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    group = models.ForeignKey(
        Group, on_delete=models.SET_NULL,
        # так добавлено же "с завода" related_names!!!
        related_name='posts', blank=True, null=True)

    class Meta:
        ordering = ("-pub_date",)

    def __str__(self) -> str:
        return self.text




