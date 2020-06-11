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
        page = requests.get("https://www.naijanews.com/politics/")

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
                        category = Category.objects.get(name="Politics"),
                        thumbnail = image,
                        author = Author.objects.get(user=1),
                    )
                    count = count + 1
                    self.stdout.write(self.style.SUCCESS("{} ------- successful uploaded" .format(title)))
                except:
                    self.stdout.write(self.style.NOTICE("{} ------- Already Exists" .format(title)))
                        
                        
        print("{} Politics News successful uploaded".format(count))
            
            
        
        
        
        
        
        
        
        # print(d)
        # count = 0
        # for link in d:
        #     page = requests.get(link)
        #     soup =  BeautifulSoup(page.content,'html.parser')
        #     a = soup.find(class_='dt_post_content')
        #     b = a.select('.post-header .post-title')
        #     post = soup.select('.post-content  p .size-medium ')
        #     post2 = soup.select('.post-content  p .btn-ghost')
            
        #     post3 = soup.select('.post-content  p')[1:4]
        #     post4 = soup.select('.post-content  p')[2:4]

        #     for x,c,y,z,w in zip(post, b, post2,post3,post4):
        #         s = c.get_text().replace('[Music]', '')
        #         print(s)
        # #         abc = s.replace('[Music + Video]', '')
        # #         daaab = abc.replace('[Video]', '')
        # #         rest = daaab.split(" – ", 1)[0] # string.split(separator, maxsplit)
        # #         abababa = z.get_text() + w.get_text()
        # #         try:
        # #             Post.objects.create(title=daaab ,category= Category.objects.get(name="Education") , slug=rest,thumbnail=x['src'],content=abababa ,tags = rest)
        # #             count = count + 1
        # #             self.stdout.write(self.style.SUCCESS("{} ------- successful uploaded" .format(daaab)))

        # #         except Exception:
        # #             pass


        #     print("{} music successful uploaded".format(count))