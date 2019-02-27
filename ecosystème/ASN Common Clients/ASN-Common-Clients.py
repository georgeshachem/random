import requests

with open('asn-31126-39010.txt') as f:
    lines = f.readlines()
    lines = [x.strip() for x in lines]

clients = list()

for line in lines:
    data = line.split(":")
    clients.append([x for x in data[2].split(' ') if x])

common_clients = set.intersection(*map(set, clients))

with open('clients-commun.txt', 'w+') as f:
    for asn in common_clients:
        r = requests.get(
            'https://stat.ripe.net/data/abuse-contact-finder/data.json?resource={}'.format(asn.strip()))
        asn_name = r.json()['data']['holder_info']['name']
        f.write("{} - {}\n".format(asn, asn_name))
