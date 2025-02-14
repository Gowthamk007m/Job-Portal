from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
import os

# Create your models here.
COUNTRY_CHOICES = (
    ('India', 'India'),
    ('United States', 'United States'),
    ('United Kingdom', 'United Kingdom'),
    ('Australia', 'Australia'),
    ('Canada', 'Canada'),
    ('New Zealand', 'New Zealand'),
    ('Afghanistan', 'Afghanistan')
)

QUALIFICATION_CHOICES = (
    ("High School", "High School"),
    ("Associate's Degree", "Associate's Degree"),
    ("Bachelor's Degree", "Bachelor's Degree"),
    ("Master's Degree", "Master's Degree"),
    ("Doctorate", "Doctorate"),
    ("Professional Degree", "Professional Degree"),
    ("Certificate", "Certificate"),
    ("Diploma", "Diploma"),
    ("Postdoctoral", "Postdoctoral"),
    ("Vocational", "Vocational"),
)

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other')
)

SMOKING_CHOICES = (
    ('Non-smoker', 'Non-smoker'),
    ('Occasional smoker', 'Occasional smoker'),
    ('Regular smoker', 'Regular smoker'),
    ('Heavy smoker', 'Heavy smoker'),
    ('Trying to quit', 'Trying to quit'),
)

DRINKING_CHOICES = (
    ('Non-drinker', 'Non-drinker'),
    ('Occasional drinker', 'Occasional drinker'),
    ('Social drinker', 'Social drinker'),
    ('Regular drinker', 'Regular drinker'),
    ('Heavy drinker', 'Heavy drinker'),
    ('Trying to quit', 'Trying to quit'),
)



LEVEL_CHOICES = (
    ('beginner', 'Beginner'),
    ('intermediate', 'Intermediate'),
    ('advanced', 'Advanced'),
    ('expert', 'Expert'),
)


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
        

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    profile_photo = models.ImageField(upload_to='user_photos/', blank=True, null=True)
    dob = models.DateField(null=True, blank=True)
    qualification = models.CharField(max_length=255, blank=True, null=True, choices=QUALIFICATION_CHOICES)
    smoking_habit = models.CharField(max_length=20, choices=SMOKING_CHOICES, default='Non-smoker')
    drinking_habit = models.CharField(max_length=20, choices=DRINKING_CHOICES, default='Non-drinker')
    short_reel = models.FileField(upload_to='short_reel/', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    def __str__(self):
        return self.email
    
    def age(self):
        if self.dob:
            today = date.today()
            age = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
            return age
        return None
    
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def save(self, *args, **kwargs):
        if self.id:
            orig = CustomUser.objects.get(pk=self.id)
            
            if self.profile_photo and orig.profile_photo != self.profile_photo:
                if orig.profile_photo:
                    if os.path.isfile(orig.profile_photo.path):
                        os.remove(orig.profile_photo.path)
            
            if self.short_reel and orig.short_reel != self.short_reel:
                if orig.short_reel:
                    if os.path.isfile(orig.short_reel.path):
                        os.remove(orig.short_reel.path)
        
        super().save(*args, **kwargs)
        
    def delete(self, *args, **kwargs):
        if self.profile_photo:
            if os.path.isfile(self.profile_photo.path):
                os.remove(self.profile_photo.path)
            self.profile_photo.delete()
        
        if self.short_reel:
            if os.path.isfile(self.short_reel.path):
                os.remove(self.short_reel.path)
            self.short_reel.delete()
        

        super().delete(*args, **kwargs)


class Hobby(models.Model):
    hobby = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.hobby


class Interest(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
        

class UserHobby(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    hobby = models.ForeignKey(Hobby, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'hobby')
        
    def __str__(self):
        return f"{self.user.username} - {self.hobby.hobby}"
    
    
class UserInterest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'interest')
        
    def __str__(self):
        return f"{self.user.username} - {self.interest.name}"
    
        

class UserImages(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='user_images/', blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.email
    
@receiver(pre_delete, sender=UserImages)
def user_images_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

@receiver(pre_save, sender=UserImages)
def user_images_update(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = UserImages.objects.get(pk=instance.pk)
            if old_instance.image:
                if old_instance.image != instance.image:
                    if os.path.isfile(old_instance.image.path):
                        os.remove(old_instance.image.path)
        except UserImages.DoesNotExist:
            pass



class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=15)
    address_line_1 = models.TextField(max_length=250)
    address_line_2 = models.TextField(max_length=250)
    address_line_3 = models.TextField(max_length=250)
    country = models.CharField(max_length=50, default='India', choices=COUNTRY_CHOICES)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    pincode = models.CharField(max_length=25)
    phone = models.CharField(max_length=15, blank=True, null=True)
    is_default = models.BooleanField(default=True)

    class Meta:
        unique_together = ['user', 'name']
        
    def save(self, *args, **kwargs):
        if self.is_default:
            Address.objects.filter(user=self.user, is_default=True).update(is_default=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'''{self.address_line_1}
        {self.address_line_2}
        {self.address_line_3}'''
        

class Experience(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} at {self.company}"


class Education(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    institution = models.CharField(max_length=100)
    degree = models.CharField(max_length=25, choices=QUALIFICATION_CHOICES)
    field_of_study = models.CharField(max_length=100, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.degree} from {self.institution}"
    

class UserSkill(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ['user', 'skill']
    
    def __str__(self):
        return f"{self.skill}"