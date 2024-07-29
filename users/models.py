from django.db import models
from django.contrib.auth.models import User
from PIL import Image


# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()
    pdf_file = models.FileField(upload_to='pdf_files', blank=True, null=True)


    def __str__(self):
        return self.user.username

    # resizing images
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)
class NGO(models.Model):
    name=models.CharField('Ngo Name', max_length=50)
    location=models.CharField('Ngo location',max_length=100)
    email=models.CharField(max_length=50)
    contactno=models.CharField(max_length=10)
    description=models.TextField(blank=True,max_length=500)
    website=models.CharField(max_length=500)
    logo = models.ImageField(upload_to='images/',default='default_logo.png')
    def __str__(self):
        return self.name
