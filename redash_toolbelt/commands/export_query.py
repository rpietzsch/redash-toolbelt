import click
from redash_toolbelt.client import Redash
from redash_toolbelt.utils import save_dict_as_json_file

template = u"""/*
Name: {name}
Data source: {data_source}
Created By: {created_by}
Last Update At: {last_updated_at}
*/
{query}"""


def get_query(client, id, toFile=False):
    query = client.query(id)
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


def get_queries(queries, client, toFile):
    for q in queries:
        get_query(client, q['id'], toFile)


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
    client = Redash(redash_url, api_key)
    if not client.test_credentials():
        print("invalid url and/or API key")
        exit(1)

    queries = client.queries()
    
    if ls:
        list_queries(queries)
    if all:
        get_queries(queries, client, to_file)
    if id:
        get_query(client, id, to_file)


if __name__ == '__main__':
    main()