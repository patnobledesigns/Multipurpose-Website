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
        page = requests.get("https://www.naijanews.com/entertainment/")

        soup =  BeautifulSoup(page.content,'html.parser')
        a = soup.select('ul.mvp-blog-story-list.left.relative.infinite-content li a')
        d = [x['href'] for x in a]
        
        count = 0
        for links in d:
            res = requests.get(links)
            soupy = BeautifulSoup(res.content, 'html.parser')
            info = soupy.find(id='mvp-post-content')
            head = info.select('h1.mvp-post-title, #mvp-post-content h1.mvp-post-title')
            para1 = info.select('span.mvp-post-excerpt.left p')
            img = info.select('#mvp-post-feat-img img')
            i = [x['src'] for x in img]
            main = info.select('#mvp-content-main p')
            
            for f,g,h,i in zip(head, para1, i, main):
                title = f.text
                firstp = g.text
                image = h
                mainp = i.text
                paragraph = firstp + mainp

                try:
                    Post.objects.create(
                        title=title,
                        content=paragraph,
                        category = Category.objects.get(name="Entertainment"),
                        thumbnail = image,
                        author = Author.objects.get(user=1),
                    )
                    count = count + 1
                    self.stdout.write(self.style.SUCCESS("{} ------- successful uploaded" .format(title)))
                except:
                    self.stdout.write(self.style.NOTICE("{} ------- Already Exists" .format(title)))
                        
                        
        print("{} Sports News successful uploaded".format(count))
            
            
        
        
        
        
        
        
        
       