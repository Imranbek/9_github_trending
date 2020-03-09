from datetime import datetime, timedelta

import requests


def main():
    time_delta = timedelta(weeks=1)
    current_date = datetime.now()
    str_date_from = (current_date - time_delta).strftime("%Y-%m-%d")

    repositories = get_github_repositories_created_after_date_order_by_stars(
        str_date_from=str_date_from)

    repositories = repositories[:20]
    for repository in repositories:
        owner_login = repository['owner']['login']
        repo_name = repository['name']
        repo_url = repository['url']
        repo_issues = get_issues(
            repo_owner=owner_login,
            repo_name=repo_name)
        open_issues_amount = get_open_issues_amount(issues=repo_issues)

        print_repo_information_with_issues_amount(
            repo_name=repo_name,
            repo_url=repo_url,
            open_issues_amount=open_issues_amount)


def print_repo_information_with_issues_amount(repo_name: str,
                                              repo_url: str,
                                              open_issues_amount: int):
    print('Repository name: {}\n'
          'Repository url: {}\n'
          'Open issues: {}'.format(repo_name,
                                   repo_url,
                                   str(open_issues_amount)))

    print('--------------------')


def get_open_issues_amount(issues: list):
    open_issues = [issue for issue in issues if issue['state'] == 'open']
    open_issues_amount = len(open_issues)
    return open_issues_amount


def get_issues(repo_owner: str, repo_name):
    url = 'https://api.github.com/repos/{}/{}/issues'.format(repo_owner, repo_name)

    headers = {'Accept': 'application/vnd.github.machine-man-preview'}
    response = requests.get(url=url,
                            headers=headers)
    issues = response.json()
    return issues


def get_github_repositories_created_after_date_order_by_stars(str_date_from: str):
    url = 'https://api.github.com/search/repositories'
    params = {'q': 'created:>{}'.format(str_date_from),
              'sort': 'stargazers',
              'order': 'asc'}

    headers = {'Accept': 'application/vnd.github.mercy-preview+json'}
    response = requests.get(url=url,
                            params=params,
                            headers=headers)
    repositories = response.json()['items']
    return repositories


if __name__ == '__main__':
    main()
