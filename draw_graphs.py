import os
import networkx as nx
from networkx.algorithms import bipartite
from matplotlib import pyplot as plt


def main():
    PICKLED_GRAPHS = "./graphs/"

    SEED = 123
    N_TOKENS = 100
    ALL_N_TOKENS = 40

    CAT_COLOR = "#e6990b"
    TOKEN_COLOR = "#77bfe6"

    ALL_CAT_G = nx.Graph()
    for graph in os.listdir(PICKLED_GRAPHS):
        print(f"Drawing {graph}... ".ljust(50, " "), end="\r")
        if "ALL_" in graph:
            continue

        cat_nodename = graph.split("_", maxsplit=1)[0].upper()

        g_path = os.path.join(PICKLED_GRAPHS, graph)
        G = nx.read_gpickle(g_path)
        plt.clf()

        cat_nodes, token_nodes = bipartite.sets(G)

        n_token_nodes = list(token_nodes)[:ALL_N_TOKENS]

        ALL_CAT_G.add_nodes_from(cat_nodes, bipartite=0)
        ALL_CAT_G.add_nodes_from(n_token_nodes, bipartite=1)

        i = 0
        for cn, tn, weight in G.edges(data="weight"):
            if tn in n_token_nodes:
                if i < ALL_N_TOKENS:
                    ALL_CAT_G.add_edge(cn, tn, weight=weight)
                    i += 1

        pos = nx.random_layout(G, seed=SEED)
        pos[cat_nodename] = (0.5, 0.5)

        nx.draw_networkx_edges(G, pos, edgelist=G.edges, width=0.4, alpha=0.25)
        nx.draw_networkx_nodes(G, pos, nodelist=cat_nodes, node_color=CAT_COLOR, node_size=1500, node_shape="h")
        nx.draw_networkx_nodes(G, pos, nodelist=token_nodes, node_color=TOKEN_COLOR)
        nx.draw_networkx_labels(G, pos, font_size=10)

        plt.axis("off")
        plt.tight_layout()
        fig = plt.gcf()
        fig.set_facecolor("white")
        fig.set_figheight(7)
        fig.set_figwidth(9)
        plt.savefig(f"./plots/{cat_nodename}_{N_TOKENS}.png")

    cat_nodes, token_nodes = bipartite.sets(ALL_CAT_G)
    plt.clf()

    print(len(ALL_CAT_G.nodes), " "*50)

    pos = nx.bipartite_layout(ALL_CAT_G, cat_nodes, align="horizontal")

    nx.draw_networkx_edges(ALL_CAT_G, pos, edgelist=ALL_CAT_G.edges, width=0.4, alpha=0.25)
    nx.draw_networkx_nodes(ALL_CAT_G, pos, nodelist=token_nodes, node_color=TOKEN_COLOR)
    nx.draw_networkx_labels(ALL_CAT_G, pos, font_size=10)
    nx.draw_networkx_nodes(ALL_CAT_G, pos, nodelist=cat_nodes, node_color=CAT_COLOR, node_size=1500, node_shape="h")

    plt.axis("off")
    plt.tight_layout()
    fig = plt.gcf()
    fig.set_facecolor("white")
    fig.set_figheight(20)
    fig.set_figwidth(50)
    plt.savefig(f"./plots/ALL_CAT_{ALL_N_TOKENS}.png")


if __name__ == "__main__":
    main()
