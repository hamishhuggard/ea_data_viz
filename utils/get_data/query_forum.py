import requests
import json

# Queries can be tested at https://forum.effectivealtruism.org/graphiql

forum_query = '''
{
  posts (
    input: {
      terms: {
        offset:%d
      }
    }
  ) {
    results {
      title
      postedAt
      user {
        username
        displayName
      }
      coauthors {
        username
        displayName
      }
      pageUrl
      wordCount
      baseScore
      commentCount
    }
  }
}
'''

def get_forum_data(offset=0):
    print(f'Getting forum data from offset={offset}')
    graphql_url = 'https://forum.effectivealtruism.org/graphql?'
    response = requests.post(graphql_url, json={'query': forum_query % offset})
    response_json = response.json()
    return response_json

def refresh_forum_data():

    offset = 0
    forum_data = get_forum_data(offset)

    # the graphql only returns 5000 results at a time
    # so keep increment offset by 5000 until all data collected
    n_results = len(forum_data['data']['posts']['results'])
    while n_results == 5000:
        offset += 5000
        offset_forum_data = get_forum_data(offset)
        n_results = len(offset_forum_data['data']['posts']['results'])

        forum_data['data']['posts']['results'].extend(
            offset_forum_data['data']['posts']['results']
        )

    with open('./data/ea_forum.json', 'w') as f:
        f.write(json.dumps(forum_data))
