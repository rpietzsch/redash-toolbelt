import click
import requests
import json


def get_data_sources(url, api_key):
    headers = {'Authorization': 'Key {}'.format(api_key)}
    path = "{}/api/data_sources".format(url)
    response = requests.get(path, headers=headers).json()
    return response


def get_data_source(url, api_key, id, toFile=False):
    headers = {'Authorization': 'Key {}'.format(api_key)}
    path = "{}/api/data_sources/{}".format(url, id)
    data_source = requests.get(path, headers=headers).json()
    if toFile:
        filename = 'data_source_{}.json'.format(data_source['id'])
        with open(filename, 'w') as f:
            f.write(json.dumps(data_source))
        print("exported: {file}, called: {name}".format(
            file=filename, name=data_source['name']))
    else:
        print(json.dumps(data_source, indent=2))


def save_data_sources(data_sources, url, api_key, toFile):
    for ds in data_sources:
        get_data_source(url, api_key, ds['id'], toFile)


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
    data_sources = get_data_sources(redash_url, api_key)
    if ls:
        list_data_sources(data_sources)
    if all:
        save_data_sources(data_sources, redash_url, api_key, to_file)
    if id:
        get_data_source(redash_url, api_key, id, to_file)


if __name__ == '__main__':
    main()
