from django.core.management.base import BaseCommand
from django.utils import timezone
from news.models import Post
import requests
from bs4 import BeautifulSoup


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'


 
def handle(self, *args, **options):
    page = requests.get("https://www.naijaloaded.com.ng/download-mp3")

    soup =  BeautifulSoup(page.content,'html.parser')
    a = soup.select('.simple-post .simple-thumb a')
   

    print("music successful uploaded")
