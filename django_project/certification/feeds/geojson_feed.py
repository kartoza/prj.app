# coding=utf-8
import json
from django.utils.feedgenerator import SyndicationFeed, rfc2822_date


class GeoJSONFeed(SyndicationFeed):
    """GeoJSON feed for training centers."""

    content_type = 'application/json; charset=utf-8'

    def write(self, outfile, encoding):
        data = {
            'rss': {
                'version': '2.0',
                'channel': self.add_root_elements()
            }
        }

        if self.items:
            item_element = []
            for item in self.items:
                item_element += [self.add_item_elements(item), ]
            data['rss']['channel']['item'] = item_element
        outfile.write(json.dumps(data))

    def add_item_elements(self, item):
        item_elements = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [
                    round(item['location'].x, 2),
                    round(item['location'].y, 2)
                ],
            },
            'properties': {
                'name': item['name'],
                'certifying_organisation': item['certifying_organisation'].name
            }
        }
        return item_elements

    def add_root_elements(self):
        root_elements = {
            'title': self.feed['title'],
            'description': self.feed['description'],
            'link': self.feed['link'],
            'homepage': self.feed['homepage'],
            'lastBuildDate': rfc2822_date(self.latest_post_date())
        }
        return root_elements
