import requests


class Redash(object):
    def __init__(self, redash_url, api_key):
        self.redash_url = redash_url
        self.session = requests.Session()
        self.session.headers.update(
            {'Authorization': 'Key {}'.format(api_key)})

    def test_credentials(self):
        try:
            response = self._get('api/session')
            return True
        except requests.exceptions.HTTPError:
            return False

    def group(self, id):
        """GET api/groups/{id}
        return detailed representation of a group"""
        return self._get('api/groups/{}'.format(id)).json()

    def groups(self):
        """GET api/groups
        return array of all groups (no details, use group(id) to get those)"""
        return self._get('api/groups').json()

    def queries(self):
        """return array of all queries (no details, use query(id) to get those)"""
        return self._paginate(self.queries_page)

    def queries_page(self, page=1, page_size=25):
        """GET api/queries
        returns page N of given page_size of queries (no details, use query(id) to get those)"""
        return self._get('api/queries', params=dict(page=page, page_size=page_size)).json()

    def query(self, id):
        """GET api/queries/{id}
        return detailed representation of a query"""
        return self._get('api/queries/{}'.format(id)).json()

    def data_sources(self):
        """GET api/data_sources
        returns array of all data_sources (no details, use data_soruce(id) to get those)"""
        return self._get('api/data_sources').json()

    def data_source(self, id):
        """GET api/data_sources/{id}
        return detailed representation of a data_source"""
        return self._get('api/data_sources/{}'.format(id)).json()

    def users(self):
        """return array of all users (no details, use user(id) to get those)"""
        return self._paginate(self.users_page)

    def users_page(self, page=1, page_size=25):
        """GET api/users
        returns page N of given page_size of users (no details, use user(id) to get those)"""
        return self._get('api/users', params=dict(page=page, page_size=page_size)).json()

    def user(self, id):
        """GET api/users/{id}
        return detailed representation of a user"""
        return self._get('api/users/{}'.format(id)).json()

    def dashboards(self):
        """return array of all dashboards (no details, use dashboard(slug) to get those)"""
        return self._paginate(self.dashboards_page)

    def dashboards_page(self, page=1, page_size=25):
        """GET api/dashboards
        returns page N of given page_size of dashboards (no details, use dashboard(slug) to get those)"""
        return self._get('api/dashboards', params=dict(page=page, page_size=page_size)).json()

    def dashboard(self, slug):
        """GET api/dashboards/{slug}
        return detailed representation of a dashboard"""
        return self._get('api/dashboards/{}'.format(slug)).json()

    def create_dashboard(self, name):
        """POST api/dashboards create a new empty dashboard with given name.
        Returns ID of the new dashboard"""
        return self._post('api/dashboards', json={'name': name}).json()

    def update_dashboard(self, dashboard_id, properties):
        """POST api/dashboards/{id} update the given dashboard (id) 
        providing the properties to set/change"""
        return self._post('api/dashboards/{}'.format(dashboard_id), json=properties).json()

    def create_widget(self, dashboard_id, visualization_id, text, options):
        """POST api/widgets create a new widget (visualization_id) on given dashboard (dashboard_id)"""
        data = {
            'dashboard_id': dashboard_id,
            'visualization_id': visualization_id,
            'text': text,
            'options': options,
            'width': 1,
        }
        return self._post('api/widgets', json=data)

    def duplicate_dashboard(self, slug, new_name=None):
        """duplicates the given dashboard (slug) set the new_name 
        (default to 'Copy of <name of dashboard to duplicate>'). 
        Copies all tags and all widgets.
        Returns the ID of the duplicate dashboard."""
        current_dashboard = self.dashboard(slug)

        if new_name is None:
            new_name = u'Copy of: {}'.format(current_dashboard['name'])

        new_dashboard = self.create_dashboard(new_name)
        if current_dashboard['tags']:
            self.update_dashboard(new_dashboard['id'], {
                                  'tags': current_dashboard['tags']})

        for widget in current_dashboard['widgets']:
            visualization_id = None
            if 'visualization' in widget:
                visualization_id = widget['visualization']['id']
            self.create_widget(
                new_dashboard['id'], visualization_id, widget['text'], widget['options'])

        return new_dashboard

    def scheduled_queries(self):
        """Loads all queries and returns only the scheduled ones."""
        queries = self._paginate(self.queries_page)
        return filter(lambda query: query['schedule'] is not None, queries)

    def update_query(self, query_id, data):
        """POST /api/queries/{query_id} with the provided data object."""
        path = 'api/queries/{}'.format(query_id)
        return self._post(path, json=data)

    @staticmethod
    def _paginate(resource):
        """Load all items of a paginated resource"""
        stop_loading = False
        page = 1
        page_size = 100

        items = []

        while not stop_loading:
            response = resource(page=page, page_size=page_size)
            items += response['results']
            page += 1
            stop_loading = response['page'] * \
                response['page_size'] >= response['count']

        return items

    def _get(self, path, **kwargs):
        return self._request('GET', path, **kwargs)

    def _post(self, path, **kwargs):
        return self._request('POST', path, **kwargs)

    def _request(self, method, path, **kwargs):
        url = '{}/{}'.format(self.redash_url, path)
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response
