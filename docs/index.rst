.. youtubeSpotifyConverter documentation master file, created by
   sphinx-quickstart on Fri Jan 20 20:21:49 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to youtubeSpotifyConverter's documentation!
===================================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

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

**GitHub, ReadTheDocs and PyPI pages**

* GitHub: https://github.com/FileNotFound7/youtubeSpotifyConverter
* PyPI: https://pypi.org/project/youtubeSpotifyConverter/
* ReadTheDocs: https://youtubespotifyconverter.readthedocs.io/en/latest/

**Method naming**

* Methods and variables that relate to youtube have YT\_ before the name
* Methods and variables that relate to spotify have SP\_ before the name
* Methods that make up the link converter have C\_ before the name

.. toctree::
   :maxdepth: 2
   :caption: Python API:

   source/api/youtubeSpotifyConverter

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

