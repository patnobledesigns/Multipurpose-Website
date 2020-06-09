import requests
from django.core.management.base import BaseCommand
from movies.models import *
from bs4 import BeautifulSoup


class Command(BaseCommand):
    help = 'Upload Latest Movies'


    def handle(self, *args, **options):
        page = requests.get("https://fzmovies.net/movieslist.php?catID=2&by=date")

        soup =  BeautifulSoup(page.content,'lxml')
        a = soup.select('.mainbox a')
        d = [x['href'] for x in a]
        print(d)
        # count = 0
        # for link in d:
        #     page = requests.get(link)
        #     soup =  BeautifulSoup(page.content,'lxml')
        #     print(soup)