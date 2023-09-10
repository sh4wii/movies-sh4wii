import requests
from bs4 import BeautifulSoup

url_list = {}
api_key = "05ec289b4931dbc5c38de970e22ec240c72be101"

def search_movies(query):
    movies_list = []
    movies_details = {}
    website = BeautifulSoup(requests.get(f"https://moviesmod.cc/?s={query.replace(' ', '+')}").text, "html.parser")
    
    # Update the below line based on the website's structure. 
    # For example, if movies are listed as <div class="movie-title">, you'd use 'div' and 'movie-title'.
    movies = website.find_all("appropriate_tag", {'class': 'appropriate_class_name'})
    
    for movie in movies:
        if movie:
            # Adjust these lines based on the website's structure
            movies_details["id"] = f"link{movies.index(movie)}"
            movies_details["title"] = movie.find("appropriate_tag_for_title", {'class': 'appropriate_class_name_for_title'}).text
            url_list[movies_details["id"]] = movie['href']
        movies_list.append(movies_details)
        movies_details = {}
    return movies_list

def get_movie(query):
    movie_details = {}
    movie_page_link = BeautifulSoup(requests.get(f"{url_list[query]}").text, "html.parser")
    
    # Adjust these lines as per the website's structure for individual movie pages
    title = movie_page_link.find("appropriate_tag_for_title", {'class': 'appropriate_class_name_for_title'}).text
    movie_details["title"] = title
    img = movie_page_link.find("appropriate_tag_for_img", {'class': 'appropriate_class_name_for_img'})['data-bg_or_src']
    movie_details["img"] = img
    links = movie_page_link.find_all("appropriate_tag_for_links", {'class': 'appropriate_class_name_for_links'})
    
    final_links = {}
    for i in links:
        # If you continue using the same URL shortening service
        url = f"https://urlshortx.com/api?api={api_key}&url={i['href']}"
        response = requests.get(url)
        link = response.json()
        final_links[f"{i.text}"] = link['shortenedUrl']
    movie_details["links"] = final_links
    
    return movie_details
