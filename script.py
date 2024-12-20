import requests
from datetime import datetime
from email.utils import format_datetime


installation_keys = [
    "49b268f4-e5db-49a3-87ad-ee23f397eadd"
]

now = format_datetime(datetime.now())

for installation_key in installation_keys:

    output = f"<rss><channel><pubDate>{now}</pubDate>"

    url = f"https://api.gbif.org/v1/dataset/search?installationKey={installation_key}"
    response = requests.get(url)
    data = response.json()
    dataset_keys = [dataset["key"] for dataset in data["results"]]

    for dataset_key in dataset_keys:
        url = f"https://api.gbif.org/v1/dataset/{dataset_key}"
        response = requests.get(url)
        data = response.json()
        endpoints = [endpoint for endpoint in data["endpoints"] if endpoint["type"] == "DWC_ARCHIVE"]
        if len(endpoints) > 0:
            title = data["title"]
            endpoint = endpoints[0]
            url = endpoint["url"]
            modified = datetime.fromisoformat(endpoint["modified"])
            pubdate = format_datetime(modified)

            output = output + f"<item><title>{title}</title><link>{url}</link><ipt:dwca>{url}</ipt:dwca><pubDate>{pubdate}</pubDate></item>"

    output = output + "</channel></rss>"

    file = open(f"feed_{installation_key}.rss", "w")
    file.write(output)
    file.close()
