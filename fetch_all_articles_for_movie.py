from newsapi.newsapi_client import NewsApiClient

def fetchAllArticlesForMovie(movie):
    # Initialize API endpoint
    newsapi = NewsApiClient(api_key="2a547d86a67340e4982cfd16d17a1837")

    # Define the list of media sources
    desiredMediaSources = {'bbc-news', 'cnn', 'fox-news', 'nbc-news', 'the-guardian-uk', 'the-new-york-times', 'the-washington-post', 'usa-today', 'independent', 'daily-mail'}

    producerData = []

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
            'url': article['url'],
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
    fetchAllArticlesForMovie()
