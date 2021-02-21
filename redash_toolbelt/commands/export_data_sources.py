import click
import json
from redash_toolbelt.client import Redash
from redash_toolbelt.utils import save_dict_as_json_file


def get_data_source(client, id, toFile=False):
    data_source = client.data_source(id)
    if toFile:
        filename = 'data_source_{}.json'.format(data_source['id'])
        msg = "exported: {file}, called: {name}".format(
            file=filename, name=data_source['name'])
        save_dict_as_json_file(data_source, filename, msg)
    else:
        print(json.dumps(data_source, indent=2))


def get_data_sources(data_sources, client, toFile):
    for ds in data_sources:
        get_data_source(client, ds['id'], toFile)


def list_data_sources(data_sources):
    for ds in data_sources:
        print("id: {id}, name: {name}".format(
            id=ds['id'], name=ds['name']))


@click.command()
@click.option('--redash-url', required=True)
@click.option('--api-key', required=True, help="API Key")
@click.option('--all', is_flag=True, help="Export all data-sources")
@click.option('--ls', is_flag=True, help="List all data-sources")
@click.option('--id', help="Export data-source with given id")
@click.option('--to-file', is_flag=True, help="write data-source(s) to file instead of stdout")
def main(redash_url, api_key, all, ls, id, to_file):
    client = Redash(redash_url, api_key)
    if not client.test_credentials():
        print("invalid url and/or API key")
        exit(1)
    

    data_sources = client.data_sources()
    if ls:
        list_data_sources(data_sources)
    if all:
        get_data_sources(data_sources, client, to_file)
    if id:
        get_data_source(client, id, to_file)


if __name__ == '__main__':
    main()
