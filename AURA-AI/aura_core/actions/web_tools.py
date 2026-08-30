import webbrowser
import urllib.parse

def open_website(site_name: str) -> str:
    site_name = site_name.lower().strip()
    sites = {
        "youtube": "https://www.youtube.com",
        "google": "https://www.google.com",
        "github": "https://www.github.com",
        "chatgpt": "https://chatgpt.com",
        "chrome": "https://www.google.com"
    }
    if site_name in sites:
        webbrowser.open(sites[site_name])
        return f"Opening {site_name.capitalize()}"
    return f"Sorry, I don't know the website {site_name}"

def google_search(query: str) -> str:
    if query:
        encoded_query = urllib.parse.quote(query)
        webbrowser.open(f"https://www.google.com/search?q={encoded_query}")
        return f"Searching Google for {query}"
    return "What would you like me to search for?"

def play_music(song_name: str) -> str:
    """
    Searches and plays music on YouTube using urllib.parse and webbrowser.
    """
    cleaned_name = song_name.strip()
    
    # Strip unnecessary keywords if present
    for suffix in ["on youtube", "in youtube", "from youtube"]:
        if cleaned_name.lower().endswith(suffix):
            cleaned_name = cleaned_name[:-len(suffix)].strip()

    if not cleaned_name:
        webbrowser.open("https://music.youtube.com")
        return "Opening YouTube Music"
    
    encoded_song = urllib.parse.quote(cleaned_name)
    url = f"https://www.youtube.com/results?search_query={encoded_song}"
    webbrowser.open(url)
    return f"Playing {cleaned_name} on YouTube"
