import csv
import json


def main():
    TOKENS_DATA_JSON = "./data/tokens_data.json"
    OUT_MAIN = "./data/tokens_data.csv"
    OUT_STATS = "./data/category_stats.csv"

    with open(TOKENS_DATA_JSON, 'rb') as jsonfb:
        tokens_json = json.load(jsonfb)

    main_headers = ("Category", "Token", "Part-of-Speech", "Occurrences", "Frequency")  # noqa: E501
    stats_headers = ("Category", "Tokens", "Files")
    with open(OUT_MAIN, 'w') as mainf, open(OUT_STATS, 'w') as statsf:
        main_writer = csv.writer(mainf, delimiter=",")
        stats_writer = csv.writer(statsf, delimiter=",")
        main_writer.writerow(main_headers)
        stats_writer.writerow(stats_headers)
        for i, (cat, cat_data) in enumerate(tokens_json.items()):
            total_tokens = cat_data["__tokens__"]
            total_files = cat_data["__files__"]
            stats_writer.writerow((cat, total_tokens, total_files))
            for j, (token, token_data) in enumerate(cat_data.items()):
                if token.startswith("__"):
                    continue
                print(
                    f"Category: {i} Token: {j} Writing to {OUT_MAIN}...",
                    end="\r"
                )
                occurs = token_data["occurs"]
                freq = token_data["freq"]
                for pos in token_data["pos"]:
                    main_writer.writerow((cat, token, pos, occurs, freq))


if __name__ == "__main__":
    main()
