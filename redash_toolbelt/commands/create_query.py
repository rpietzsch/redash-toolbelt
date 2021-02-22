import click
import json
from redash_toolbelt.client import Redash
from redash_toolbelt.utils import copy_value_if_key_exists


@click.command()
@click.option('--redash-url', required=True, help="Redash base URL")
@click.option('--api-key', required=True, help="API Key")
@click.option('--id', help="Change query with given id")
@click.option('--data-source-id', help="The data-source to use the query with")
@click.option('--from-file', help="Use json file to provide details")
@click.option('--tags', 'tags_', help="Blank separated list of tags")
@click.option('--name', 'name_', help="The query name")
@click.option('--query', 'query_', help="The query string")
def main(redash_url, api_key, id, data_source_id, from_file, tags_, name_, query_):
    client = Redash(redash_url, api_key)
    if not client.test_credentials():
        print("invalid url and/or API key")
        exit(1)

    data = {'is_draft': False, 'version': 1}
    file = {}

    if from_file is not None:
        with open(from_file) as f:
            file = json.load(f)

        copy_value_if_key_exists('query', file, data)
        copy_value_if_key_exists('tags', file, data)
        copy_value_if_key_exists('is_draft', file, data)
        copy_value_if_key_exists('name', file, data)
        copy_value_if_key_exists('data_source_id', file, data)

    if query_ is not None:
        data['query'] = query_
    if name_ is not None:
        data['name'] = name_
    if data_source_id is not None:
        data['data_source_id'] = data_source_id
    if tags_ is not None:
        data['tags'] = tags_.split()

    #print("Request: " + json.dumps(data) + "\n")

    # update or create
    qry = {}
    if id is None:
        qry = client.create_query(data)
        id = qry['id']
        qry = json.loads(client.update_query(id, data).text)
        print("Created new query: ", qry['id'])
    else:
        qry = json.loads(client.update_query(id, data).text)
        print("Updated query: ", qry['id'])

    #print("Response: ", qry, "\n")


if __name__ == '__main__':
    main()
