import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

def hierarchy_pos(G, root=None, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):
    '''
    Calcola le posizioni per un layout gerarchico di un grafo.
    
    Parameters:
    -----------
    G : NetworkX graph
        A directed graph
    root : node, optional
        The root node of the hierarchy
    width : float, optional
        Horizontal space allocated for this branch
    vert_gap : float, optional
        Gap between levels of hierarchy
    vert_loc : float, optional
        Vertical location of root
    xcenter : float, optional
        Horizontal location of root
    '''
    if not G.is_directed():
        raise TypeError('Graph must be directed')
    
    if root is None:
        # Find a root if one exists
        try:
            root = next(iter(nx.topological_sort(G)))  # A root in a tree
        except nx.NetworkXUnfeasible:
            # The graph has cycles, use a node with min in-degree
            root = sorted(G.nodes(), key=lambda n: G.in_degree(n))[0]
    
    def _hierarchy_pos(G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5, pos=None, parent=None, parsed=None):
        if pos is None:
            pos = {root: (xcenter, vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        
        if parsed is None:
            parsed = []
        parsed.append(root)
            
        # Get all neighbors (successors in directed graph)
        if hasattr(G, 'successors'):
            children = list(G.successors(root))
        else:
            children = list(G.neighbors(root))
            
        # Safely filter out the parent if it exists in the children list
        if parent is not None and parent in children:
            children.remove(parent)
            
        if len(children) != 0:
            dx = width / len(children)
            nextx = xcenter - width/2 - dx/2
            for child in children:
                if child not in parsed:
                    nextx += dx
                    pos = _hierarchy_pos(G, child, width=dx, vert_gap=vert_gap, 
                                         vert_loc=vert_loc-vert_gap, xcenter=nextx, 
                                         pos=pos, parent=root, parsed=parsed)
        return pos
            
    return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)

try:
    # Prova a caricare il CSV
    try:
        df = pd.read_csv('labels_hierarchy_.csv')
    except FileNotFoundError:
        # Se il file non esiste, creiamo dati di esempio
        print("File 'labels_hierarchy.csv' non trovato. Creando dati di esempio...")
        data = {
            'Label': ['Atlantic Records', 'Columbia Records', 'Warner Records', 
                     'Atlantic Jazz', 'Columbia Classical', 'Warner Pop',
                     'Atlantic R&B', 'Columbia Country', 'Warner Rock',
                     'Sony Music', 'Warner Music Group', 'Universal Music'],
            'Parent': ['Warner Music Group', 'Sony Music', 'Warner Music Group',
                      'Atlantic Records', 'Columbia Records', 'Warner Records',
                      'Atlantic Records', 'Columbia Records', 'Warner Records',
                      None, None, None]
        }
        df = pd.DataFrame(data)

    # Crea un grafo diretto
    G = nx.DiGraph()

    # Aggiungi i nodi e le connessioni
    for _, row in df.iterrows():
        label = row['Label']
        parent = row['Parent']
        G.add_node(label)
        if pd.notna(parent):
            G.add_edge(parent, label)

    # Trova la radice (nodo senza predecessori)
    roots = [n for n, d in G.in_degree() if d == 0]
    if not roots:
        raise ValueError("Nessuna radice trovata nel grafo.")
        
    # Se ci sono più radici, creiamo un super-nodo radice
    if len(roots) > 1:
        super_root = "Etichette Discografiche"
        G.add_node(super_root)
        for root in roots:
            G.add_edge(super_root, root)
        root = super_root
    else:
        root = roots[0]

    # Calcola le posizioni gerarchiche
    pos = hierarchy_pos(G, root)

    # Personalizza l'aspetto per un risultato migliore
    figure(figsize=(16, 10), dpi=80)
    
    # Prepara node_colors basandosi sul livello
    node_colors = []
    node_sizes = []
    
    for node in G.nodes():
        if node in roots:
            node_colors.append('#FF9999')  # Rosso chiaro per le radici
            node_sizes.append(3000)
        elif G.out_degree(node) > 0:  # Nodi intermedi con figli
            node_colors.append('#99CCFF')  # Blu chiaro per i nodi intermedi
            node_sizes.append(2500)
        else:  # Foglie
            node_colors.append('#99FF99')  # Verde chiaro per le foglie
            node_sizes.append(2000)
    
    # Disegna il grafo con etichette più leggibili
    nx.draw(G, pos, 
            with_labels=True, 
            node_size=node_sizes,
            node_color=node_colors, 
            font_size=12, 
            font_weight='bold',
            font_color='black',
            arrows=True,
            arrowsize=20,
            edge_color='gray',
            width=2.0,
            alpha=0.9)
    
    plt.title('Gerarchia delle Etichette Discografiche Americane', fontsize=18, fontweight='bold')
    plt.tight_layout()
    plt.show()

except Exception as e:
    print(f"Si è verificato un errore: {e}")
    
    # In caso di problemi, proviamo un approccio più semplice
    if 'G' in locals() and 'pos' not in locals():
        print("Tentativo con una visualizzazione più semplice...")
        plt.figure(figsize=(12, 8))
        nx.draw(G, pos=nx.spring_layout(G), with_labels=True, 
                node_size=1500, node_color='lightblue', font_size=10)
        plt.title('Visualizzazione alternativa della gerarchia')
        plt.show()