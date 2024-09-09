from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from .models import Link

def scrape(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        if url:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Clear existing links before saving new ones
            Link.objects.all().delete()

            for link in soup.find_all('a'):
                link_address = link.get('href')
                link_text = link.string
                if link_address:
                    Link.objects.create(address=link_address, name=link_text)

            data = Link.objects.all()
            return render(request, 'scraper/result.html', {'data': data})

    # If GET request or invalid URL
    return render(request, 'scraper/index.html')
