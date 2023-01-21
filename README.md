# youtubeSpotifyConverter
A library that allows you to convert between Spotify, YouTube and YouTube Music URLs (only works on songs at the moment). 
Includes methods for basic calls to the YouTube and Spotify APIs.

## Installation
```
pip install youtubeSpotifyConverter
```

## Get started
How to convert a YouTube URL into a Spotify and YouTube Music URL
```Python
from youtubeSpotifyConverter import youtubeSpotifyConverter

# Instantiate a youtubeSpotifyConverter object
converter = youtubeSpotifyConverter([YOUTUBE_API_KEY], [SPOTIFY_CLIENT_ID], [SPOTIFY_CLIENT_SECRET])

# Call the C_fromLink method
links = converter.C_fromLink("Youtube/Youtube Music or Spotify URL")

# Call the C_fromTitle method
links = converter.C_fromTitle("Song Title")
```

## GitHub and PyPI pages
GitHub: https://github.com/FileNotFound7/youtubeSpotifyConverter
PyPI: https://pypi.org/project/youtubeSpotifyConverter/