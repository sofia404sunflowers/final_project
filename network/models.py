from django.contrib.auth.models import AbstractUser
from django.db import models
from urllib.parse import urlparse, parse_qs



class User(AbstractUser):
    pass

class Recording(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField()
    link = models.URLField(max_length=200)

    @property
    def youtube_id(self):
        try:
            parsed = urlparse(self.link)
            if parsed.netloc == 'youtu.be':
                youtube_id = parsed.path[1:]
                return youtube_id
            youtube_id = parse_qs(parsed.query)['v'][0]
            return youtube_id
        except:
            raise ValueError('Can not parse youtube id from link')

    def __str__(self):
        return f"{self.title}"



class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    text = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField("User", related_name="likes")

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.id,  # "temp user", #self.user.serialize(),
            "user_name": self.user.username,
            "text": self.text,
            "timestamp": self.timestamp.strftime("%b %-d %Y, %-I:%M %p"),
            "likes": self.likes.count(),
        }

    def __str__(self): return f"{self.user} posted: {self.text}"

