from django.core.management.base import BaseCommand
from faker import Faker
from accounts.models import CustomUser, Profile
from blog.models import Post, Category 
import random

list_category= ["cultural", "political", "scientific" , "fictional", "Fun"]
class Command(BaseCommand):
    
    
    help = "Closes the specified poll for voting"
    
    fake = Faker()

    def handle(self, *args, **options):
       user = CustomUser.objects.create_user(email= self.fake.email(), password = "as@123456")
       # profile data
       profile = Profile.objects.get(user = user)
       profile.first_name=self.fake.first_name() 
       profile.last_name = self.fake.last_name()
       profile.description = self.fake.text()
       profile.updated_on = self.fake.date_object()
       profile.save()
       
       # category data
       for name in list_category:
            Category.objects.get_or_create(name = name)
        
        # post data
       for _ in range(10):
           Post.objects.create(
               author = profile,
               title = self.fake.text(),
               body = self.fake.paragraph(nb_sentences = 10),
               status = random.choice([True, False]),
               updated_date = self.fake.date_object() ,
               category = Category.objects.get(name= random.choice(list_category)),
           )
        
           