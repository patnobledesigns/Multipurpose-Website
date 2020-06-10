# from blog.models import Music, Category
import requests
from django.core.management.base import BaseCommand
from news.models import Category, Post
from bs4 import BeautifulSoup

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'


    def handle(self, *args, **options):
        page = requests.get("https://www.naijaloaded.com.ng/download-mp3")

        soup =  BeautifulSoup(page.content,'html.parser')
        a = soup.select('.simple-post .simple-thumb a')
        d = [x['href'] for x in a]
        # print(d)
        count = 0
        for link in d:
            page = requests.get(link)
            soup =  BeautifulSoup(page.content,'html.parser')
            a = soup.find(class_='dt_post_content')
            b = a.select('.post-header .post-title')
            post = soup.select('.post-content  p .size-medium ')
            post2 = soup.select('.post-content  p .btn-ghost')
            
            post3 = soup.select('.post-content  p')[1:4]
            post4 = soup.select('.post-content  p')[2:4]

            for x,c,y,z,w in zip(post, b, post2,post3,post4):
                s = c.get_text().replace('[Music]', '')
                print(s)
        #         abc = s.replace('[Music + Video]', '')
        #         daaab = abc.replace('[Video]', '')
        #         rest = daaab.split(" – ", 1)[0] # string.split(separator, maxsplit)
        #         abababa = z.get_text() + w.get_text()
        #         try:
        #             Post.objects.create(title=daaab ,category= Category.objects.get(name="Education") , slug=rest,thumbnail=x['src'],content=abababa ,tags = rest)
        #             count = count + 1
        #             self.stdout.write(self.style.SUCCESS("{} ------- successful uploaded" .format(daaab)))

        #         except Exception:
        #             pass


            print("{} music successful uploaded".format(count))