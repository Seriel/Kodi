# -*- coding: utf-8 -*-
# Module: default
# Author: Andrea Sant.
# Created on: 12.12.2023
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html
#from __future__ import unicode_literals
'''

        
'''
#import re
import  sys, os 
import xbmcgui, xbmc
import xbmcplugin
import xbmcaddon
import xbmcvfs

import urllib.request
from urllib.parse import parse_qsl
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

#import web_pdb # web_pdb.set_trace()   #togliere successivamente

def get_runtime_path():

    return xbmcvfs.translatePath( __settings__.getAddonInfo('Path') )


class MyPlayer(xbmc.Player):

    def __init__(self):
        xbmc.Player.__init__(self)

    def cat_link(self):
        
        link = get_link(ind)
        li = createListItem(_addonName,
                            thumbnailImage='{0}/icon.png'.format(os.path.dirname(os.path.abspath(__file__))),
                            streamtype='video', infolabels={'title': 'LIVE'})

        if link.find('www.youtube.com') > 0:
            codStart = link.find('embed/') + 6
            codStop = link.find('?')
            video_id = link[codStart:codStop]

            link = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % video_id
            # play_item = xbmcgui.ListItem(path=url)
            # xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)

        self.play(link, li)

    def onPlayBackEnded(self):
        # Will be called when xbmc stops playing a file
        #self.cat_link()
        return

    def onPlayBackStopped(self):
        global finito
        finito = True

def createListItem(label, label2 = '', iconImage = None, thumbnailImage = None, path = None, fanart = None, streamtype = None, infolabels = None, duration = '', isPlayable = False):
    li = xbmcgui.ListItem(label, label2)
    if iconImage:
      li.setIconImage(iconImage)
    if thumbnailImage:
      li.setThumbnailImage(thumbnailImage)
    if path:
      li.setPath(path)
    if fanart:
      li.setProperty('fanart_image', fanart)
    if streamtype:
      li.setInfo(streamtype, infolabels)
    if streamtype == 'video' and duration:
      li.addStreamInfo(streamtype, {'duration': duration})
    if isPlayable:
      li.setProperty('IsPlayable', 'true')
    return li

_id='plugin.video.visionetv'


__settings__ = xbmcaddon.Addon(id=_id)
_addonName = xbmcaddon.Addon().getAddonInfo('name')
path = get_runtime_path()
_resdir = path + "/resources"
#add our library to python search path
sys.path.append( _resdir + "/lib/")
sys.path.append( _resdir + "/media/")
mPath = path+"/resources/media/"
indirizzo = "https://visionetv.it/"




# Get the plugin url in plugin:// notation.
_url = sys.argv[0]
# Get the plugin handle as an integer number.
_handle = int(sys.argv[1])

# Free sample videos are provided by www.vidsplay.com
# Here we use a fixed set of properties simply for demonstrating purposes
# In a "real life" plugin you will need to get info and links to video files/streams
# from some web-site or online service.
VIDEOS = []

def ricerca(category):
    kb =xbmc.Keyboard ('', 'Ricerca', False)
    kb.doModal()
    
    if (kb.isConfirmed()):
        richiesta = kb.getText()
        richiesta = richiesta.strip()
        stringa = '?s='+ richiesta.replace(" ", "+")  
    return stringa
    
def get_link1(ind):
    req = Request(ind,headers={ 'User-Agent': 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16'})
    response = urllib2.urlopen(req)
    the_page = response.read()
    page = common.parseDOM(the_page, "div",attrs = {"class":"screen fluid-width-video-wrapper"})    
    link1 = common.parseDOM(page, "iframe", ret = "src")
    print(link1)
    start = link1[0].find("embed")+ 6
    stop = link1[0].find("?auto")
    cod = link1[0][start:stop]
    link = "http://video.mainstreaming.tv/sdk/13/jsRequest.js?contentId="+cod+"&method=getVideo&skinId=150575&referrer="
    print(link)
    
    return link
  
def get_link(ind):
    req = urllib2.Request(ind,headers={ 'User-Agent': 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16'})
    response = urllib2.urlopen(req)
    the_page = response.read()
    linkStart =the_page.find('attributesHtml5.href="')+22
    linkStop = the_page.find('m3u8')+4
    ind = the_page[linkStart:linkStop]
    return ind  
    
def get_menu(ind):

    global MENU
    MENU = []

    req = Request(ind,headers={ 'User-Agent': 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16'})
    response = urlopen(req)
    the_page = BeautifulSoup(response, 'html.parser')

    main_menu = the_page.find('li', id='menu-item-109224')

    for link in main_menu.find_all('a'):
        #xbmc.log('OGGETTO1------: ' + str(link), xbmc.LOGINFO)

        name = link.get_text()
        if name == "FORMAT":
            name = "Novità"

        indirizzo = (link.get('href'))
        #'thumb': mPath + 'icon.png'
        MENU.append({'name': name,
                     'indirizzo': indirizzo,
                     'thumb': mPath + 'fanart.jpg',
                     'fanart': mPath + 'fanart.jpg'
                     })
    return ind 



def get_videos(category, page, cerca):
    """
    Get the list of videofiles/streams.
    Here you can insert some parsing code that retrieves
    the list of videostreams in a given category from some site or server.
    :param category: str
    :return: list
    """
    global VIDEOS
    video = []
    name =[]
    thumb =[]

    ind = MENU[category]['indirizzo']
    req = Request(ind,headers={ 'User-Agent': 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16'})
    response = urlopen(req)
    the_page = BeautifulSoup(response,'html.parser')

    #xbmc.log('Sono a 286------: '+str(art), xbmc.LOGINFO)
    for link in the_page.find_all('article'):

        #xbmc.log('TEST------: ' + str(link), xbmc.LOGINFO)
        ind_t = link.find('a').get('href')
        #xbmc.log('indirizzo------: ' + str(ind_t), xbmc.LOGINFO)
        req=Request(ind_t,headers={ 'User-Agent': 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16'})
        response = urlopen(req)
        articolo=BeautifulSoup(response,'html.parser')

        video.append(articolo.iframe.get('src'))  # .get('scr')
        #xbmc.log('Articolo------: ' + str(articolo), xbmc.LOGINFO)
        #thumb.append(articolo.img.get('src'))
        thumb.append(link.img.get('src'))

        name.append(articolo.title.string)

    VIDEOS = []   
    i = 0
    while i < len(video):
        
        VIDEOS.append({'video': video[i],
                    'name': name[i].encode('utf-8'),
                    'thumb': thumb[i]})
        i = i + 1    
    return #VIDEOS


def list_categories():
    """
    Create the list of video categories in the Kodi interface.
    :return: None
    """    
    get_menu(indirizzo)
    listing = []
    # Iterate through categories    
    for index in range(len(MENU)):

        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=MENU[index]['name'])        
        list_item.setProperty('fanart_image', MENU[index]['fanart'])
        list_item.setArt({'thumb': MENU[index]['thumb']})
        url = '{0}?action=listing&category={1}&page=1&stringa={2}'.format(_url, index, " ")
        #url = MENU[index]['indirizzo']

        is_folder = True
        listing.append((url, list_item, is_folder))  
    #xbmc.log('Lista-----: '+str(listing),xbmc.LOGINFO)
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_UNSORTED) # non ordina, lascia cosi 
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_handle)
    return


def list_videos(category, page, cerca):
    """
    Create the list of playable videos in the Kodi interface.
    :param category: str
    :return: None
    """
    get_menu(indirizzo)
    global VIDEOS    
    cerca = cerca.replace('_','+')

    try:
       get_videos(category, page, cerca)
    except:
        return


    listing = []
    # Iterate through videos.
    for index in range(len(VIDEOS)):   
        list_item = xbmcgui.ListItem(label=VIDEOS[index]['name'])
        # Set a fanart image for the list item.
        # Here we use the same image as the thumbnail for simplicity's sake.
        #       list_item.setProperty('fanart_image', VIDEOS[index]['thumb'])
        list_item.setArt({'thumb': VIDEOS[index]['thumb']})
        # Set additional info for the list item.
        list_item.setInfo('video', {'title': VIDEOS[index]['name']})
        # Set additional graphics (banner, poster, landscape etc.) for the list item.
        # Again, here we use the same image as the thumbnail for simplicity's sake.
        list_item.setArt({'landscape': VIDEOS[index]['thumb']})
        # Set 'IsPlayable' property to 'true'.
        # This is mandatory for playable items!
        list_item.setProperty('IsPlayable', 'true')
        # Create a URL for the plugin recursive callback.
        # Example: plugin://plugin.video.example/?action=play&video=http://www.vidsplay.com/vids/crab.mp4
        #url = '{0}?action=play&video={1}'.format(_url, get_link(get_link1(VIDEOS[index]['video'])))
        url = '{0}?action=play&video={1}'.format(_url, VIDEOS[index]['video'])      
        is_folder = False 
        # Add our item to the listing as a 3-element tuple.
        listing.append((url, list_item, is_folder))
    is_folder = True    
    #list_item = xbmcgui.ListItem(label='Pagina Successiva ({0})'.format(str(page+1)))
    #list_item.setProperty('fanart_image', mPath+'icon.png')
    #url = '{0}?action=listing&category={1}&page={2}&stringa={3}'.format(_url,category,str(page+1),cerca.replace("+","_"))
    #listing.append((url, list_item, is_folder))
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.endOfDirectory(_handle)
    return

def play_video(path):
    """
    Play a video by the provided path.
    :param path: str
    :return: None
    """

    if path.find('www.youtube.com') > 0:
        codStart = path.find('embed/') + 6
        #codStop = path.find('?')
        video_id = path[codStart:]

        url = 'plugin://plugin.video.youtube/play/?video_id=%s' % video_id

        play_item = xbmcgui.ListItem(path=url)
        xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)

    else:
        play_item = xbmcgui.ListItem(path=npath)
        print
        play_item
        print
        "FINE"
        xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)
    return

    
def parameters_string_to_dict(parameters):
    # xbmc.log('PARAMETERS------: '+str(parameters),xbmc.LOGINFO)
    param_dict = dict(parse_qsl(parameters[1:]))
    return param_dict
    
def router(paramstring):
    """
    Router function that calls other functions
    depending on the provided paramstring
    :param paramstring:
    :return:
    """
    
    global VIDEOS  
    print("PARAMSTRING")

    params = dict(parse_qsl(paramstring))

    # Check the parameters passed to the plugin

    if params:
        if params['action'] == 'listing':
            # Display the list of videos in a provided category.            
            list_videos(int(params['category']),int(params['page']),params['stringa'])

        elif params['action'] == 'play':
            # Play a video from a provided URL
            play_video(params['video'])
    else:
        # If the plugin is called from Kodi UI without any parameters,
        # display the list of video categories
        list_categories()
        
if __name__ == '__main__':
    # Call the router function and pass the plugin call parameters to it.
    # We use string slicing to trim the leading '?' from the plugin call paramstring   
    print(sys.argv[0])
    print(sys.argv[1])
    print(sys.argv[2][1:])
    #xbmc.log('sys.argv ----: ' + str(sys.argv), xbmc.LOGINFO)




    finito = False
    router(sys.argv[2][1:])
