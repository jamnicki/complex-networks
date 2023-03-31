import os
import csv
import json
from collections import defaultdict
from nltk.tokenize import word_tokenize
from nltk import pos_tag


def main():
    INPUT_DIR = "./data/CLEAN_wiki_articles"
    CATEGORIES = "./data/categories.tsv"
    OUTPUT = "./data/tokens_data.json"

    SKIP_TOKENS = [
        "copyright", "also", "may", "first", "would", "one", "many",
        "two", "however", "could", "three", "four", "five", "six", "seven",
        "eight", "nine", "ten", "eleven", "twelve", "several", "new", "often",
        "used", "much"
    ]

    tokens_data = defaultdict(
        lambda: defaultdict(
            lambda: defaultdict()
        )
    )

    with open(CATEGORIES) as cat_f:
        i = 0
        cat_files = defaultdict(int)
        for row in csv.reader(cat_f, delimiter="\t"):
            print(f"({i}) Tagging and counting token occurrences...", end="\r")
            i += 1
            filename, category = row[0] + ".txt", row[1].split(".")[1]
            file_path = os.path.join(INPUT_DIR, filename)
            tokens_occur = defaultdict(int)
            tokens_pos = defaultdict(set)
            with open(file_path, "r") as fin:
                cat_files[category] += 1
                for line in fin:
                    tokens = word_tokenize(line, language="english")
                    pos_tags = pos_tag(tokens)
                    for token, pos in pos_tags:
                        if token in SKIP_TOKENS:
                            continue
                        tokens_occur[token] += 1
                        tokens_pos[token].add(pos)
            for token, occurs in tokens_occur.items():
                tokens_data[category][token]["occurs"] = occurs
            for token, tags in tokens_pos.items():
                tokens_data[category][token]["pos"] = list(tags)
    for cat, cat_data in tokens_data.items():
        tokens_data[cat]["__tokens__"] = len(cat_data.values())
        tokens_data[cat]["__files__"] = cat_files[cat]

    for i, (cat, cat_data) in enumerate(tokens_data.items()):
        print(f"({i}) Calculating frequency...", end="\r")
        total = cat_data["__tokens__"]
        for token, token_data in cat_data.items():
            if token.startswith("__"):
                continue
            occurs = token_data["occurs"]
            tokens_data[cat][token]["freq"] = token_data["occurs"] / total

    for i, (cat, cat_data) in enumerate(tokens_data.items()):
        print(f"({i}) Sorting the data...", end="\r")
        new_cat_data = {
            __key: value
            for __key, value in cat_data.items()
            if "__" in __key
        }
        sorted_cat_data = dict(sorted(
            [(k, v) for k, v in cat_data.items() if not k.startswith("__")],
            reverse=True,
            key=lambda item: item[1]["occurs"]
        ))
        new_cat_data.update(sorted_cat_data)
        tokens_data[cat] = new_cat_data

    with open(OUTPUT, "w") as fout:
        print(f"Saving to {OUTPUT}...", end="\r")
        json.dump(tokens_data, fout, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
