import click
import urllib.request
from bs4 import BeautifulSoup
from setuptools import setup
def url_checker(url):
    try:
        url_d = urllib.request.urlopen(url)
        if url_d.getcode() == 200:
            return True
        else:
            click.echo("URL you enteres returned an error message")

    except:
        click.echo("URL you entered is invalid")
        exit(0)
        return False

@click.command()
@click.option('--user',help = "Specifies to only scrape posts from that user")
@click.option('--pages',default = 1,help = 'The number of pages to scrape')
@click.argument('url',type = str,)
def cli(user,pages,url):
    """ This script is designed to help scrape xeno-forum posts. Type the words
    Hello along with a url to scrape the page."""
    if url[-1] != '/': #Fixes the most common error
        url = url +'/'
    url_checker(url)
    for i in range(1,pages + 1): # decides how many pages of a thread to use
        thread = urllib.request.urlopen((url + 'page-{}').format(i)).read()
        page = BeautifulSoup(thread,"html.parser")
        posts = page.find_all('li',{"class" : "message"}) # extracts the post from the background of the website
        if user: # only has to be run if a specifed user is designates
            for post in posts :
                author = str(post["data-author"]) # Turns the author of the post into a comparable string
                post_text = post.find('div',{"class" : "messageContent"}) # get's the content of the text
                if (author == user):
                    click.echo(post_text.text)
                    click.echo("*" * 30) # Seperates Posts

        else:
            for post in posts:
                post_text = post.find('div',{"class" : "messageContent"})
                click.echo(post_text.text)
                click.echo("*" * 30) # Seperates Posts
