import click
import json
from redash_toolbelt.client import Redash
from redash_toolbelt.utils import save_dict_as_json_file


def get_user(client, id, toFile=False):
    user = client.user(id)
    if toFile:
        filename = 'user_{}.json'.format(user['id'])
        msg = "exported: {file}, called: {email}".format(file=filename, email=user['email'])
        save_dict_as_json_file(user, filename, msg)
    else:
        print(json.dumps(user, indent=2))


def get_users(users, client, toFile):
    for u in users:
        get_user(client, u['id'], toFile)


def list_users(users):
    for u in users:
        print("id: {id}, email: {email}, name: {name}".format(
            id=u['id'], email=u['email'], name=u['name']))


@click.command()
@click.option('--redash-url', required=True)
@click.option('--api-key', required=True, help="API Key")
@click.option('--all', is_flag=True, help="Export all user")
@click.option('--ls', is_flag=True, help="List all user")
@click.option('--id', help="Export user with given id")
@click.option('--to-file', is_flag=True, help="write user(s) to file instead of stdout")
def main(redash_url, api_key, all, ls, id, to_file):
    client = Redash(redash_url, api_key)
    if not client.test_credentials():
        print("invalid url and/or API key")
        exit(1)

    users = client.users()
    
    if ls:
        list_users(users)
    if all:
        get_users(users, client, to_file)
    if id:
        get_user(client, id, to_file)


if __name__ == '__main__':
    main()
