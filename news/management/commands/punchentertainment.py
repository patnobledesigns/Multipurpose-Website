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
        url = "https://punchng.com/topics/metro-plus/"
        page = requests.get(url)

        soup =  BeautifulSoup(page.content,'html.parser')
        a = soup.select('main.sub-section-wrapper .cards.no-gutter .items a')
        d = [x['href'] for x in a]
       
        
        count = 0
        for links in d:
            res = requests.get(links)
            soupy = BeautifulSoup(res.content, 'html.parser')
            info = soupy.find(class_='entry-header')
            head = info.select('h1.post_title')
            img = soupy.find(class_='post_featured_image')
            sour = img.select('div.b-lazy[data-src]')
            data = [x['data-src'] for x in sour]
            para = soupy.select('div.entry-content p')[:10]
            i = ' '.join(map(str, para))
            content = str(i)

            for f,g in zip(head, data):
                title = f.text
                image = g


                try:
                    Post.objects.create(
                        title=title,
                        content=content,
                        category = Category.objects.get(name="National News"),
                        thumbnail = image,
                        author = Author.objects.get(user=1) ,
                        tags = Tag.objects.get(id=15), 
                    )
                    count = count + 1
                    self.stdout.write(self.style.SUCCESS("{} ------- successful uploaded" .format(title)))
                except:
                    self.stdout.write(self.style.NOTICE("{} ------- Already Exists" .format(title)))
                        
                        
        print("{} Punch Entertainment News successful uploaded".format(count))
            
            
        
        
        
        
        
        
