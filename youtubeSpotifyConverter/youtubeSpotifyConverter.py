import requests
from base64 import b64encode
from urllib.parse import urlparse, parse_qs, urlencode
from time import time

class youtubeSpotifyConverter:
    # the URLs used to make requests
    SP_URL = "https://api.spotify.com/v1/"
    YT_URL = "https://youtube.googleapis.com/youtube/v3/"

    def __init__(self, YT_API_KEY:str=None, SP_REFRESH_TOKEN:str=None, SP_CLIENT_ID:str=None, SP_CLIENT_SECRET:str=None):
        """
        Sets the api keys. If no arguments are passed, nothing will work.

        :param YT_API_KEY The youtube API key. (optional if you don't want youtube or converter functions)
        :type YT_API_KEY: str

        :param SP_REFRESH_TOKEN: The spotify API refresh token which belongs to a particular user. (optional if you don't need access to a user account or aren't using spotify functions)
        :type SP_CLIENT_ID: str

        :param SP_CLIENT_ID: The spotify API client id. (optional if you don't want spotify or converter functions or are using a refresh token)
        :type SP_CLIENT_ID: str

        :param SP_CLIENT_SECRET: The spotify API client secret. (optional if you don't want spotify or converter functions or are using a refresh token)
        :type SP_CLIENT_SECRET: str

        """
        
        # this takes a look at all arguments passed and decides what methods are usable from that
        if YT_API_KEY != None:
            # this key will be used always for youtube API requests
            self.YT_key = YT_API_KEY

            self.converter = True
            self.youtube = True
        else:
            self.converter = False
            self.youtube = False
        
        if SP_REFRESH_TOKEN != None:
            self.SP_REFRESH_TOKEN = SP_REFRESH_TOKEN

            self.spotify_mode = 1 # this indicates how spotify is being accessed, whether by user token (1) or using client credentials (2) or with no spotify access (0)
        elif SP_CLIENT_ID != None and SP_CLIENT_SECRET != None:
            # these keys are only used to get an access token
            self.SP_CLIENT_ID = SP_CLIENT_ID
            self.SP_CLIENT_SECRET = SP_CLIENT_SECRET

            self.spotify_mode = 2
        else:
            self.spotify_mode = 0
            self.converter = False

        self.timer = 0
        self.SP_getToken()

    def SP_getToken(self):
        if self.spotify_mode != 0:
            if time - self.timer >= 3600:
                if self.spotify_mode == 1:
                    token = self.__SP_refreshToken()
                elif self.spotify_mode == 2:
                    token = self.__SP_clientCreds()
                
                self.SP_token = token
                return token
            else:
                return self.SP_token

    def __SP_refreshToken(self):
        """
        gets a token for making requests to the spotify API via refresh token
        """
    
        url = "https://accounts.spotify.com/api/token" # token request url

        # converts the client id and secret in base64 that spotify will understand
        credentials = self.SP_CLIENT_ID + ":" + self.SP_CLIENT_SECRET
        credentials = credentials.encode("ascii")
        credentials = b64encode(credentials).decode()

        # the request data
        headers = {'Authorization': 'Basic ' + str(credentials), "Content-Type": "application/x-www-form-urlencoded"}
        params = {"grant_type" : "authorization_code", "code" : self.SP_REFRESH_TOKEN, "redirect_uri": self.SP_REDIRECT_URI}

        # send the request
        response = requests.post(url=url,headers=headers, params=params)

        # raise an exception if the request has a bad status code if not return the token
        response.raise_for_status()
        return(response.json()["access_token"])

    def __SP_clientCreds(self):
        """
        gets a token for making requests to the spotify API via client credentials.
        """

        url = "https://accounts.spotify.com/api/token" # token request url

        # converts the client id and secret in base64 that spotify will understand
        credentials = self.SP_CLIENT_ID + ":" + self.SP_CLIENT_ID
        credentials = credentials.encode("ascii")
        credentials = b64encode(credentials).decode()

        # the request data
        headers = {'Authorization': 'Basic ' + str(credentials), "Content-Type": "application/x-www-form-urlencoded"}
        params = {"grant_type" : "client_credentials",}

        # send the request
        response = requests.post(url=url,headers=headers, params=params)
        
        # raise an exception if the request has a bad status code if not return the token
        response.raise_for_status()
        return(response.json()["access_token"])

    def SP_userAuth(self, scope:str, redirect_uri:str, state):
        
        url = "https://accounts.spotify.com/authorize?"

        params = {"client_id": self.SP_id,
                  "response_type": "code",
                  "redirect_uri": redirect_uri,
                  "state": state,
                  "scope": scope
                  }
                   
        return(url + urlencode(params))

    def SP_getToken(self, code:str, redirect_uri:str):
    
        url = "https://accounts.spotify.com/api/token" # token request url

        # converts the client id and secret in base64 that spotify will understand
        credentials = self.SP_CLIENT_ID + ":" + self.SP_CLIENT_SECRET
        credentials = credentials.encode("ascii")
        credentials = b64encode(credentials).decode()

        # the request data
        headers = {'Authorization': 'Basic ' + str(credentials), "Content-Type": "application/x-www-form-urlencoded"}
        params = {"grant_type" : "authorization_code", "code" : self.SP_REFRESH_TOKEN, "redirect_uri": self.SP_REDIRECT_URI}

        # send the request
        response = requests.post(url=url,headers=headers, params=params)
        
        # raise an exception if the request has a bad status code if not return the token
        response.raise_for_status()
        return(response.json()["access_token"])

    def SP_createPlaylist(self, name:str, description:str="", public:bool=True):
        """
        creates a spotify playlist

        :param token: The token to 
        :type description: str

        :param name: The name of the new playlist
        :type name: str
        
        :param description: The description of the new playlist
        :type description: str

        :param public: If the playlist is public or not (defaults to True)
        :type public: bool
        """
        
        headers = {
            "Content-Type" : "application/json",
            "Authorization" : f"Bearer {self.SP_token}"
        }

        params = {
            "name" : name,
            "description" : description,
            "public" : public,
        }

        url=f"{self.SP_URL}users/{id}/playlists"

        response = requests.get(url=url, headers=headers, params=params)
        
        # raise an exception if the request has a bad status code if not return
        response.raise_for_status()
        return(response.json())

    def SP_search(self, keyword:str, limit:int=1):
        """
        gets the first song from a spotify search and returns info about it in json form

        :param keyword: The string to search for.
        :type keyword: str

        :param limit: The amount of tracks to return.
        :type limit: int

        """

        # the request data
        headers = {
            "Content-Type" : "application/json",
            "Authorization" : f"Bearer {self.SP_token}"
        }

        params = {
            "q" : keyword,
            "type" : "track",
            "include_external" : "audio",
            "limit" : limit,
        }

        response = requests.get(url=self.SP_URL+"search/", headers=headers, params=params)
        
        # raise an exception if the request has a bad status code if not return
        response.raise_for_status()
        return(response.json())

    def SP_get(self, id:str):
        """
        gets a spotify song from an Id and returns info about it in json form

        :param id: The song that you want to find's id.
        :type id: str

        :return: Json data about the channel specified in the id
        :rtype: json
        """

        headers = {
            "Content-Type" : "application/json",
            "Authorization" : f"Bearer {self.SP_token}"
        }

        url=f"{self.SP_URL}tracks{id}"

        response = requests.get(url=url, headers=headers)

        # raise an exception if the request has a bad status code if not return
        response.raise_for_status()
        return(response.json())

    def YT_search(self, keyword: str, limit=1):
        """
        gets the first song from a youtube search and returns info about it in json form

        :param keyword: The keyword to search for.
        :type keyword: str

        :param limit: The amount of tracks to return.
        :type limit: int

        :return: Json data about the video found by the search
        :rtype: object
        """

        response = requests.get(self.YT_URL+f"search?part=snippet&maxResults={limit}&q={keyword}&key={self.YT_key}")

        # raise an exception if the request has a bad status code if not return
        response.raise_for_status()
        return(response.json())

    def YT_getVideo(self, id:str):
        """
        gets a youtube video from an Id and returns info about it in json form

        :param id: The video that you want to find's id.
        :type id: str

        :return: Json data about the video specified in the id
        :rtype: object
        """

        response = requests.get(self.YT_URL+f"videos?part=snippet%2CcontentDetails%2Cstatistics&id={id}&key={self.YT_key}")
        
        # raise an exception if the request has a bad status code if not return
        response.raise_for_status()
        return response.json()

    def YT_getChannel(self, id:str):
        """
        gets a youtube channel from an Id and returns info about it in json form

        :param id: The channel that you want to find's id.
        :type id: str

        :return: Json data about the channel specified in the id
        :rtype: object
        """

        response = requests.get(self.YT_URL+f"channels?part=snippet%2CcontentDetails%2Cstatistics&id={id}&key={self.YT_key}")
        
        # raise an exception if the request has a bad status code if not return
        response.raise_for_status()
        return response.json()

    def YT_intoMusic(self, URL:str):
        """
        turns a youtube URL into a youtube music URL. Note: this will not always work, and will not work on URLs to anything that isn't music

        :param URL: The youtube URL that will be changed
        :type URL: str

        :return: A youtube music URL
        :rtype: str
        """

        return(URL.replace("www", "music"))

    def YT_intoRegular(self, URL:str):
        """
        turns a youtube music URL into a youtube URL. Note: this will not always work, and will not work on URLs to anything that isn't music

        :param URL: The youtube music URL that will be changed
        :type URL: str

        :return: A youtube URL
        :rtype: str
        """

        return(URL.replace("music", "www"))

    def YT_idIntoURL(self, id:str):
        """
        turns a youtube Id into a URL

        :param id: The Id that you want a URL for
        :type id: str

        :return: A youtube URL
        :rtype: str
        """

        return "https://www.youtube.com/watch?v=" + str(id)

    def C_fromLink(self, link:str):
        """
        takes in a link to either youtube/youtube music or spotify and returns a links to the same content in other services.
        services names: youtube, youtubeMusic, spotify
        
        :param link: The link you want to convert
        :type link: str

        :param music: Whether or not to also include a youtube music link
        :type music: bool

        :return: A dictionary of key-value pairs where the key is the service name and value is the URL that should match the name. Also has a pair called name containing the song and it's artist's name
        :rtype: dict
        """

        result = {
            "youtube" : "",
            "youtubeMusic" : "",
            "spotify" : "",
            "name" : ""
        }

        if link.find("spotify") != -1:
            id = urlparse(link).path.replace("/track", "") # find track id
            json = self.SP_get(id) # get song info
            name = json["name"] + " " + json["artists"][0]["name"] # change song info into a name for searching
            name = name.replace(" - Topic", "")
            name = name.replace("VEVO", "")

            # get tracks and fill the results dictionary
            result["spotify"] = link
            result["name"] = name
            result["youtube"] = self.YT_idIntoURL(self.YT_search(name)["items"][0]["id"]["videoId"])
            result["youtubeMusic"] = self.YT_intoMusic(result["youtube"])

        else:
            # get id different ways depend on if it's a shortened url
            if link.find("youtu.be") != -1:
                id = urlparse(link).path.replace("/", "")

                link = self.YT_idIntoURL(id) # replace the shortened url with a regular one
            else:
                id = parse_qs(urlparse(link).query)["v"][0]

            # make a request for video data and take the name and artist name from the video data
            json = self.YT_getVideo(id)
            name = json["items"][0]["snippet"]["title"] + " " + json["items"][0]["snippet"]["channelTitle"]

            # remove "VEVO" and " - Topic" from the name. This should help improve accuracy
            name = name.replace(" - Topic", "")
            name = name.replace("VEVO", "")

            # fill the dictionary with the links and names by searching on spotify and using the given link

            if link.find("music") != -1:
                result["youtube"] = self.YT_intoRegular(link)
                result["name"] = name
                result["youtubeMusic"] = link
                result["spotify"] = self.SP_search(name)["tracks"]["items"][0]["external_urls"]["spotify"]
            else:
                result["youtube"] = link
                result["name"] = name
                result["youtubeMusic"] = self.YT_intoMusic(link)
                result["spotify"] = self.SP_search(name)["tracks"]["items"][0]["external_urls"]["spotify"]

        return(result)

    def C_fromTitle(self, name:str):
        """
        takes in a song name and returns links to youtube, youtube music, and spotify that should match
        services names: youtube, youtubeMusic, spotify
        
        :param name: The name of the song (you can get more accurate searches with artist in the name) that you want links to
        :type name: str

        :return: A dictionary of key-value pairs where the key is the service name and value is the URL that should match the name
        :rtype: dict
        """

        result = {
            "youtube" : "",
            "youtubeMusic" : "",
            "spotify" : "",
            "name" : name
        }

        result["youtube"] = self.YT_idIntoURL(self.YT_search(name)["items"][0]["id"]["videoId"])
        result["youtubeMusic"] = self.YT_intoMusic(result["youtube"])
        result["spotify"] = self.SP_search(name)["tracks"]["items"][0]["external_urls"]["spotify"]

        return(result)