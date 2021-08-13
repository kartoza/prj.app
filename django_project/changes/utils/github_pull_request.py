""" Tools for parsing the GitHub pull request. """

import re


def parse_funded_by(content: str) -> tuple:
    """ Parse the pull request content and find a 'funded by'.

    It returns the content but without the funder in it if was found.
    """
    token = (
        'funded by', 'sponsored by', 'this is funded by',
        'this is sponsored by',
    )
    funded_regex = r'^({})([\s:]*)'.format('|'.join(token))
    url_regex = r'(https?://\S+)'

    new_content = []
    funded_by = ''
    funded_by_url = ''

    # noinspection PyBroadException
    try:
        lines = content.split('\n')
        for line in lines:

            # If it starts by a markdown bullet list
            cleaned = line.lstrip('* ').strip()
            if cleaned.lower().startswith(token):

                # Remove the "funded by"
                cleaned = re.sub(
                    funded_regex, '', cleaned, flags=re.IGNORECASE)

                # Look for URL
                urls = re.findall(url_regex, cleaned)
                if urls:
                    funded_by_url = urls[0]

                # Remove the URL
                funder = re.sub(url_regex, '', cleaned)
                funded_by = funder.strip()
            else:
                new_content.append(line)

        content = '\n'.join(new_content)
        content = content.strip()
        return content, funded_by, funded_by_url

    except Exception:
        # Let's be safe
        return content, '', ''
