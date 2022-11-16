    """
    fichier de test du fichier Video.py
    Auteur : Titouan Riot
    https://github.com/titouanriot/archiMicro/
    
    """

import sys
import json

from Video import Video

NB_COMMENTS = 5

# Test number of parameters
if(len(sys.argv) != 5):
    raise Exception("make sure to run python3.10 scrapper.py --input 'input.json' output.json")

with open('input.json', 'r') as f:
    videosId = json.load(f)['videos_id']

res = []
for video in videosId:
    data = Video("https://www.youtube.com/watch?v=" + video).getData()
    data['Id'] = video
    res.append(data)

with open('output.json', 'w') as f:
    f.write(json.dumps(res, indent=4))
