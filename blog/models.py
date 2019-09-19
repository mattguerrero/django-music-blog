from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

from django.core.validators import RegexValidator
from taggit.managers import TaggableManager


spotify_regex = RegexValidator(regex=r'(https://open.spotify.com/){1}(track|album|artist|embed/track|embed/album|embed/artist){1}/.*',
    message="Please enter a valid link.")

int_choices = [(i,i) for i in range(1,11)]

cat_choices = [
    ("Song", "Song"),
    ("Album", "Album"),
    ("Artist", "Artist"),
]

# Create your models here.
class Post(models.Model):
    link = models.CharField("Spotify Link", validators=[spotify_regex], 
            max_length=100, 
            help_text="Format: 'https://open.spotify.com/(track|album|artist)/.*'")

    category = models.CharField(max_length=50, blank=True)
    title = models.CharField(max_length=50, blank=True)
    artist = models.CharField(max_length=50, blank=True)
    
    rating = models.IntegerField(choices=int_choices, blank=False)
    content = models.TextField("Your thoughts")

    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    tags = TaggableManager(blank=True)

    def __str__(self):
        return "'{}' by {}".format(self.title, self.author)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
        