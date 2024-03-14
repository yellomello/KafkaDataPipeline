from newsapi.newsapi_client import NewsApiClient

listMovies = ['Deadpool & Wolverine', 'Dune: Part Two', 'The Matrix Resurrections', 'Kung Fu Panda 4']

def dataSourceMovieByList():
    # Initialize API endpoint
    newsapi = NewsApiClient(api_key="1bf9612ea0a14b87854320b0e0bb4425")

    # Define the list of media sources
    desiredMediaSources = {'bbc-news', 'cnn', 'fox-news', 'nbc-news', 'the-guardian-uk', 'the-new-york-times', 'the-washington-post', 'usa-today', 'independent', 'daily-mail'}

    producerData = []

    for movie in listMovies:
        # Get articles for the current movie
        allArticles = newsapi.get_everything(q=movie,
                                            language='en',
                                            sources=', '.join(desiredMediaSources))

        # Process the articles
        for article in allArticles['articles']:
            formattedData = {
                'source': article['source']['id'],
                'author': article['author'],
                'title': article['title'],
                'description': article['description'],
                'url': article['url'],
                'urlToImage': article['urlToImage'],
                'publishedAt': article['publishedAt'],
                'content': article['content']
            }

            # Filter out objects where content is '[Removed]'
            if article['content'] == '[Removed]':
                continue

            producerData.append(formattedData)

    # Print producer data
    print("Producer data:", producerData)

    return producerData

if __name__ == "__main__":
    dataSourceMovieByList()
