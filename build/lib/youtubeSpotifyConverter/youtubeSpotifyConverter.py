import requests
from base64 import b64encode
from urllib.parse import urlparse, parse_qs

class youtubeSpotifyConverter:
    """
    A module that converts spotify URLs to youtube and vice versa.
    There is the ability to output a youtube music URL but it is not 100% reliable as links may not work properly so it is not recommended to use that function.

    The API keys are passed in on instantiation.
    You can get the keys at:
        Youtube: https://console.cloud.google.com/apis/credentials
        Spotify: https://developer.spotify.com/dashboard/applications

    Methods and variables that relate to youtube have YT_ before the name
    Methods and variables that relate to spotify have SP_ before the name
    Methods that make up the link converter have C_ before the name
    """

    # the URLs used to make requests
    SP_URL = "https://api.spotify.com/v1/"
    YT_URL = "https://youtube.googleapis.com/youtube/v3/"

    def __init__(self, YT_API_KEY:str, SP_CLIENT_ID:str, SP_CLIENT_SECRET:str):
        """
        Sets the api keys.

        :param YT_API_KEY: The youtube API key.
        :type YT_API_KEY: str

        :param SP_CLIENT_ID: The spotify API client id.
        :type SP_CLIENT_ID: str

        :param SP_CLIENT_SECRET: The spotify API client secret.
        :type SP_CLIENT_SECRET: str

        """
        
        # this will be used always for youtube API requests
        self.YT_key = YT_API_KEY

        # these two will not be used after getting a token from the spotify API
        self.SP_id = SP_CLIENT_ID
        self.SP_secret = SP_CLIENT_SECRET

        # get an token for the spotify API
        self.__SP_authorise()

    def __SP_authorise(self):
        """
        gets a token for making requests to the spotify API
        """

        url = "https://accounts.spotify.com/api/token" # token request url

        # converts the client id and secret in base64 that spotify will understand
        credentials = self.SP_id + ":" + self.SP_secret
        credentials = credentials.encode("ascii")
        credentials = b64encode(credentials).decode()

        # the request data
        headers = {'Authorization': 'Basic ' + str(credentials), "Content-Type": "application/x-www-form-urlencoded"}
        params = {"grant_type" : "client_credentials",}

        # send the request
        response = requests.post(url=url,headers=headers, params=params)
        
        # raise an exception if the request fails or else save the token
        if response.status_code == 200:
            self.SP_token = response.json()["access_token"]
        else:
            raise Exception(f"Error response after requesting token.\nResponse status code: {response.status_code}\nResponse Content: {response.content}")

    def SP_search(self, keyword:str):
        """
        gets the first song from a spotify search and returns info about it in json form

        :param keyword: The string to search for.
        :type keyword: str

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
            "limit" : 1,
        }

        response = requests.get(url=self.SP_URL+"search/", headers=headers, params=params)

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

        return(response.json())

    def YT_search(self, keyword: str):
        """
        gets the first song from a youtube search and returns info about it in json form

        :param keyword: The keyword to search for.
        :type keyword: str

        :return: Json data about the video found by the search
        :rtype: object
        """

        response = requests.get(self.YT_URL+f"search?part=snippet&maxResults=1&q={keyword}&key={self.YT_key}")
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

            # fill the dictionary with the links and names by searching on spotify and using the given link
            result["youtube"] = link
            result["name"] = name
            result["youtubeMusic"] = self.YT_intoMusic(result["youtube"])
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
            "name" : ""
        }

        result["youtube"] = self.YT_idIntoURL(self.YT_search(name)["items"][0]["id"]["videoId"])
        result["youtubeMusic"] = self.YT_intoMusic(result["youtube"])
        result["spotify"] = self.SP_search(name)["tracks"]["items"][0]["external_urls"]["spotify"]

        return(result)