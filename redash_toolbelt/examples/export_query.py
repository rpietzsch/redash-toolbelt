import click
import requests

template = u"""/*
Name: {name}
Data source: {data_source}
Created By: {created_by}
Last Update At: {last_updated_at}
*/
{query}"""


def get_queries(url, api_key):
    queries = []
    headers = {'Authorization': 'Key {}'.format(api_key)}
    path = "{}/api/queries".format(url)
    has_more = True
    page = 1
    while has_more:
        response = requests.get(path, headers=headers,
                                params={'page': page}).json()
        queries.extend(response['results'])
        has_more = page * response['page_size'] + 1 <= response['count']
        page += 1
    return queries


def get_query(url, api_key, id, toFile=False):
    headers = {'Authorization': 'Key {}'.format(api_key)}
    path = "{}/api/queries/{}".format(url, id)
    query = requests.get(path, headers=headers).json()
    content = template.format(name=query['name'],
                data_source=query['data_source_id'],
                created_by=query['user']['name'],
                last_updated_at=query['updated_at'],
                query=query['query'])
    if toFile:
        filename = 'query_{}.sql'.format(query['id'])
        with open(filename, 'w') as f:
            f.write(content)
        print("exported: {file}, called: {name}".format(
            file=filename, name=query['name']))
    else:
        print(content)


def save_queries(queries, url, api_key, toFile):
    for q in queries:
        get_query(url, api_key, q['id'], toFile)


def list_queries(queries):
    for q in queries:
        print("id: {id}, name: {name}".format(
            id=q['id'], name=q['name']))


@click.command()
@click.option('--redash-url', required=True)
@click.option('--api-key', required=True, help="API Key")
@click.option('--all', is_flag=True, help="Export all queries")
@click.option('--ls', is_flag=True, help="List all queries")
@click.option('--id', help="Export query with given id")
@click.option('--to-file', is_flag=True, help="write query(s) to file instead of stdout")
def main(redash_url, api_key, all, ls, id, to_file):
    queries = get_queries(redash_url, api_key)
    if ls:
        list_queries(queries)
    if all:
        save_queries(queries, redash_url, api_key, to_file)
    if id:
        get_query(redash_url, api_key, id, to_file)


if __name__ == '__main__':
    main()