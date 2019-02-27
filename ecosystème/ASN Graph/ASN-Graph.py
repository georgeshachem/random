import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()

with open('asconn.txt') as f:
    lines = f.readlines()
    lines = [x.strip() for x in lines]

all_asn = dict()
asn_to_draw = ['31126', '39010']
selected_nodes = {'31126', '39010'}

for line in lines:
    data = line.split(":")
    main_asn = data[0].strip()
    fournisseurs = [x.strip() for x in data[1].split(' ') if x]
    clients = [x.strip() for x in data[2].split(' ') if x]

    all_asn[main_asn] = {'fournisseurs': fournisseurs, 'clients': clients}

    for asn in fournisseurs:
        G.add_edge(asn, main_asn)
    for asn in clients:
        G.add_edge(main_asn, asn)

    if main_asn in asn_to_draw:
        for asn in fournisseurs:
            selected_nodes.add(asn)
        for asn in clients:
            selected_nodes.add(asn)

H = G.subgraph(selected_nodes)
nx.draw(H, with_labels=True, node_size=30)
plt.show()
