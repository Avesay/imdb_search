import json


class Movie:
    def __init__(self, title, url, year, age, duration, rating, poster, plot, directors, writers, actors, actors_ref):
        self.url = url
        self.imdb_id = url.split('/')[-2]
        self.title = title
        self.year = year
        self.duration = duration
        self.rating = age
        self.imdb_rating = rating
        try:
            self.poster = poster.split('www.imdb.com')[-1]
        except IndexError:
            self.poster = ""
        self.plot = plot
        self.directors = directors
        self.writers = writers
        self.actors = []
        for i in range(len(actors)):
            self.actors.append({'name': actors[i], 'href': actors_ref[i].split('www.imdb.com')[-1]})

    def serialize(self, filename, path):
        with path(filename).open('a', encoding='utf-8') as f:
            json.dump(self.__dict__, f, ensure_ascii=False)
            f.write("\n")

    def set_plot(self, plot):
        self.plot = plot