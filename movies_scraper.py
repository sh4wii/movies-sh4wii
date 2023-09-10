import requests
from bs4 import BeautifulSoup

url_list = {}
api_key = "05ec289b4931dbc5c38de970e22ec240c72be101"

def search_movies(query):
    movies_list = []
    movies_details = {}
    website = BeautifulSoup(requests.get(f"https://moviesmod.cc/?s={query.replace(' ', '+')}").text, "html.parser")
    
    # Using 'a' as a common tag for links; adjust if necessary.
    movies = website.find_all("a", {'class': 'js'})
    
    for movie in movies:
        if movie:
            movies_details["id"] = f"link{movies.index(movie)}"
            movies_details["title"] = movie.text
            url_list[movies_details["id"]] = movie['href']
        movies_list.append(movies_details)
        movies_details = {}
    return movies_list

def get_movie(query):
    movie_details = {}
    movie_page_link = BeautifulSoup(requests.get(f"{url_list[query]}").text, "html.parser")
    
    title = movie_page_link.find("a", {'class': 'js'}).text  # Adjust if the tag is different on the details page.
    movie_details["title"] = title
    
    # If the image has the same class or a different one, adjust accordingly
    img = movie_page_link.find("img", {'class': 'js'})['src']
    movie_details["img"] = img
    
    # Assuming movie download links also use the same class
    links = movie_page_link.find_all("a", {'class': 'js'})
    
    final_links = {}
    for i in links:
        url = f"https://urlshortx.com/api?api={api_key}&url={i['href']}"
        response = requests.get(url)
        link = response.json()
        final_links[f"{i.text}"] = link['shortenedUrl']
    movie_details["links"] = final_links
    
    return movie_details
