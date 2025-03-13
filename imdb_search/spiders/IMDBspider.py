import scrapy
from pathlib import Path
from imdb_search.movie import Movie

class IMDBSpider(scrapy.Spider):
    name = 'imdb-spider'
    start_urls = ['http://web.archive.org/web/20231021155922/https://www.imdb.com/chart/top/']

    def parse(self, response):
        ITEM_SELECTOR = '.ipc-metadata-list-summary-item__c'
        TITLE_SELECTOR = '.ipc-title__text::text'
        YEAR_TIME_AGE_SELECTOR = '.cli-title-metadata-item::text'
        RATING_SELECTOR = '.ratingGroup--imdb-rating::text'
        URL_SELECTOR = '.ipc-title a::attr("href")'

        for item in response.css(ITEM_SELECTOR):
            title = item.css(TITLE_SELECTOR).get()
            year_time_age = item.css(YEAR_TIME_AGE_SELECTOR).getall()
            if len(year_time_age) == 2:  # case when there's no rating
                year_time_age = [year_time_age[0], 'None', year_time_age[1]]#year_time_age.append(None)
            rating = item.css(RATING_SELECTOR).get()
            next_page = item.css(URL_SELECTOR).extract_first()
            if next_page:
                yield response.follow('https' + next_page.split('https')[-1], callback=self.parse_page2,
                    cb_kwargs={'title': title, 'year_time_age': year_time_age, 'rating': rating})


    def parse_page2(self, response, title, year_time_age, rating):

        DIR_WR_ITEM_SELECTOR = '.ipc-metadata-list__item'
        DIRECTOR_WRITER_SELECTOR = 'a.ipc-metadata-list-item__list-content-item.ipc-metadata-list-item__list-content-item--link::text'
        ACTOR_SELECTOR = 'a.sc-cd7dc4b7-1.kVdWAO::text'
        ACTOR_REF_SELECTOR = 'a.sc-cd7dc4b7-1.kVdWAO ::attr("href")'
        POSTER_SELECTOR = 'a.ipc-lockup-overlay.ipc-focusable ::attr("href")'

        items = response.css(DIR_WR_ITEM_SELECTOR)
        directors = items[0].css(DIRECTOR_WRITER_SELECTOR).getall()
        writers = items[1].css(DIRECTOR_WRITER_SELECTOR).getall()
        actors = response.css(ACTOR_SELECTOR).getall()
        actors_ref = response.css(ACTOR_REF_SELECTOR).getall()
        poster = response.css(POSTER_SELECTOR).extract_first()
        plot = ""
        m = Movie(title, response.url, year_time_age[0], year_time_age[2], year_time_age[1], rating, poster, plot, directors, writers, actors, actors_ref)
        plot_link = ''.join([c + '/' for c in response.url.split('/')[0:-1]]) + 'plotsummary'
        yield response.follow(plot_link, callback=self.parse_plot,
                              cb_kwargs={'m': m})


    def parse_plot(self, response, m):
        PLOT_SELECTOR = '.ipc-html-content-inner-div::text'
        m.set_plot(response.css(PLOT_SELECTOR).extract_first())
        filename = f"imdb_movies.jsonl"
        m.serialize(filename, Path)