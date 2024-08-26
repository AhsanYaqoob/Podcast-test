import yaml
import xml.etree.ElementTree as xml_tree

with open('feed.yaml', 'r') as file:
    yaml_data = yaml.safe_load(file)

    rss_element = xml_tree.Element('rss', {
        'version': '2.0',
        'xmlns:itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd',
        'xmlns:content': 'http://purl.org/rss/1.0/modules/content/'
    })

    Channel_element = xml_tree.SubElement(rss_element, 'channel')

    # Ensure link_prefix is a valid string, default to an empty string if it's None
    link_prefix = yaml_data.get('link', '')

    xml_tree.SubElement(Channel_element, 'title').text = yaml_data['title']
    xml_tree.SubElement(Channel_element, 'format').text = yaml_data['format']
    xml_tree.SubElement(Channel_element, 'subtitle').text = yaml_data['subtitle']
    xml_tree.SubElement(Channel_element, 'itunes:author').text = yaml_data['author']
    xml_tree.SubElement(Channel_element, 'description').text = yaml_data['description']

    # Ensure both link_prefix and image_url are valid strings before concatenating
    image_url = yaml_data.get('image')
    if image_url:  # image_url is not None
        full_image_url = (link_prefix or '') + image_url  # If link_prefix is None, default to an empty string
        xml_tree.SubElement(Channel_element, 'itunes:image', {'href': full_image_url})

    xml_tree.SubElement(Channel_element, 'language').text = yaml_data['language']
    xml_tree.SubElement(Channel_element, 'link').text = link_prefix
    xml_tree.SubElement(Channel_element, 'itunes:category', {'text': yaml_data['category']})

    for item in yaml_data['item']:
        item_element = xml_tree.SubElement(Channel_element, 'item')
        xml_tree.SubElement(item_element, 'title').text = item['title']
        xml_tree.SubElement(item_element, 'itunes:author').text = yaml_data['author']
        xml_tree.SubElement(item_element, 'description').text = item['description']
        xml_tree.SubElement(item_element, 'itunes:duration').text = item['duration']
        xml_tree.SubElement(item_element, 'pubDate').text = item['published']

        enclosure = xml_tree.SubElement(item_element, 'enclosure', {
            'url': (link_prefix or '') + item['file'],  # Ensure link_prefix is valid
            'type': 'audio/mpeg',
            'length': item['length']
        })

    output_tree = xml_tree.ElementTree(rss_element)
    output_tree.write('podcast.xml', encoding='UTF-8', xml_declaration=True)
