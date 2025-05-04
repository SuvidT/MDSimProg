# --------------------
# IMPORTS
# --------------------
from os import path, listdir
from re import compile
from math import log, sqrt
from os.path import basename

# --------------------
# CONSTANTS
# --------------------
TARGET_FOLDER = '/Users/suvidthungathurti/Documents/Vault/'

# --------------------
# FUNCTIONS
# --------------------
def read_file(target_file):
    try:
        with open(target_file, "r") as f:
            content = f.read()
        return content
    except FileNotFoundError:
        print("That file does not exist")
    except Exception as e:
        print(f"Error: {e}")


def get_md_paths(target_folder):
    md_paths = []
    for item in listdir(target_folder):
        full_path = path.join(target_folder, item)
        if path.isfile(full_path) and full_path.lower().endswith('.md'):
            md_paths.append(full_path)
        elif path.isdir(full_path):
            md_paths.extend(get_md_paths(full_path))  # Recursive call
    return md_paths


def get_md_contents(md_paths):
    md_contents = []
    for path in md_paths:
        md_contents.append(read_file(path))
    return md_contents


def get_tokens(content):
    contractions = {
        "don't": ["do", "not"],
        "can't": ["can", "not"],
        "won't": ["will", "not"],
        "it's": ["it", "is"],
    }

    content = content.lower()

    for contraction, expansion in contractions.items():
        content = content.replace(contraction, ' '.join(expansion))

    token_pattern = compile(r"\b\w[\w'-]*\b")
    words = token_pattern.findall(content)

    tokens = []
    for word in words:
        if word.endswith("'s") and len(word) > 2:
            tokens.append(word[:-2])
            tokens.append("'s")
        else:
            tokens.append(word)

    return tokens


def make_std_vector(md_contents):
    std_vector = set()
    for content in md_contents:
        tokens = get_tokens(content)
        std_vector.update(tokens)
    return list(std_vector)


def compute_tfidf_weights(md_contents, std_vector):
    N = len(md_contents)
    df_counts = {term: 0 for term in std_vector}

    for content in md_contents:
        tokens = set(get_tokens(content))
        for token in tokens:
            if token in df_counts:
                df_counts[token] += 1

    idf_dict = {}
    for term in std_vector:
        df = df_counts.get(term, 0)
        idf_dict[term] = log(N / (1 + df))  # Smoothed with +1

    return idf_dict


def make_tfidf_vector(content, std_vector, idf_dict):
    tokens = get_tokens(content)
    total_terms = len(tokens)

    tf_counts = {}
    for token in tokens:
        tf_counts[token] = tf_counts.get(token, 0) + 1

    tfidf_vector = []
    for term in std_vector:
        tf = tf_counts.get(term, 0) / total_terms if total_terms else 0
        idf = idf_dict.get(term, 0)
        tfidf_vector.append(tf * idf)

    return tfidf_vector


def make_tfidf_vectors_for_all(md_paths, md_contents, std_vector, idf_dict):
    tfidf_dict = {}
    for path, content in zip(md_paths, md_contents):
        tfidf_vector = make_tfidf_vector(content, std_vector, idf_dict)
        tfidf_dict[path] = tfidf_vector
    return tfidf_dict


def cosine_similarity(vec1, vec2):
    dot = sum(a * b for a, b in zip(vec1, vec2))
    mag1 = sqrt(sum(a * a for a in vec1))
    mag2 = sqrt(sum(b * b for b in vec2))
    return dot / (mag1 * mag2) if mag1 and mag2 else 0.0


def build_similarity_matrix(target_folder):
    md_paths = get_md_paths(target_folder)
    md_contents = get_md_contents(md_paths)
    std_vector = make_std_vector(md_contents)
    idf_dict = compute_tfidf_weights(md_contents, std_vector)
    tfidf_vectors = make_tfidf_vectors_for_all(md_paths, md_contents, std_vector, idf_dict)

    file_names = [basename(p) for p in md_paths]
    file_map = {basename(p): tfidf_vectors[p] for p in md_paths}

    similarity_dict = {}

    for file1 in file_names:
        similarity_dict[file1] = {}
        for file2 in file_names:
            if file1 != file2:
                vec1 = file_map[file1]
                vec2 = file_map[file2]
                similarity = cosine_similarity(vec1, vec2)
                similarity_dict[file1][file2] = round(similarity, 4)

    return similarity_dict

# --------------------
# DATA VISUALIZATION
# --------------------
# this section is entirely from chatgpt

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def display_similarity_heatmap(similarity_dict):
    # Get a consistent sorted list of filenames
    filenames = sorted(similarity_dict.keys())

    # Reconstruct the DataFrame using the same order for rows and columns
    df = pd.DataFrame(
        [[similarity_dict.get(row, {}).get(col, 0) for col in filenames] for row in filenames],
        index=filenames,
        columns=filenames
    )

    plt.figure(figsize=(10, 8))
    sns.heatmap(df, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
    plt.title("Markdown File Similarity (Cosine TF-IDF)")
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.show()




# --------------------
# MAIN
# --------------------
if __name__ == '__main__':
    from pprint import pprint

    result = build_similarity_matrix(TARGET_FOLDER)
    pprint(result)
    display_similarity_heatmap(result)