# from blog.models import Music, Category
import requests
from django.core.management.base import BaseCommand
from news.models import *
from bs4 import BeautifulSoup
from taggit.models import Tag
from account.models import *  

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'


    def handle(self, *args, **options):
        page = requests.get("https://www.xtremeloaded.com/fb-tricks/")

        soup =  BeautifulSoup(page.content,'html.parser')
        a = soup.select('#messageindex #topic_container .sepbg .info div span a')
        d = [x['href'] for x in a]
        
        count = 0
        for links in d:
            res = requests.get(links)
            soupy = BeautifulSoup(res.content, 'html.parser')
            


        #         try:
        #             Post.objects.create(
        #                 title=title,
        #                 content=paragraph,
        #                 category = Category.objects.get(name="Gist"),
        #                 thumbnail = image,
        #                 author = Author.objects.get(user=1),
        #             )
        #             count = count + 1
        #             self.stdout.write(self.style.SUCCESS("{} ------- successful uploaded" .format(title)))
        #         except:
        #             self.stdout.write(self.style.NOTICE("{} ------- Already Exists" .format(title)))
                        
                        
        # print("{} Gist News successful uploaded".format(count))
            
            
        
        
        
        
        
  