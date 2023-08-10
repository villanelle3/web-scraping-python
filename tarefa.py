import requests
import csv
from bs4 import BeautifulSoup

URL = "https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
}

page = requests.get(URL, headers=headers)

soup = BeautifulSoup(page.content, "html.parser")

results = soup.find(
    "ul",
    attrs={
        "class": "ipc-metadata-list ipc-metadata-list--dividers-between sc-3a353071-0 wTPeg compact-list-view ipc-metadata-list--base",
        "role": "presentation",
    },
)
# print(results.prettify())

film_elements = results.find_all(
    "li", class_="ipc-metadata-list-summary-item sc-bca49391-0 eypSaE cli-parent"
)

# for movie in film_elements:
#     print(movie, end="\n"*2)

for movie in film_elements:
    try:
        titulo = movie.find("h3", class_="ipc-title__text")
        data = movie.find(
            "span", class_="sc-14dd939d-6 kHVqMR cli-title-metadata-item"
        )
        rating = movie.find(
            "span",
            class_="ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating",
        )
        print(titulo.text.strip())
        print(data.text.strip())
        print(rating.text.strip())
        print()
        with open("movies.csv", mode="a") as file:
            movie_writer = csv.writer(
                file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
            )
            movie_writer.writerow(
                [
                    titulo.text.strip(),
                    data.text.strip(),
                    rating.text.strip(),
                    "plot_text",
                ]
            )
    except Exception as e:
        print(e)
