import requests

with open('asn-42020.txt') as f:
    lines = f.readlines()
    lines = [x.strip() for x in lines]

for line in lines:
    data = line.split(":")
    main_asn = data[0]
    fournisseurs = [x for x in data[1].split(' ') if x]
    clients = [x for x in data[2].split(' ') if x]

    r = requests.get(
        'https://stat.ripe.net/data/abuse-contact-finder/data.json?resource={}'.format(main_asn.strip()))
    main_asn_name = r.json()['data']['holder_info']['name']
    with open('{} - {}.txt'.format(main_asn, main_asn_name), 'w+') as f:
        f.write('Main:\n')
        f.write("{} - {}\n".format(main_asn, main_asn_name))
        f.write('\n')
        f.write('Fournisseurs ({}):\n'.format(len(fournisseurs)))

    with open('{} - {}.txt'.format(main_asn, main_asn_name), 'a+') as f:
        for asn in fournisseurs:
            r = requests.get(
                'https://stat.ripe.net/data/abuse-contact-finder/data.json?resource={}'.format(asn.strip()))
            asn_name = r.json()['data']['holder_info']['name']
            f.write("{} - {}\n".format(asn, asn_name))
        f.write('\n')
        f.write('Clients ({}):\n'.format(len(clients)))

    with open('{} - {}.txt'.format(main_asn, main_asn_name), 'a+') as f:
        for asn in clients:
            r = requests.get(
                'https://stat.ripe.net/data/abuse-contact-finder/data.json?resource={}'.format(asn))
            asn_name = r.json()['data']['holder_info']['name']
            f.write("{} - {}\n".format(asn, asn_name))
