import requests
from datetime import datetime, timedelta


API_URL = 'https://api.github.com/search/repositories'
API_ISSUES_URL = 'https://api.github.com/repos/{}/{}/issues'


def get_trending_repositories():
    week_ago = datetime.now() - timedelta(weeks=1)
    parameters = \
        {'q': 'created:>={}'.format(week_ago.date()),
         'sort': 'stars', 'order': 'desc'}
    get_info_from_github = requests.get(API_URL,
                     parameters)
    json_repositories = get_info_from_github.json()
    top_20_repositories =  json_repositories['items'][:20]
    repositories = []
    for repo in top_20_repositories:
        repositories.append({'owner': repo['owner']['login'],
                      'name': repo['name'],
                      'stars': repo['stargazers_count'],
                      'list_of_issues': []
                      })
    return repositories
        

def get_open_issues_amount(repositories):
    for repos in repositories:
        get_info_from_github = requests.get(API_ISSUES_URL.format(repos['owner'],repos['name']),
                         {'state' : 'open'})
        issues = get_info_from_github.json()
        for issue in issues:
            issue_url = str(issue['html_url'])
            if 'issues' in issue_url:
                repos['list_of_issues'].append(issue_url)
    return repositories


def print_top_20_repositories(repositories):
    for repo in repositories:    
        print('Name: {}\n'
              'Stars = {}\n'
              'url: https://github.com/{}/{}\n'
              .format(repo['name'],
                      repo['stars'],
                      repo['owner'],
                      repo['name']))
        print('Amount of issues: {}\n'.format(
            len(repo['list_of_issues'])))
        if len(repo['list_of_issues']) > 0:
            print('issues urls are:')
            for issue in repo['list_of_issues']:
                print(issue)
        print()
    

if __name__ == '__main__':
    top_20_repo = get_trending_repositories()
    top_20_repo_with_issues = get_open_issues_amount(top_20_repo)
    print_top_20_repositories(top_20_repo_with_issues)
    
