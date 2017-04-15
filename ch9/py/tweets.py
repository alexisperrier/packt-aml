import twitter

class ATweets():
    def __init__(self, raw_query):
        self.twitter_api = twitter.Api(consumer_key='fd5TwZfTmZR4J8qMq0THM7sQh',
                      consumer_secret='8aFf6eGf6kKEfrIQjsiQbYyveawSw0rJX7xBiJ3AhcQ098MvjN',
                      access_token_key='14698049-rtGiciCeYlBI3HKI7M0sqfVidFwx2PGBKRVrnkvCh',
                      access_token_secret='Z2qkurxKca4acCbZHgrZCYND33SVaofaaoYe7Pc0QJrO3')
        self.raw_query = raw_query

    def capture(self):
        statuses = self.twitter_api.GetSearch(
            raw_query = self.raw_query,
            lang = 'en',
            count=3, result_type='recent', include_entities=True
        )

        return statuses

