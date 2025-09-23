from celery import shared_task
from . models import Posts,SubText
from bs4 import BeautifulSoup
import aiohttp
import asyncio
from datetime import datetime
from pprint import pprint
from asgiref.sync import sync_to_async
from pprint import pprint

@sync_to_async
def save_post(all_data):
    print('save post called')
    for data in all_data:
        sub=data['subtext']
        post,post_create=Posts.objects.get_or_create(post_id=data['post_id'],defaults={
            "ranking":data['ranking'],
            "source":data['source'],
            "title":data['title'],
            "title_url":data['title_url']
            })
        if not post_create:
            post.ranking=data['ranking']
            post.source=data['source']
            post.title=data['title']
            post.title_url=data['title_url']
            post.save()
        subtext,sub_create=SubText.objects.get_or_create(author=post,defaults=sub)
        if not sub_create:
            for key,value in sub.items():
                setattr(subtext,key,value)
                subtext.save()
async def scrapp():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://news.ycombinator.com") as resp:
            data=await resp.text()
            soup=BeautifulSoup(data,'html.parser')
    main_part=soup.find_all('tr',class_='athing')
    subtext=soup.find_all(class_='subtext')
    all_data=[]
    for turns,part in enumerate(main_part):
        a_tag=subtext[turns].find_all('a')
        comment=a_tag[-1].text.split()[0] if a_tag[-1] else None
        sitebite=part.find(class_='sitebit')
        source=sitebite.a.text if sitebite and sitebite.a else 'No Source'
        score=subtext[turns].find(class_='score')
        writer=subtext[turns].find(class_='hnuser')
        data={
            'post_id':int(part['id']),
            'ranking':int(part.span.text.split('.')[0]),
            'title':" ".join(line.strip() for line in part.find(class_='titleline').a.text.split('\n')),
            'title_url':part.find(class_='titleline').a['href'],
            'source':source,
            'subtext':{
            'points':int(score.text.split()[0] if score else 0),
            'writer':writer.text if writer else '',
            'time':datetime.fromisoformat(subtext[turns].find(class_='age')['title'].split()[0]),
            'comments':int(comment if comment not in ('discuss','hide') else 0)
            }
        }
        all_data.append(data)
    # for x in all_data:
    #     pprint(x['ranking'])
    await save_post(all_data)
@shared_task
def fetch_news():
    asyncio.run(scrapp())
    return 'Success News Fetch Successfully'

# asyncio.run(scrapp())

