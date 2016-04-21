# -*- coding: utf-8 -*-

import re
import requests
import sys

from bs4 import BeautifulSoup


TAG_IMG_PATTERN = r'<img alt="\[(?P<short>[A-Za-z0-9]+)\]" border="([0-9]+)" height="([0-9]+)" src="/images/icons/(?P<long>[a-zA-Z0-9]+).gif" width="([0-9]+)">'
TAG_SUB_PATTERN = r'[\g<short>]'


def replace_markup(text):
    text = re.sub(TAG_IMG_PATTERN, TAG_SUB_PATTERN, unicode(text))
    text = re.sub(r'<font color="red">.*<\/font>', r'(*)', text)

    deleted_tags = [
        '<p>', '</p>',
        '<b>', '</b>',
        '<em>', '</em>',
        '<strong>', '</strong>',
    ]

    replaces = dict.fromkeys(deleted_tags, '')
    replaces['<br>'] = '\n'
    replaces['&gt;'] = '>'

    for original, replacement in replaces.iteritems():
        text = text.replace(original, replacement)

    return text


def parse_card(html):
    bs = BeautifulSoup(html, 'html.parser')
    raw_card_info = bs.find('div', style='padding:5px;position:relative;width:500px;')
    processed = replace_markup(list(raw_card_info.children)[1])
    return processed.split('\n')[:-1]


if __name__ == '__main__':
    response = requests.get('http://www.trekcc.org/2e/index.php?cardID=%s' % sys.argv[1])
    print '\n'.join(parse_card(response.content))
