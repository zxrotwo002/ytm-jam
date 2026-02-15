from flask import *
from markupsafe import escape
from ytmusicapi import YTMusic,OAuthCredentials
from dotenv import load_dotenv,dotenv_values
import dominate
from dominate.tags import *
import os
import json
import requests

app = Flask(__name__)
load_dotenv()



ytmusic = YTMusic("browser.json")

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/search/')
@app.route('/search/<query>')
def search(query=" "):
    results = (ytmusic.search(query=query))
    doc = dominate.document(title=query)

    with doc.head:
        link(rel='stylesheet', href=url_for('static', filename='style.css'))
        script(type='text/javascript', src=url_for('static', filename='script.js'))

    with doc:
        with div(id='header').add(ol()):
            for i in ['home']:
                li(a(i.title(), href='/'))
        
        artists = []
        songs = []
        playlists = []
        videos = []

        div(input_(type="text",cls="form-control",id="searchYTM",oninput="apiCall()") ,id='container')

        for result in results:
            type = result['resultType']
            match type:
                case 'artist':
                    artists.append(result)
                case 'song':
                    songs.append(result)
                case 'video':
                    videos.append(result)
                case 'playlist':
                    playlists.append(result)
        p('Songs')
        for result in songs:
            with div():
                thumbnails = result['thumbnails']
                url = thumbnails[len(thumbnails)-1]['url']
                img(src=url, width=100)
                title = result['title']
                video_id = result['videoId']
                a(title,href=f'https://music.youtube.com/watch?v={video_id}',cls="video")
                artist_name = ""
                if 'artist' in result:
                    name = result['artist']
                    if 'browseId' in result:
                        id = result['browseId']
                        a(name,href=f'/artist/{id}',cls="artist")
                    else:
                        span(result)
                    if artist_name == "":
                        artist_name = name
                if 'artists' in result:
                    for artist in result['artists']:
                        name = artist['name']
                        if artist_name == "":
                            artist_name = name
                        id = artist['id']
                        a(name,href=f'/artist/{id}',cls="artist")
                button("Add to Queue",type="button",cls="button queue",onclick=f'add(event,"{title}","{artist_name}","{video_id}","queue")')
                button("Play Next",type="button",cls="button next",onclick=f'add(event,"{title}","{artist_name}","{video_id}","next")')
        p('Artists')
        for result in artists:
            with div():
                thumbnails = result['thumbnails']
                url = thumbnails[len(thumbnails)-1]['url']
                img(src=url, width=100)
                if 'artist' in result:
                    name = result['artist']
                    if 'browseId' in result:
                        id = result['browseId']
                        a(name,href=f'/artist/{id}',cls="artist")
                    else:
                        span(result)
                if 'artists' in result:
                    for artist in result['artists']:
                        name = artist['name']
                        id = artist['id']
                        a(name,href=f'/artist/{id}',cls="artist")
        p('Videos')
        for result in videos:
            with div():
                thumbnails = result['thumbnails']
                url = thumbnails[len(thumbnails)-1]['url']
                img(src=url, width=100)
                title = result['title']
                video_id = result['videoId']
                a(title,href=f'https://music.youtube.com/watch?v={video_id}',cls="video")
                artist_name = ""
                if 'artist' in result:
                    name = result['artist']
                    id = result['browseId']
                    a(name,href=f'/artist/{id}',cls="artist")
                    if artist_name == "":
                        artist_name = name
                if 'artists' in result:
                    for artist in result['artists']:
                        name = artist['name']
                        if artist_name == "":
                            artist_name = name
                        id = artist['id']
                        a(name,href=f'/artist/{id}',cls="artist")
                button("Add to Queue",type="button",cls="button queue",onclick=f'add(event,"{title}","{artist_name}","{video_id}","queue")')
                button("Play Next",type="button",cls="button next",onclick=f'add("event,{title}","{artist_name}","{video_id}","next")')
        p('Playlists')
        for result in playlists:
            with div():
                thumbnails = result['thumbnails']
                url = thumbnails[len(thumbnails)-1]['url']
                img(src=url, width=100)
                title = result['title']
                author = result['author']
                if 'browseId' in result:
                    id = result['browseId'][2:]
                    a(title,href=f'https://music.youtube.com/playlist?list={id}',cls="playlist")
                elif 'playlistId' in result:
                    id = result['playlistId'][2:]
                    a(title,href=f'https://music.youtube.com/playlist?list={id}',cls="playlist")
                else:
                    span(result)
                span(author)
    return doc.render()

@app.route('/suggestion/')
@app.route('/suggestion/<query>')
def suggestion(query=""):
    results = ytmusic.get_search_suggestions(query)
    return results

@app.route('/artist/<artist_id>')
def artist(artist_id):
    doc = dominate.document(title=artist_id)




    with doc.head:
        link(rel='stylesheet', href=url_for('static', filename='style.css'))
        script(type='text/javascript', src=url_for('static', filename='script.js'))

    with doc:
        with div(id='header').add(ol()):
            for i in ['home']:
                li(a(i.title(), href='/'))
        div(input_(type="text",cls="form-control",id="searchYTM",oninput="apiCall()") ,id='container')
        try:
            results = ytmusic.get_artist(artist_id)
            name = results['name']
            subscribers = results['subscribers']
            songs = results['songs']['results']
            videos = results['videos']['results']
            thumbnails = results['thumbnails']
            url = thumbnails[len(thumbnails)-1]['url']
            img(src=url, width=200)
            a(name,href=f'https://music.youtube.com/channel/{artist_id}',cls="artist external")
            span(f'{subscribers} subscribers',cls = "subscribers")
            p('Songs')
            for result in songs:
                with div():
                    thumbnails = result['thumbnails']
                    url = thumbnails[len(thumbnails)-1]['url']
                    img(src=url, width=100)
                    title = result['title']
                    video_id = result['videoId']
                    a(title,href=f'https://music.youtube.com/watch?v={video_id}',cls="video")
                    artist_name = ""
                    if 'artist' in result:
                        name = result['artist']
                        if 'browseId' in result:
                            id = result['browseId']
                            a(name,href=f'/artist/{id}',cls="artist")
                        else:
                            span(result)
                        if artist_name == "":
                            artist_name = name
                    if 'artists' in result:
                        for artist in result['artists']:
                            name = artist['name']
                            if artist_name == "":
                                artist_name = name
                            id = artist['id']
                            a(name,href=f'/artist/{id}',cls="artist")
                    button("Add to Queue",type="button",cls="button queue",onclick=f'add(event,"{title}","{artist_name}","{video_id}","queue")')
                    button("Play Next",type="button",cls="button next",onclick=f'add(event,"{title}","{artist_name}","{video_id}","next")')
            p('Videos')
            for result in videos:
                with div():
                    thumbnails = result['thumbnails']
                    url = thumbnails[len(thumbnails)-1]['url']
                    img(src=url, width=100)
                    title = result['title']
                    video_id = result['videoId']
                    a(title,href=f'https://music.youtube.com/watch?v={video_id}',cls="video")
                    artist_name = ""
                    if 'artist' in result:
                        name = result['artist']
                        if 'browseId' in result:
                            id = result['browseId']
                            a(name,href=f'/artist/{id}',cls="artist")
                        else:
                            span(result)
                        if artist_name == "":
                            artist_name = name
                    if 'artists' in result:
                        for artist in result['artists']:
                            name = artist['name']
                            if artist_name == "":
                                artist_name = name
                            id = artist['id']
                            a(name,href=f'/artist/{id}',cls="artist")
                    button("Add to Queue",type="button",cls="button queue",onclick=f'add(event,"{video_id}","{artist_name}","{video_id}","queue")')
                    button("Play Next",type="button",cls="button next",onclick=f'add(event,"{video_id}","{artist_name}","{video_id}","next")')
            #span(results)
        except:
            span(f"Couldn't find artist with id: {artist_id}")
            p()
            span(span("You can try to find that artist on "),a("Youtube",href=f'https://music.youtube.com/channel/{artist_id}',cls="artist external"))

    return doc.render()
