# coding=utf-8
import json
from django.utils.feedgenerator import SyndicationFeed, rfc2822_date


class CourseJSONFeed(SyndicationFeed):
    """JSON feed for course."""

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
            'title': item['title'],
            'link': item['link'],
            'start_date': str(item['start_date']),
            'end_date': str(item['end_date']),
            'course_convener': item['course_convener'],
            'course_type': item['course_type'],
            'language': item['language'],
            'certifying_organisation': item['certifying_organisation'].name
        }

        if item['trained_competence']:
            item_elements['trained_competence'] = item['trained_competence']

        if item['training_center']:
            item_elements['training_center'] = {
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [
                        round(item['training_center'].location.x, 2),
                        round(item['training_center'].location.y, 2)
                    ],
                },
                'properties': {
                    'name': item['training_center'].name
                }
            }
        return item_elements

    def add_root_elements(self):
        root_elements = {
            'title': self.feed['title'],
            'description': self.feed['description'],
            'link': self.feed['link'],
            'lastBuildDate': rfc2822_date(self.latest_post_date())
        }
        return root_elements
