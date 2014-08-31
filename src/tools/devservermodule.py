from devserver.modules import DevServerModule

from django.db import connections


class SQLPtitsynModule(DevServerModule):
    """
    Outputs a summary SQL queries.
    """

    logger_name = 'sql'

    def process_complete(self, request):
        queries = [
            q for alias in connections
            for q in connections[alias].queries
        ]
        for query in queries:
            self.logger.info('time: {},\nsql: {}'.format(query['time'], query['sql']))
        num_queries = len(queries)
        if num_queries:
            unique = set([s['sql'] for s in queries])
            self.logger.info('%(calls)s queries with %(dupes)s duplicates' % dict(
                calls=num_queries,
                dupes=num_queries - len(unique),
            ), duration=sum(float(c.get('time', 0)) for c in queries) * 1000)
