import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import networkx as nx
import matplotlib.pyplot as plt
import musicbrainzngs
import matplotlib.patches as mpatches
from collections import defaultdict
import ssl
import certifi
import urllib.request

# SSL fix for cert verification
ssl_context = ssl.create_default_context(cafile=certifi.where())
opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ssl_context))
urllib.request.install_opener(opener)

# Initialize MusicBrainz
musicbrainzngs.set_useragent("SI507-Final-Project", "1.0")
musicbrainzngs.set_rate_limit(False)


# Load Spotify API credentials
load_dotenv()
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

# Step 1: Fetch artist data from both APIs
def fetch_artist_data(seed_artists):
    artist_genres = {}
    collaborations = defaultdict(list)
    
    for name in seed_artists:
        # Spotify data (genres)
        sp_res = sp.search(q=name, type="artist", limit=1)
        if not sp_res["artists"]["items"]:
            print(f"Spotify: Artist '{name}' not found!")
            continue
        
        spotify_artist = sp_res["artists"]["items"][0]
        artist_name = spotify_artist["name"]  
        artist_genres[artist_name] = spotify_artist.get("genres", [])
        
        # MusicBrainz data (collaborations)
        try:
            mb_res = musicbrainzngs.search_artists(artist=name)
            if not mb_res["artist-list"]:
                print(f"MusicBrainz: No results for {name}")
                continue
                
            artist_id = mb_res["artist-list"][0]["id"]
            collab_data = musicbrainzngs.browse_recordings(artist=artist_id, limit=25)
            
            for recording in collab_data["recording-list"]:
                if "artist-credit" in recording:
                    for credit in recording["artist-credit"]:
                        if isinstance(credit, dict):
                            collab_name = credit["artist"]["name"]
                            if collab_name != artist_name:
                                collaborations[artist_name].append(collab_name)
                                
        except Exception as e:
            print(f"Error processing {name}: {type(e).__name__} - {str(e)[:100]}")
    
    return artist_genres, collaborations

# Step 2: Build graph with BOTH genre and collaboration data
def build_graph(artist_genres, collaborations):
    G = nx.Graph()
    
    # Add nodes with genre attributes
    for artist, genres in artist_genres.items():
        G.add_node(artist, genres=genres)
    
    # Add edges based on shared genres (Spotify)
    artists = list(artist_genres.keys())
    for i in range(len(artists)):
        for j in range(i + 1, len(artists)):
            shared_genres = set(artist_genres[artists[i]]) & set(artist_genres[artists[j]])
            if shared_genres:
                G.add_edge(artists[i], artists[j], weight=len(shared_genres), type="genre")
    
    # Add edges based on collaborations (MusicBrainz)
    for artist, collabs in collaborations.items():
        for collab in collabs:
            if collab in artist_genres:
                G.add_edge(artist, collab, type="collaboration")
    
    print(f"Graph stats: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    print(f"Collaboration edges: {sum(1 for _,_,d in G.edges(data=True) if d['type']=='collaboration')}")
    return G

# Visualization 
def visualize_graph(G, artist_genres):
    if not os.path.exists("assets"):
        os.makedirs("assets")
        
    plt.figure(figsize=(14, 12))
    pos = nx.spring_layout(G, k=0.7, seed=42)
    
    # Node colors by genre 
    genre_color_map = {
        "indie rock": "lightblue",
        "alternative rock": "lightgreen",
        "bedroom pop": "pink",
        "indie pop": "orange",
        "pop": "violet",
        "rock": "red",
        "dream pop": "purple",
        "folk": "gold",
        "j-pop": "cyan",
        "j-rock": "lightcoral",
        "japanese indie": "lightpink",
        "j-rap": "lightyellow",
        "j-hip hop": "coral",
        "electronic": "yellow",
        "anime": "lightgray",
        "vocaloid": "silver",
        "japanese classical": "lightpink"
    }
    
    # Assign colors to nodes
    node_colors = []
    for artist in G.nodes():
        genres = G.nodes[artist].get("genres", [])
        color = "gray"
        for genre in genres:
            if genre.lower() in genre_color_map:
                color = genre_color_map[genre.lower()]
                break
        node_colors.append(color)
    
    # Draw edges by type
    genre_edges = [(u,v) for u,v,d in G.edges(data=True) if d['type']=='genre']
    collab_edges = [(u,v) for u,v,d in G.edges(data=True) if d['type']=='collaboration']
    
    nx.draw_networkx_edges(G, pos, edgelist=genre_edges, edge_color="lightgray", width=1)
    nx.draw_networkx_edges(G, pos, edgelist=collab_edges, edge_color="red", width=2, style="dashed")
    
    # Draw nodes and labels
    nx.draw_networkx_nodes(G, pos, node_size=500, node_color=node_colors)
    nx.draw_networkx_labels(G, pos, font_size=8)
    
    # Add legend
    genre_patch = mpatches.Patch(color='lightgray', label='Genre Similarity')
    collab_patch = mpatches.Patch(color='red', label='Collaborations')
    plt.legend(handles=[genre_patch, collab_patch], loc='upper right')
    
    plt.title("Japanese Artist Network (Genres & Collaborations)")
    plt.axis('off')
    plt.tight_layout()
    plt.savefig("assets/combined_graph.png")
    plt.close()

# Interactive menu
if __name__ == "__main__":
    seed_artists = [
        "Lamp",
        "Ichiko Aoba",
        "Lily Chou-Chou",
        "Magnolia Cacophony",
        "utari",
        "The Natsuyasumi Band",
        "Kaede",
        "Fishmans",
        "Nanase Aikawa",
        "Shiina Ringo", 
        "YOASOBI",
        "Centimillimental",
        "Ado",
        "Fujii Kaze",
        "Yumi Arai",
        "Yumi Matsutoya",
        "Ayase",
        "Given",
        "Gen Hoshino",
        "Joe Hisaishi",
        "Aoi Tejima",
        "Macaroni Enpitsu",    
        "yama",
        "Vaundy",
        "Kikuo",
        "Eve",
        "Rokudenashi",
        "natori",
        "Satoshi Takebe"
        "Wednesday Campanella",
        "Ryuichi Sakamoto",
        "Cornelius",
        "KIRINJI",
        "Yorushika",
        "Aimer",
        "Aimyon",
        "Official Hige Dandism",
        "King Gnu",
        "RADWIMPS",
        "Spitz",
        "Tokyo Incidents",
        "Utada Hikaru",
        "Sheena Ringo",
        "Suchmos",
        "LUCKY TAPES",
        "cero",
        "Sakanaction",
        "Awesome City Club",
        "Hikaru Utada",
        "Zutomayo",
        "Kenshi Yonezu",
        "Rei",
        "iri",
        "Haruka Nakamura",
        "Kokia",
        "Nujabes",
        "Shugo Tokumaru",
        "Mariya Takeuchi",
        "Tatsuro Yamashita",
        "Akiko Yano",
        "TWEEDEES",
        "Hitomitoi",
        "YUKI",
        "Chara"
    ]
    
    print("Fetching data from Spotify and MusicBrainz...")
    artist_genres, collaborations = fetch_artist_data(seed_artists)
    G = build_graph(artist_genres, collaborations)
    
    while True:
        print("\n1. Genre connections\n2. Collaboration path\n3. Key artists\n4. Visualize\n5. Exit")
        choice = input("Choose: ")
        
        if choice == "1":
            artist = input("Artist: ")
            if artist in G:
                print(f"Genre connections: {[n for n in G.neighbors(artist) if G.edges[artist,n]['type']=='genre']}")
            else:
                print("Artist not found in graph!")
        
        elif choice == "2":
            a1, a2 = input("Artist 1: "), input("Artist 2: ")
            try:
                path = nx.shortest_path(G, a1, a2)
                for i in range(len(path)-1):
                    print(f"{path[i]} → {path[i+1]} ({G.edges[path[i],path[i+1]]['type']})")
            except nx.NetworkXNoPath:
                print("No path exists between these artists")
            except nx.NodeNotFound:
                print("One or both artists not found!")
            except Exception as e:
                print(f"Error: {e}")
        
        elif choice == "3":
            if G.number_of_nodes() > 0:
                print("\nMost connected artists:")
                for artist, degree in sorted(G.degree(), key=lambda x: x[1], reverse=True)[:5]:
                    print(f"{artist}: {degree} connections")
            else:
                print("Graph is empty!")
        
        elif choice == "4":
            visualize_graph(G, artist_genres)
            print("Graph saved to assets/combined_graph.png")
        
        elif choice == "5":
            print("Exiting...")
            break
        
        else:
            print("Invalid choice, please try again")