import click
import json
from redash_toolbelt.client import Redash
from redash_toolbelt.utils import save_dict_as_json_file


def get_group(client, id, toFile=False):
    group = client.group(id)
    if toFile:
        filename = 'group_{}.json'.format(group['id'])
        msg = "exported: {file}, called: {name}".format(file=filename, name=group['name'])
        save_dict_as_json_file(group, filename, msg)
    else:
        print(json.dumps(group, indent=2))


def get_groups(groups, client, toFile):
    for group in groups:
        get_group(client, group['id'], toFile)


def list_groups(groups):
    for group in groups:
        print("id: {id}, name: {name}".format(
            id=group['id'], name=group['name']))


@click.command()
@click.option('--redash-url', required=True)
@click.option('--api-key', required=True, help="API Key")
@click.option('--all', is_flag=True, help="Export all groups")
@click.option('--ls', is_flag=True, help="List all groups")
@click.option('--id', help="Export group with given id")
@click.option('--to-file', is_flag=True, help="write group(s) to file instead of stdout")
def main(redash_url, api_key, all, ls, id, to_file):
    client = Redash(redash_url, api_key)
    if not client.test_credentials():
        print("invalid url and/or API key")
        exit(1)

    groups = client.groups()
    
    if ls:
        list_groups(groups)
    if all:
        get_groups(groups, client, to_file)
    if id:
        get_group(client, id, to_file)


if __name__ == '__main__':
    main()
