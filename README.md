# Artist Genre Similarity Graph
This project builds a graph connecting Japanese music artists based on shared genres and collaborations using the Spotify API and musicbrainzngs.

Project Overview:
- Fetches artists from a seed list using the Spotify Web API.
- Collects each artist's genre tags.
- Connects artists if they share at least one genre.
- Looks for artist collaborations and depicts them.
- Visualizes the resulting graph with NetworkX and Matplotlib.

## Data Sources
- Artist/genre data: Spotify API (`artist_related_artists` and `search` endpoints)
- Genres are standardized by Spotify (e.g., "j-pop", "j-rock")
- musicbrainz for artist collaborations and recording credits (featuring artists)

## Used
- Python 3.12
- Spotipy (Spotify Web API wrapper)
- NetworkX (graph building)
- Matplotlib (graph visualization)
- musicbrainz (python library)

## Future Improvements/Challenges faced
- Collaboration edge cases need to be improved
- Improve graph layout for larger datasets
- Allow user input to select seed artists dynamically
