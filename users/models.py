from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# set the way to save user data file
def user_directory_save_file(instance, file):
    return 'user_{0}/{1}'.format(instance.user.id, file)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to=user_directory_save_file)
    file = models.FileField(upload_to=user_directory_save_file, default='default.csv')

    def __str__(self):
        return f'{self.user.username} Profile'

#@ for AWS lanbda functions !

    def save(self, *args, **kwargs): # change the save method
        super().save(*args, **kwargs)
        # image
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)




