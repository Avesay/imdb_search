## IMDB Search engine
This is a project created for a course at University of Nicosia. Its main goal is to create an Information Retrieval System for top 250 movies on IMDB. In order to keep data consistent, a web archive website is used.
### To run web crawler:

  1. Open terminal and change current directory to *'[location of the folder]\imdb_search\imdb_search'*
  2. Run command *'scrapy crawl imdb-spider'*
    
This should successfully initialize and run the web crawler. After it's done, You should be able to see file called
*'imdb-movies.jsonl'* in the *'imdb_search'* folder.

### To run IR System (search movies):
  1. Open Jupyter Notebook (IMDB_search.ipynb)
  2. In the menu select "run all"
  3. At the end, an input window should open - that's where you can search for movies. After inputting your search query, an output should show you a movie that is the best match to what you enetered.
