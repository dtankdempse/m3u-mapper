import json
import os
import gzip
import requests
import xml.etree.ElementTree as ET

input_url = "https://epgshare01.online/epgshare01/epg_ripper_ALL_SOURCES1.xml.gz"
output_file = os.path.join(os.getcwd(), "data", "tvg-ids.json")

def convert_gz_xml_to_json(input_url, output_file):
    response = requests.get(input_url, stream=True)
    if response.status_code != 200:
        print(f"Failed to fetch the input file. Status code: {response.status_code}")
        return
    
    with gzip.GzipFile(fileobj=response.raw) as gz_file:
        context = ET.iterparse(gz_file, events=("start", "end"))
        _, root = next(context)
        data = {}
        for event, elem in context:
            if event == "end" and elem.tag == "channel":
                channel_id = elem.get("id")
                if channel_id:
                    parts = channel_id.split(".")
                    region = parts[-1] if len(parts) > 1 else "unknown"
                    if region not in data:
                        data[region] = []
                    data[region].append(channel_id)
                root.clear()
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)
    
    # print(f"JSON by region created at {output_file}")

convert_gz_xml_to_json(input_url, output_file)
