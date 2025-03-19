import json
import numpy as np
import os

def save_grouped_logos(urls, labels, output_file):
    if not os.path.exists("outputs"):
        os.mkdir("outputs")

    grouped_logos = {}
    for url, label in zip(urls, labels):
        label=int(label)
        if label not in grouped_logos:
            grouped_logos[label] = []
        grouped_logos[label].append(url)
    with open(output_file, 'w') as f:
        json.dump(grouped_logos, f, indent=4)
    print(f'Grouped logos saved to {output_file}')