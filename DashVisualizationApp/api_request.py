import requests


def get_url_data(pid):
    r = requests.get(f"http://tesla.iem.pw.edu.pl:9080/v2/monitor/{pid}")
    rj = r.json()

    taken_data = {"timestamps": rj["trace"]["id"],
                  "values": [i["value"] for i in rj["trace"]["sensors"]],
                  "anomalies": [i["anomaly"] for i in rj["trace"]["sensors"]]}

    return taken_data
