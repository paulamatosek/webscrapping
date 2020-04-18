

import pymysql, requests

from bs4 import BeautifulSoup

from Model import top250
# 1. Wykonaj żądanie GET dla zadresu https://www.imdb.com/chart/top?ref_=nv_mv_250

class ImdbScrapper:
    def __init__(self):
        self.movies = []        # list obiektow kalsy modelu -> top250
    # self.obiekt -> zakres wydoczności obejmuje całąklasę ImdbScrapper
    def getTop250(self):
        try:
            self.page = requests.get("https://www.imdb.com/chart/top?ref_=nv_mv_250")
            print("Wykonano poprawnie żądanie")
            # print(self.page.content)
        except:
            print("Ups! Coś poszło nie tak")
    def scrappingTop250(self):
        # page.content -> zwraca zawartość żądania get
        html_content = BeautifulSoup(self.page.content, 'html.parser')
        # print(html_content.prettify())
        titles = html_content.find_all(class_ = "titleColumn")
        years = html_content.find_all('span', attrs={'class' : 'secondaryInfo'})
        ratings = html_content.find_all(class_ = "ratingColumn imdbRating")
        refs = html_content.find_all(class_ = "titleColumn")

        for index, title in enumerate(titles):
            titles[index] = str(titles[index]).split(">")[2].replace("</a","")
            years[index] = str(years[index]).split("(")[1].split(")")[0]
            ratings[index] = str(ratings[index]).split(">")[2].replace("</strong","")
            refs[index] = "https://www.imdb.com" + str(refs[index]).split('href="')[1].split('"')[0]
            director, stars = self.getMovieDetails(refs[index])
            # zapis danych o filmie do obiektu modelu
            movie = top250(titles[index], years[index], director, stars, ratings[index], refs[index])
            print(movie)
            self.movies.append(movie)   # dodawanie obiektu filmu do listy
    def getMovieDetails(self, url):
        details = requests.get(url)
        details_html = BeautifulSoup(details.content, 'html.parser')
        # pobierz reżysera
        # pobierz gwiazdy 3 pozycje
        column = details_html.findAll(class_="credit_summary_item")
        director = (str(column).split(">")[4])[:-3]
        stars = (str(column).split("Stars:")[1].split(">")[2]).replace("</a", ""), \
                  (str(column).split("Stars:")[1].split(">")[4]).replace("</a", ""), \
                  (str(column).split("Stars:")[1].split(">")[6]).replace("</a", "")
        return director, stars
    def saveMoviesToFile(self):
        file = open("movies_list.txt",'w')
        file.write('| %100s | %5s | %50s | %100s | %5s | %50s |\n' %
                   ('TITILE','YEAR', 'DIRECTOR', 'STARS', 'RATE', 'REFLINK'))   # zapis nagłówka
        for movie in self.movies:
            file.write(str(movie) + '\n')                                       # zapis wszystkich filmów
        file.close()

imdb = ImdbScrapper()
imdb.getTop250()
imdb.scrappingTop250()
imdb.saveMoviesToFile()