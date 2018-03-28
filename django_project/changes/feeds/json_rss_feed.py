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

        if item['author_name'] and item['author_email']:
            item_elements['author'] = "%s (%s)" % (
            item['author_name'], item['author_email'])
        elif item['author_email']:
            item_elements['author'] = item['author_email']
        elif item['author_name']:
            item_elements['author'] = item['author_name']

        if item['pubdate'] is not None:
            item_elements['pubDate'] = rfc2822_date(item['pubdate'])
        if item['comments'] is not None:
            item_elements['comments'] = item['comments']
        if item['unique_id'] is not None:
            guid_attrs = {}
            if isinstance(item.get('unique_id_is_permalink'), bool):
                guid_attrs['isPermaLink'] = str(
                    item['unique_id_is_permalink']).lower()
            item_elements['guid'] = item['unique_id']

        if item['enclosure'] is not None:
            item_elements['enclosure'] = {
                'href': item['enclosure'].url,
                'lenght': item['enclosure'].length,
                'type': item['enclosure'].mime_type,
            }

        if item['categories']:
            item_elements['categories'] = []
        for cat in item['categories']:
            item_elements['categories'] += [{"term": cat}, ]

        if item['item_copyright'] is not None:
            item_elements['rights'] = item['item_copyright']

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

        if self.feed['feed_url'] is not None:
            root_elements['feed_url'] = self.feed['feed_url']
        if self.feed['language'] is not None:
            root_elements['language'] = self.feed['language']
        if self.feed['categories']:
            root_elements['categories'] = []
        for cat in self.feed['categories']:
            root_elements['categories'] += [cat, ]
        if self.feed['feed_copyright'] is not None:
            root_elements['copyright'] = self.feed['feed_copyright']
        root_elements['lastBuildDate'] = rfc2822_date(self.latest_post_date())
        if self.feed['ttl'] is not None:
            root_elements['ttl'] = self.feed['ttl']

        return root_elements