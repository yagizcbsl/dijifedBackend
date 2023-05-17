from django.db import models
import string
import random
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from django.conf import settings

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "Token for password reset={}".format(reset_password_token.key)
    send_mail(
        # title:
        "Password Reset for {title}".format(title="DIJIFED"),
        # message:
        email_plaintext_message,
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [reset_password_token.user.email]
    )


# Create your models here.
def generate_unique_id():
    length = 6
    
    while True:
        code = "".join(random.choices(string.ascii_uppercase,k=length))
        if ProfileTable.objects.filter(userID=code).count() == 0:
            break
    return code

def generate_random_code():
    length = 6
    return "".join(random.choices(string.ascii_uppercase,k=length))
        

def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)

defaultSocailMedia = {
    "instagram" : {"link":"","activated":0},
    "discord" : {"link":"","activated":0},
    "facebook" : {"link":"","activated":0},
    "instagram" : {"link":"","activated":0},
    "linkedin" : {"link":"","activated":0},
    "messenger" : {"link":"","activated":0},
    "pinterest": {"link":"","activated":0},
    "reddit" : {"link":"","activated":0},
    "snapchat" : {"link":"","activated":0},
    "spotify" : {"link":"","activated":0},
    "telegram" : {"link":"","activated":0},
    "tiktok" : {"link":"","activated":0},
    "twitter" : {"link":"","activated":0},
    "vsco" : {"link":"","activated":0}
}

class ProfileTable(models.Model):
    user = models.OneToOneField(User, null=True,blank=True, on_delete=models.CASCADE)
    userID = models.CharField(max_length=15,primary_key=True,unique=True,null=False,blank=False,default=generate_unique_id)
    name = models.CharField(max_length=128, null= True,blank=True)
    surname = models.CharField(max_length=128,null=True,blank=True)
    title = models.CharField(max_length=128 , null=True,blank = True)
    company = models.CharField(max_length=128,null=True,blank=True)
    description = models.CharField(max_length=256,null=True,blank=True)
    profilePicture = models.ImageField(upload_to=upload_to, blank=True, null=True)
    coverPage = models.ImageField(upload_to=upload_to, blank=True, null=True)
    website = models.CharField(max_length=256,null = True,blank = True)
    phone =  models.CharField(null = True, blank = True, max_length=64)
    companyPhone = models.CharField(null = True, blank = True, max_length=64)
    mail = models.CharField(null = True, blank = True, max_length=64)
    address = models.CharField(null=True,blank=True,max_length=512)
    addressCompany = models.CharField(null=True,blank=True,max_length=128)
    location = models.JSONField(default=dict ,blank=True, null=True)
    vergiNo = models.CharField(null=True,blank=True,max_length=512)
    iban = models.CharField(null=True,blank=True,max_length=512)
    socialLinks = models.JSONField(default=defaultSocailMedia ,blank=True, null=True)
    externalLinks = models.JSONField(default=[] ,blank=True, null=True)
    
class extraUserFields(models.Model):
    user = models.OneToOneField(User, null=True,blank=True, on_delete=models.CASCADE)
    verificationCode = models.CharField(max_length=64,null=False, blank=False, default=generate_random_code)
    isVerified = models.BooleanField(default= False, blank=True, null=True)
    resetCode = models.CharField(max_length=64,null=False, blank=False, default=generate_random_code)