import requests
from django.core.management.base import BaseCommand
from movies.models import *
from bs4 import BeautifulSoup


class Command(BaseCommand):
    help = 'Upload Latest Movies'


    def handle(self, *args, **options):
        page = requests.get("https://www.thenetnaija.com/videos/movies")

        soup =  BeautifulSoup(page.content,'html.parser')
        a = soup.select('main.file-list a')
        d = [x['href'] for x in a]

        
        count = 0
        for link in d:
            page = requests.get(link)
            soup =  BeautifulSoup(page.content,'html.parser')
            page = soup.find('article', class_='video-file')
            run = page.select('.video-stats')
            for x in run:
                runt = x.text.split('|')[-1] 
                runtime = runt.replace(' Runtime:', '')
            imgsrc = page.select('.video-plain .video-image img')
            img = [x['src'] for x in imgsrc]
            content = page.select('.video-details .video-about > p')
            titlep = page.select('.quote-content p')
            titl = soup.select('h1#page-title')
            for x in titl:
                tit = x.text.replace('[DVDRip]', '')
                t = tit.replace('Movie:', '')
                u = t.replace('[Korean]', '')
                title = u.replace('[Thai]', '')
            gen = [x for x in titlep][1].get_text()
            genre = gen.replace('Genre:', '')
            release = [x for x in titlep][2].get_text()
            releasedate = release.replace('Release Date:', '')
            star = [x for x in titlep][3].get_text()
            stars = star.replace('Stars:', '')
            sour = [x for x in titlep][4].get_text()
            source = sour.replace('Source:', '')
            lang = [x for x in titlep][5].get_text()
            language = lang.replace('Language:', '')
            try:        
                imd = [x for x in titlep][7].get_text()
                imdb = imd.replace('IMDB:', '')
            except:
                pass
            emb = page.select('.embed-video iframe')
            downlinks = page.select('.video-download p a[href*="/download"]')
            download = [x['href'] for x in downlinks]
            
            for links in download:
                res = requests.get(links)
                search = BeautifulSoup(res.content, 'html.parser')
                file = search.select('.file-share .form .row > input') 
                loop = [x for x in file][3].get('value')
                for d,e,f,g in zip(img,content,emb,runt):
                    image = d
                    cont = e.text
                    embed = str(f)                
                    try:
                        Movie.objects.create(
                            name=title,
                            star=stars,
                            genre=genre,
                            overview=cont,
                            release_date=releasedate,
                            language=language,
                            runtime=runtime,
                            thumbnail=image,
                            imdb=imdb,
                            iframe=embed,
                            source=source,
                            download_link=loop,
                        )
                        count = count + 1
                        self.stdout.write(self.style.SUCCESS("{} ------- successful uploaded" .format(title)))
                    except:
                        self.stdout.write(self.style.NOTICE("{} ------- Already Exists" .format(title)))
                    
                    
        print("{} Movies successful uploaded".format(count))
            