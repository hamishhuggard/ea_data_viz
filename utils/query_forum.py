import requests

# Queries can be tested at https://forum.effectivealtruism.org/graphiql

forum_query = '''
{
  posts
  {
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

def get_forum_data():
    graphql_url = 'https://forum.effectivealtruism.org/graphql?'
    response = requests.post(graphql_url, json={'query': forum_query})
    response_json = response.json()
    return response_json
