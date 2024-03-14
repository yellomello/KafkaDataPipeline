from datetime import datetime, timedelta
from newsapi.newsapi_client import NewsApiClient

def dataSourceMovieByDay():
    # Initialize API endpoint
    newsapi = NewsApiClient(api_key="1bf9612ea0a14b87854320b0e0bb4425")

    # Define the list of media sources
    desiredMediaSources = {'bbc-news', 'cnn', 'fox-news', 'nbc-news', 'the-guardian-uk', 'the-new-york-times', 'the-washington-post', 'usa-today', 'independent', 'daily-mail'}
    
    producerData = []

    # Calculate the start and end dates
    today = datetime.today()
    startDate = (today - timedelta(days=29))
    endDate = (today)

    # Loop over each day in the date range
    currentDate = startDate
    while currentDate <= endDate:
        # Get articles for the current page
        allArticles = newsapi.get_everything(q='Dune: Part Two',
                                            from_param=currentDate.strftime('%Y-%m-%d'),
                                            to=currentDate.strftime('%Y-%m-%d'),
                                            page=1,
                                            language='en',
                                            sources=', '.join(desiredMediaSources)),

        # Check if 'articles' is empty, if yes, break out of the loop
        if not allArticles[0]['articles']:
            break

        # Process the articles
        for article in allArticles[0]['articles']:
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

        # Move to the next day
        currentDate += timedelta(days=1)

    # Print producer data
    print("Producer data:", producerData)

    return producerData

if __name__ == "__main__":
    dataSourceMovieByDay()