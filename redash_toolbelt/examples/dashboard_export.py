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
        response = requests.get(path, headers=headers, params={'page': page}).json()
        dashboards.extend(response['results'])
        has_more = page * response['page_size'] + 1 <= response['count']
        page += 1

    return dashboards


def get_dashboard(url, api_key, slug):
    headers = {'Authorization': 'Key {}'.format(api_key)}
    path = "{}/api/dashboards/{}".format(url, slug)
    response = requests.get(path, headers=headers).json()
    #print(response)
    return response


def save_dashboards(dashboards, url, api_key):
    for db in dashboards:
        board = get_dashboard(url, api_key, db['slug'])
        filename = 'db_{}.json'.format(db['id'])
        with open(filename, 'w') as f:
            f.write(json.dumps(board))
        print("exported: {file}, called: {name}".format(file=filename, name=db['name']))


@click.command()
@click.option('--redash-url')
@click.option('--api-key', required=True, help="API Key")
@click.option('--all', is_flag=True, help="Export all dashboard")
@click.option('--id', help="Export specific ID")
def main(redash_url, api_key):
    dashboards = get_dashboards(redash_url, api_key)      
    save_dashboards(dashboards, redash_url, api_key)
    #print(dashboards)


if __name__ == '__main__':
    main()