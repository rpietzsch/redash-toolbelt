import click
import json
from redash_toolbelt.client import Redash
from redash_toolbelt.utils import save_dict_as_json_file


def get_dashboard(client, slug, toFile=False):
    dashboard = client.dashboard(slug)
    if toFile:
        filename = 'db_{}.json'.format(dashboard['id'])
        msg = "exported: {file}, called: {name}".format(file=filename, name=dashboard['name'])
        save_dict_as_json_file(dashboard, filename, msg)
    else:
        print(json.dumps(dashboard, indent=2))


def get_dashboards(dashboards, client, toFile):
    for db in dashboards:
        get_dashboard(client, db['slug'], toFile)


def list_dashboards(dashboards):
    for db in dashboards:
        print("id: {id}, slug: {slug}, name: {name}".format(
            id=db['id'], slug=db['slug'], name=db['name']))


@click.command()
@click.option('--redash-url', required=True)
@click.option('--api-key', required=True, help="API Key")
@click.option('--all', is_flag=True, help="Export all dashboard")
@click.option('--ls', is_flag=True, help="List all dashboards")
@click.option('--slug', help="Export dashboard with given slug")
@click.option('--to-file', is_flag=True, help="write dashboard to file instead of stdout")
def main(redash_url, api_key, all, ls, slug, to_file):
    client = Redash(redash_url, api_key)
    if not client.test_credentials():
        print("invalid url and/or API key")
        exit(1)

    dashboards = client.dashboards()

    if ls:
        list_dashboards(dashboards)
    elif all:
        get_dashboards(dashboards, client, to_file)
    elif slug:
        get_dashboard(client, slug, to_file)


if __name__ == '__main__':
    main()
