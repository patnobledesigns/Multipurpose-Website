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
        page = requests.get("https://www.naijanews.com/sports/")

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
            q = [x['src'] for x in img]
            main = info.select('#mvp-content-main')
            
            for f,g,h,i in zip(head, para1, q, main):
                title = f.text
                image = h
                paragraph = i.get_text() + g.get_text()

                try:
                    Post.objects.create(
                        title=title,
                        content=paragraph,
                        category = Category.objects.get(name="Sport"),
                        thumbnail = image,
                        author = Author.objects.get(user=1) ,
                        tags = Tag.objects.get(id=15), 
                    )
                    count = count + 1
                    self.stdout.write(self.style.SUCCESS("{} ------- successful uploaded" .format(title)))
                except:
                    self.stdout.write(self.style.NOTICE("{} ------- Already Exists" .format(title)))
                        
                        
        print("{} Sports News successful uploaded".format(count))
            
            
        
        
        
        
        
        
