import click
import requests
import json


def get_dashboards(url, api_key):
    dashboards = []
    headers = {'Authorization': 'Key {}'.format(api_key)}
    path = "{}/api/dashboards".format(url)
    has_more = True
    page = 1
    while has_more:
        response = requests.get(path, headers=headers,
                                params={'page': page}).json()
        dashboards.extend(response['results'])
        has_more = page * response['page_size'] + 1 <= response['count']
        page += 1
    return dashboards


def get_dashboard(url, api_key, slug, toFile=False):
    headers = {'Authorization': 'Key {}'.format(api_key)}
    path = "{}/api/dashboards/{}".format(url, slug)
    dashboard = requests.get(path, headers=headers).json()
    if toFile:
        filename = 'db_{}.json'.format(dashboard['id'])
        with open(filename, 'w') as f:
            f.write(json.dumps(dashboard))
        print("exported: {file}, called: {name}".format(
            file=filename, name=dashboard['name']))
    else:
        print(json.dumps(dashboard, indent=2))


def save_dashboards(dashboards, url, api_key, toFile):
    for db in dashboards:
        get_dashboard(url, api_key, db['slug'], toFile)


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
    dashboards = get_dashboards(redash_url, api_key)
    if ls:
        list_dashboards(dashboards)
    if all:
        save_dashboards(dashboards, redash_url, api_key, to_file)
    if slug:
        get_dashboard(redash_url, api_key, slug, to_file)


if __name__ == '__main__':
    main()
