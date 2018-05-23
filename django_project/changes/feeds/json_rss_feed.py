# coding=utf-8
import json
from django.utils.feedgenerator import SyndicationFeed, rfc2822_date


class JSONFeed(SyndicationFeed):
    mime_type = 'application/json; charset=utf-8'

    def write(self, outfile, encoding):
        data = {}
        data['rss'] = {'version': '2.0'}
        data['rss']['channel'] = self.add_root_elements()

        if self.items:
            item_element = []

            for item in self.items:
                item_element += [self.add_item_elements(item), ]

            data['rss']['channel']['item'] = item_element

        outfile.write(json.dumps(data, encoding=encoding))

    def add_item_elements(self, item):
        item_elements = {}

        item_elements['title'] = item['title']
        item_elements['link'] = item['link']
        if item['description'] is not None:
            item_elements['description'] = item['description']

        if item['pubdate'] is not None:
            item_elements['pubDate'] = rfc2822_date(item['pubdate'])
        if item['unique_id'] is not None:
            guid_attrs = {}
            if isinstance(item.get('unique_id_is_permalink'), bool):
                guid_attrs['isPermaLink'] = str(
                    item['unique_id_is_permalink']).lower()
            item_elements['guid'] = item['unique_id']

        # Add image url attributes for sponsor
        if item['image_url'] is not None:
            domain_url = self.feed['link']
            head, sep, tail = domain_url.partition('/en/')
            item_elements['image_url'] = head + item['image_url']

        return item_elements

    def add_root_elements(self):
        root_elements = {}

        root_elements['title'] = self.feed['title']
        root_elements['link'] = self.feed['link']
        root_elements['description'] = self.feed['description']
        root_elements['lastBuildDate'] = rfc2822_date(self.latest_post_date())

        return root_elements
