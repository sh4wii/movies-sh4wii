import requests
from bs4 import BeautifulSoup
import time

api_key = "05ec289b4931dbc5c38de970e22ec240c72be101"
url_list = {}


def search_movies(query):
    try:
        movies_list = []
        movies_details = {}
        response = requests.get(f"https://185.53.88.104/?s={query.replace(' ', '+')}")
        response.raise_for_status()

        website = BeautifulSoup(response.text, "html.parser")
        movies = website.find_all("a", {'class': 'ml-mask jt'})

        for movie in movies:
            if movie:
                movies_details["id"] = f"link{movies.index(movie)}"
                movies_details["title"] = movie.find("span", {'class': 'mli-info'}).text
                url_list[movies_details["id"]] = movie['href']
                movies_list.append(movies_details)
                movies_details = {}
        return movies_list

    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        return []


def get_movie(query):
    try:
        movie_details = {}
        response = requests.get(f"{url_list[query]}")
        response.raise_for_status()

        movie_page_link = BeautifulSoup(response.text, "html.parser")

        if movie_page_link:
            title = movie_page_link.find("div", {'class': 'mvic-desc'}).h3.text
            movie_details["title"] = title
            img = movie_page_link.find("div", {'class': 'mvic-thumb'})['data-bg']
            movie_details["img"] = img
            links = movie_page_link.find_all("a", {'rel': 'noopener', 'data-wpel-link': 'internal'})
            final_links = {}
            for i in links:
                url = f"https://urlshortx.com/api?api={api_key}&url={i['href']}"
                link_response = requests.get(url)
                if link_response.status_code == 200:
                    link = link_response.json()
                    final_links[i.text] = link['shortenedUrl']
            movie_details["links"] = final_links
        return movie_details

    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        return {}


# Sample Usage
search_results = search_movies("money heist")
for movie in search_results:
    print(movie['id'], movie['title'])

selected_movie = input("Enter the movie id to get details: ")
details = get_movie(selected_movie)
print(details)
