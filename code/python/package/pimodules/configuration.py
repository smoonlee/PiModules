import xmltodict

DEFAULT_FSSD_XML_CONFIG = """<?xml version="1.0" encoding="utf-8"?>
<root>
    <fssd:config xmlns:fssd="http://pimodules.com/">
        <fssd:alerts>
            <fssd:email>
                <fssd:enabled>False</fssd:enabled>
                <fssd:username></fssd:username>
                <fssd:sender-email-address></fssd:sender-email-address>
                <fssd:sender-password></fssd:sender-password>
                <fssd:recipient-email-address></fssd:recipient-email-address>
                <fssd:subject-template></fssd:subject-template>
                <fssd:body-template></fssd:body-template>
                <fssd:server></fssd:server>
                <fssd:security></fssd:security>
                <fssd:port>0</fssd:port>
            </fssd:email>
        </fssd:alerts>
    </fssd:config>
</root>
"""


def read_config_xml(xml, default=True):
    try:
        if default:
            data_dict = xmltodict.parse(DEFAULT_FSSD_XML_CONFIG)
        else:
            with open(xml, "rt") as fi:
                data_dict = xmltodict.parse(fi.read())

    except IOError as e:
        data_dict = xmltodict.parse(DEFAULT_FSSD_XML_CONFIG)

    return data_dict

def write_config_xml(xmlfile, data_dict):
    try:
        with open(xmlfile, "wt") as fo:
            xmltodict.unparse(data_dict, fo, pretty=True)
    except IOError as e:
        print("Error writing XML file: ", e)
        return False

    return True
