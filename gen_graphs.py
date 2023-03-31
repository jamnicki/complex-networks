import pandas as pd
import networkx as nx
from networkx.algorithms import bipartite
from matplotlib import pyplot as plt


def get_core_pos(pos):
    if pos.startswith("NN"):
        return "Noun"
    elif pos.startswith("PR"):
        return "Pronoun"
    elif pos.startswith("VB"):
        return "Verb"
    elif pos.startswith("JJ"):
        return "Adjective"
    elif pos.startswith("RB"):
        return "Adverb"
    elif pos.startswith("IN"):
        return "Preposition"
    elif pos.startswith("CC"):
        return "Conjunction"
    elif pos.startswith("UH"):
        return "Interjection"
    return pd.NA


def main():
    TOKENS_DATA = "./data/tokens_data.csv"
    CATEGORY_STATS = "./data/category_stats.csv"

    tokens_df = pd.read_csv(TOKENS_DATA)
    tokens_df["Part-of-Speech"] = tokens_df["Part-of-Speech"].apply(get_core_pos)
    tokens_df.dropna(inplace=True)

    cat_stats_df = pd.read_csv(CATEGORY_STATS)
    categories = cat_stats_df["Category"].unique()

    # bipartite=0 - "Category"
    # bipartite=1 - "Token"

    SEED = 123
    N_TOKENS = 100
    ALL_N_TOKENS = 10

    CAT_COLOR = "#e6990b"
    TOKEN_COLOR = "#77bfe6"

    ALL_CAT_G = nx.Graph()
    for j, category in enumerate(categories):
        print(f"Genereting {category}...  ({str(j).rjust(2, '0')})", end="\r")
        G = nx.Graph()
        cat_nodename = category.upper()

        G.add_node(cat_nodename, bipartite=0)
        ALL_CAT_G.add_node(cat_nodename, bipartite=0)

        _tokens_df = tokens_df.loc[tokens_df["Category"] == category]
        unique_tokens = _tokens_df["Token"].unique()
        total_tokens = unique_tokens.shape[0]
        weights_dict = {
            token: _tokens_df.loc[_tokens_df["Token"] == token]["Occurrences"].to_numpy()[0]
            for token in unique_tokens
        }
        weights_dict = dict(sorted(
            weights_dict.items(),
            reverse=True,
            key=lambda item: item[1]
        ))
        for i, (token, weight) in enumerate(weights_dict.items()):
            if i < N_TOKENS-1:
                G.add_node(token, bipartite=1)
                G.add_edge(cat_nodename, token, weight=weight)
            if i < ALL_N_TOKENS-1:
                ALL_CAT_G.add_node(token, bipartite=1)
                ALL_CAT_G.add_edge(cat_nodename, token, weight=weight, label=str(weight))

        cat_nodes, token_nodes = bipartite.sets(G)

        pos = nx.random_layout(G, seed=SEED)
        pos[cat_nodename] = (0.5, 0.5)

        nx.write_gpickle(G, f"./graphs/{category}_{N_TOKENS}.gpickle")

    cat_nodes, token_nodes = bipartite.sets(ALL_CAT_G)

    pos = nx.random_layout(ALL_CAT_G, seed=SEED)
    # pos[cat_nodename] = (0.5, 0.5)

    nx.write_gpickle(G, f"./graphs/ALL_CAT_{ALL_N_TOKENS}.gpickle")


if __name__ == "__main__":
    main()
