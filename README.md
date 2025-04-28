🎵 Artist Genre Similarity Graph
This project builds a graph connecting music artists based on shared genres using the Spotify API.

📋 Project Overview
Fetches artists from a seed list using the Spotify Web API.

Collects each artist's genre tags.

Connects artists if they share at least one genre.

Visualizes the resulting graph with NetworkX and Matplotlib.

## Data Sources
- Artist/genre data: Spotify API (`artist_related_artists` and `search` endpoints)
- Genres are standardized by Spotify (e.g., "j-pop", "j-rock")

🛠 Technologies Used
Python 3.12

Spotipy (Spotify Web API wrapper)

NetworkX (graph building)

Matplotlib (graph visualization)

🚀 How to Run
Clone the repository:

bash
Copy
Edit
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Set up your environment:

Create a .env file with your Spotify API credentials:

ini
Copy
Edit
SPOTIPY_CLIENT_ID=your_client_id
SPOTIPY_CLIENT_SECRET=your_client_secret
Create the assets folder:

bash
Copy
Edit
mkdir assets
Run the script:

bash
Copy
Edit
python3 graph.py
View your graph output:

Check assets/genre_graph.png

📚 Notes
Some major artists (like Taylor Swift, Lady Gaga) may not return full genre or related-artist data through the API due to Spotify platform restrictions.

You can adjust the seed artists list inside graph.py to explore different artist networks.

💡 Future Improvements
Color nodes by primary genre.

Improve graph layout for larger datasets.

Allow user input to select seed artists dynamically.

Highlight clusters and genre communities.