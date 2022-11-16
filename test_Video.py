    """
    fichier de test des fichiers Video.py et scrapper.py
    Auteur : Titouan Riot
    https://github.com/titouanriot/archiMicro/
    """


import pytest
from Video import Video


class TestVideo:

    def testUrlValid(self):
        v = Video("https://www.youtube.com/watch?v=4wTADlDJRQs")
        # if description is None it means it did not raise the Exception "URL invalid" 
        assert(v.description is None) is True

    def testUrlInvalid(self):
        with pytest.raises(Exception, match=r"URL invalid") :
            v = Video("whatever")

    def testVideoDoesntExist(self):
        with pytest.raises(Exception, match=r"Video not existing"):
            v = Video("https://www.youtube.com/watch?v=kldjfmqlksf")

    def testgetTitle(self):
        v = Video("https://www.youtube.com/watch?v=H_N-VhSsnUw")
        assert(v._getTitle() == "Afrikanda teaser 2021") is True

    def testgetAuthor(self):
        v = Video("https://www.youtube.com/watch?v=EcYcIAaTeRA")
        assert(v._getAuthor() == "Fouloscopie") is True

    def testDescription(self):
        v = Video("https://www.youtube.com/watch?v=H_N-VhSsnUw")
        description = "Pour d\u00e9buter 2021 en beaut\u00e9, nous vous mettons au d\u00e9fi: le d\u00e9fi de l'histoire!"
        assert(v._getDescription() == description) is True
    
    def testgetLikes(self):
        v = Video("https://www.youtube.com/watch?v=H_N-VhSsnUw")
        assert(v._getLikes() == 9) is True
    
    def testgetNoLink(self):
        v = Video("https://www.youtube.com/watch?v=H_N-VhSsnUw")
        assert(len(v._getLinks()) == 0) is True

    def testgetLink(self):
        v = Video("https://www.youtube.com/watch?v=EcYcIAaTeRA")
        assert(v._getLinks()[0] == "http://audible.fr/fouloscopie") is True

   

    