import json
import re
import requests
from bs4 import BeautifulSoup
from typing import List


class Video:
    def __init__(self, link):
        # link exists ? 
        if not(link.startswith("https://www.youtube.com/watch?v=")):
            raise Exception("URL invalid")

        html = requests.get(link)        
        self.soup = BeautifulSoup(html.text, "html.parser")

        # video exists ?
        if(self.soup.find("meta", itemprop="name") is None):
            raise Exception("Video not existing")

        self.link = link
        self.description = None

    def _getTitle(self): 
        return self.soup.find("meta", itemprop="name")['content']

    def _getAuthor(self): 
        return self.soup.find("span", itemprop="author").next.next['content']

    def _getLikes(self):
        #From https://www.javatpoint.com/how-to-extract-youtube-data-in-python
        data = re.search(r"var ytInitialData = ({.*?});", self.soup.prettify()).group(1)  
        data_json = json.loads(data)

        # extract the likes from the json exctracted from the script  
        videoPrimaryInfoRenderer = data_json['contents']['twoColumnWatchNextResults']['results']['results']['contents'][0]['videoPrimaryInfoRenderer']
        likes_label = videoPrimaryInfoRenderer['videoActions']['menuRenderer']['topLevelButtons'][0]['segmentedLikeDislikeButtonRenderer']['likeButton']['toggleButtonRenderer']['defaultText']['accessibility']['accessibilityData']['label'] 
        
        # keep only the name
        likes = re.sub(r'[^0-9]', '', likes_label)
        return int(likes)
        

    def _getDescription(self):
        #From https://stackoverflow.com/questions/72354649/how-to-scrape-youtube-video-description-with-beautiful-soup
        # take everthing from the shortDescription in json to the isCrawlable which is just after 
        # line 32 I had to delete some of the characters from the resutl of Beautiful soup so I cannot use self.soup.find("shortDescription") alone
        pattern = re.compile(r'(?<=shortDescription":").*(?=","isCrawlable)')
        self.description = pattern.findall(str(self.soup))[0].replace('\\n','\n')

        return self.description

    def _getLinks(self):
        if(self.description is None):
            self.description = self._getDescription()
        
        description = self.description

        # Get Links
        # Check every blocks that start with https 
        res = re.findall(r"(?P<url>https?://[^\s]+)", description)

        # Get Timestamp
        # convert the format
        res += re.findall(r"[0-9]+:[0-9]{2}", description)

        return res

 

    def getData(self):
        d = {}
        d['Title'] = self._getTitle()
        d['Author'] = self._getAuthor()
        d['NbLikes'] = self._getLikes()
        d['Description'] = self._getDescription()
        d['Links'] = self._getLinks()

        return d