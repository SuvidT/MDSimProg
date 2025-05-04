# Markdown File Similarity Analyzer

This script analyzes the similarity between Markdown (`.md`) files in a specified directory. It uses TF-IDF vectorization and cosine similarity to compute how similar each file is to the others based on word content.

---

## Target Folder

```python
TARGET_FOLDER = '/Users/suvidthungathurti/Documents/Vault/'
```

* This constant defines the folder where `.md` files will be searched recursively.

---

## Functions Summary

### `read_file(target_file)`

Reads the content of a file given its path.

* Returns the file content as a string.
* Handles missing file errors gracefully.

---

### `get_md_paths(target_folder)`

Recursively collects all `.md` file paths from the target folder.

* Returns a list of full paths to Markdown files.

---

### `get_md_contents(md_paths)`

Reads all files in the provided list of Markdown paths.

* Returns a list of file contents.

---

### `get_tokens(content)`

Tokenizes the input text:

* Converts text to lowercase.
* Expands common contractions (e.g., "don't" → "do not").
* Uses a regular expression to split words and handle possessives.
* Returns a list of tokens.

---

### `make_std_vector(md_contents)`

Builds a vocabulary list (standard vector) from all tokens in the Markdown contents.

* Returns a list of unique tokens across all files.

---

### `compute_tfidf_weights(md_contents, std_vector)`

Computes Inverse Document Frequency (IDF) values for the vocabulary.

* Uses smoothed IDF: `log(N / (1 + df))`.
* Returns a dictionary mapping terms to IDF scores.

---

### `make_tfidf_vector(content, std_vector, idf_dict)`

Computes the TF-IDF vector for a single document.

* Normalizes term frequencies.
* Multiplies by corresponding IDF values.
* Returns a list of TF-IDF values.

---

### `make_tfidf_vectors_for_all(md_paths, md_contents, std_vector, idf_dict)`

Generates TF-IDF vectors for all Markdown files.

* Returns a dictionary mapping file paths to their TF-IDF vectors.

---

### `cosine_similarity(vec1, vec2)`

Computes cosine similarity between two TF-IDF vectors.

* Returns a similarity score between 0 and 1.

---

### `build_similarity_matrix(target_folder)`

Main orchestrator that:

1. Collects all `.md` file paths and contents.
2. Builds the vocabulary and IDF dictionary.
3. Creates TF-IDF vectors for each file.
4. Computes cosine similarity between all pairs of files.

* Returns a nested dictionary `{file1: {file2: similarity}}`.

---

## Main Execution

When run directly:

* Calls `build_similarity_matrix()` on the target folder.
* Pretty-prints the similarity matrix using `pprint`.

---

## Example Output

```
{'file1.md': {'file2.md': 0.5829, 'file3.md': 0.1943}, ...}
```

---

## Use Cases

* Detect content overlap or plagiarism.
* Cluster similar notes.
* Analyze content similarity in personal or team knowledge bases.

---

Let me know if you'd like this README saved as a file or formatted for a PDF version.
