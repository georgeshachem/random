import pandas as pd

with open('asconn.txt') as f:
    lines = f.readlines()
    lines = [x.strip() for x in lines]

all_asn = dict()
for line in lines:
    data = line.split(":")
    main_asn = data[0].strip()
    fournisseurs = [x.strip() for x in data[1].split(' ') if x]
    clients = [x.strip() for x in data[2].split(' ') if x]

    all_asn[main_asn] = {'fournisseurs': len(fournisseurs), 'clients': len(clients)}

df = pd.DataFrame.from_dict(all_asn, orient='index')
writer = pd.ExcelWriter('ASN.xlsx')
df.to_excel(writer)
writer.save()
