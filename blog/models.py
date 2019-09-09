from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import RegexValidator

spotify_regex = RegexValidator(regex=r'(https://open.spotify.com/){1}(track|album|artist){1}/.*',
    message="Please enter a valid link.")

int_choices = [(i,i) for i in range(1,11)]

cat_choices = [
    ("Song", "Song"),
    ("Album", "Album"),
    ("Artist", "Artist"),
]

# Create your models here.
class Post(models.Model):
    category = models.CharField(choices=cat_choices, max_length=50)
    title = models.CharField("Name",max_length=50)
    
    rating = models.IntegerField(choices=int_choices)
    
    content = models.TextField("Tell us about it!")
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    link = models.CharField("Spotify Link", validators=[spotify_regex], 
            max_length=100, 
            help_text="URL format: 'https://open.spotify.com/(track|album|artist)/.*'")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
