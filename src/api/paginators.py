#coding:utf-8


class DummyPaginator(object):
    def __init__(self, request_data, objects, resource_uri=None,
                 limit=None, offset=0, max_limit=1000,
                 collection_name='objects'):
        self.objects = objects
        self.collection_name = collection_name

    def page(self):
        return { self.collection_name: self.objects, }
