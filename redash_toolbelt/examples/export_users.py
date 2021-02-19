import click
import requests
import json


def get_users(url, api_key):
    dashboards = []
    headers = {'Authorization': 'Key {}'.format(api_key)}
    path = "{}/api/users".format(url)
    has_more = True
    page = 1
    while has_more:
        response = requests.get(path, headers=headers,
                                params={'page': page}).json()
        dashboards.extend(response['results'])
        has_more = page * response['page_size'] + 1 <= response['count']
        page += 1
    return dashboards


def get_user(url, api_key, id, toFile=False):
    headers = {'Authorization': 'Key {}'.format(api_key)}
    path = "{}/api/users/{}".format(url, id)
    user = requests.get(path, headers=headers).json()
    if toFile:
        filename = 'user_{}.json'.format(user['id'])
        with open(filename, 'w') as f:
            f.write(json.dumps(user))
        print("exported: {file}, called: {email}".format(
            file=filename, email=user['email']))
    else:
        print(json.dumps(user, indent=2))


def save_users(users, url, api_key, toFile):
    for u in users:
        get_user(url, api_key, u['id'], toFile)


def list_users(users):
    for u in users:
        print("id: {id}, email: {email}, name: {name}".format(
            id=u['id'], email=u['email'], name=u['name']))


@click.command()
@click.option('--redash-url', required=True)
@click.option('--api-key', required=True, help="API Key")
@click.option('--all', is_flag=True, help="Export all dashboard")
@click.option('--ls', is_flag=True, help="List all dashboards")
@click.option('--id', help="Export dashboard with given slug")
@click.option('--to-file', is_flag=True, help="write dashboard to file instead of stdout")
def main(redash_url, api_key, all, ls, id, to_file):
    users = get_users(redash_url, api_key)
    if ls:
        list_users(users)
    if all:
        save_users(users, redash_url, api_key, to_file)
    if id:
        get_user(redash_url, api_key, id, to_file)


if __name__ == '__main__':
    main()
