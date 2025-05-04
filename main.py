# --------------------
# IMPORTS
# --------------------
from os import path, listdir
from re import compile
from math import log

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
        for token in tokens:
            std_vector.add(token)
    return list(std_vector)


def make_vector(content, std_vector):
    tokens = get_tokens(content)


def compute_tfidf_weights(md_contents, std_vector):
    N = len(md_contents)
    df_counts = {term: 0 for term in std_vector}

    # Count in how many documents each term appears
    for content in md_contents:
        tokens = set(get_tokens(content))
        for token in tokens:
            if token in df_counts:
                df_counts[token] += 1

    # Compute IDF for each token
    idf_dict = {}
    for term in std_vector:
        df = df_counts.get(term, 0)
        idf_dict[term] = log(N / (1 + df))  # Smoothed with 1

    return idf_dict


def make_tfidf_vector(content, std_vector, idf_dict):
    tokens = get_tokens(content)
    total_terms = len(tokens)

    # Count TF
    tf_counts = {}
    for token in tokens:
        tf_counts[token] = tf_counts.get(token, 0) + 1

    # Build TF-IDF vector
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


# --------------------
# TESTING
# --------------------
if __name__ == '__main__':
    from pprint import pprint

    md_paths = get_md_paths(TARGET_FOLDER)
    md_contents = get_md_contents(md_paths)
    std_vector = make_std_vector(md_contents)

    pprint(md_paths)
    print("\n\n----------------------------------------------------------------------------\n\n")
    pprint(md_contents)
    print("\n\n----------------------------------------------------------------------------\n\n")
    print(std_vector)
    print("\n\n----------------------------------------------------------------------------\n\n")
