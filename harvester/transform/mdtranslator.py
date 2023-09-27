import requests
import xml.etree.ElementTree as ET


def translate_mbjson_to_iso():
    # download xml or parse local file
    xml_data = ET.parse("path_to_xml")

    root = xml_data.getroot()
    xml_str = ET.tostring(root, encoding="utf8")

    res = requests.post(
        "https://api.sciencebase.gov/mdTranslator/api/v3/translator",
        {"file": xml_str, "reader": "fgdc", "writer": "iso19110"},
    )

    # write the output locally
    # open( "out.xml", "w" ).write(str(res.content, "utf-8"))


if __name__ == "__main__":
    translate_mbjson_to_iso()
