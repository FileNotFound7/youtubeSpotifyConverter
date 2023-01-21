Getting Started
=======================

A library that allows you to convert between Spotify, YouTube and YouTube Music URLs (only works on songs at the moment). 
Includes methods for basic calls to the YouTube and Spotify APIs.

**Installation**

``pip install youtubeSpotifyConverter``

**Get started**

How to convert a YouTube URL into a Spotify and YouTube Music URL::

    from youtubeSpotifyConverter import youtubeSpotifyConverter

    # Instantiate a youtubeSpotifyConverter object
    converter = youtubeSpotifyConverter([YOUTUBE_API_KEY], [SPOTIFY_CLIENT_ID], [SPOTIFY_CLIENT_SECRET])

    # Call the C_fromLink method
    links = converter.C_fromLink("Youtube/Youtube Music or Spotify URL")

    # Call the C_fromTitle method, getting a 
    links = converter.C_fromTitle("Song Title")

**API keys**

The API keys are passed in on instantiation.
You can get the keys at:

* Youtube: https://console.cloud.google.com/apis/credentials
* Spotify: https://developer.spotify.com/dashboard/applications

**Method naming**

Methods and variables that relate to youtube have YT\_ before the name
Methods and variables that relate to spotify have SP\_ before the name
Methods that make up the link converter have C\_ before the name