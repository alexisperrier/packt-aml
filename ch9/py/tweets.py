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

# search_query = 'brocolli OR carrot OR artichoke OR lentils OR spinach'
# %20OR%20chickpea%20OR%20quinoa%20OR%20tomato%20OR%20avocado%20OR%20cauliflower
# rq = 'f=tweets&vertical=default&q=brocolli%20OR%20carrot%20OR%20artichoke%20OR%20lentils%20OR%20spinach%20%3A%29%20%3A%28&l=en&src=typd'
# cauliflower
# rq = 'f=tweets&q=brocolli%20OR%20chickpea%20OR%20quinoa%20OR%20tomato%20OR%20avocado%20OR%20cauliflower%20OR%20carrot%20OR%20artichoke%20OR%20lentils%20OR%20spinach&l=en&src=typd'
# twitter_api.GetSearch( raw_query = rq,count=100, result_type='recent', include_entities=True, lang='en')

# https://twitter.com/search?l=en&q=brocolli%20OR%20carrot%20OR%20artichoke%20OR%20lentils%20OR%20spinach%20%3A)%20%3A(&src=typd
# https://twitter.com/search?f=tweets&vertical=default&q=brocolli%20OR%20carrot%20OR%20artichoke%20OR%20lentils%20OR%20spinach%20%3A%29%20%3A%28&l=en&src=typd


# for status in statuses:
#     if process_status(status, output_file_handle):
#         count = count + 1


# # fetch_tweets(parsed_handle)


# def process_status(status, output_file_handle):
#     global sleep_before_get_status
#     global sleep_before_get_user
#     if status.retweeted_status is not None:
#         return False
#     record = {}
#     record.update(status_to_map('', status))
#     record.update(user_to_map('', status.user))
#     if record['in_reply_to_status_id'] is not None:
#         if sleep_before_get_status:
#             sleep_then_update_flags()
#         try:
#             r2status = twitter_api.GetStatus(record['in_reply_to_status_id'])
#             sleep_before_get_status = True
#             record.update(status_to_map('r.', r2status))
#             record.update(user_to_map('r.', r2status.user))
#         except TwitterError as e:
#             print(e)
#             print('statusId:' + str(record['in_reply_to_status_id']))
#     elif record['in_reply_to_user_id'] is not None:
#         if sleep_before_get_user:
#             sleep_then_update_flags()
#         try:
#             r2user = twitter_api.GetUser(int(record['in_reply_to_user_id']))
#             sleep_before_get_user = True
#             record.update(user_to_map('r.', r2user))
#         except TwitterError as e:
#             print(e)
#             print('statusId:' + str(record['in_reply_to_user_id']))
#     output_file_handle.write(json.dumps(record))
#     output_file_handle.write('\n')
#     return True

# def fetch_tweets(twitter_handle):
#     with codecs.open(output_file_name, 'w', 'utf-8') as output_file_handle:
#         global sleep_before_get_search
#         max_id = -1
#         count = 0

#         while count < max_tweets:
#             if sleep_before_get_search:
#                 sleep_then_update_flags()
#             if max_id == -1:
#                 statuses = twitter_api.GetSearch(
#                     term=search_query, count=100, result_type='recent')
#             else:
#                 statuses = twitter_api.GetSearch(
#                     term=search_query, count=100, result_type='recent', max_id=max_id - 1)
#             sleep_before_get_search = True
#             if len(statuses) == 0:
#                 print("No more search results found.")
#                 break
#             for status in statuses:
#                 # print a '.' for each tweet that is downloaded
#                 sys.stdout.write(".")
#                 sys.stdout.flush()
#                 if max_id == -1:
#                     max_id = status.id
#                 else:
#                     max_id = min(max_id, status.id)
#                 if process_status(status, output_file_handle):
#                     count = count + 1
#         print("{0} tweets downloaded.".format(count))
#         print("See file {0} for tweets".format(output_file_name))



# if __name__ == "__main__":
#     try:
#         twitter_handle = sys.argv[1]
#         parsed_handle = parse_handle(twitter_handle)
#         if not parsed_handle:
#             raise "{0} is not a legal handle. Please input in format similar to example: @awscloud".format(twitter_handle)
#     except:
#         print(__doc__)
#         raise

