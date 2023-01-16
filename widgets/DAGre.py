import dagre

# Creazione del grafo
graph = dagre._graph()

# Aggiunta dei nodi al grafo
graph.set_node("x", { "label": "x", "width": 100, "height": 50 })
graph.set_node("y", { "label": "y", "width": 100, "height": 50 })
graph.set_node("z", { "label": "z", "width": 100, "height": 50 })

# Aggiunta delle connessioni tra i nodi
graph.set_edge("x", "y")
graph.set_edge("y", "z")

# Posizionamento dei nodi
dagre.layout(graph)

# Stampa della posizione dei nodi
print(graph.node_dict())