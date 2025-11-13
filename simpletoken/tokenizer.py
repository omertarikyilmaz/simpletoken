from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Dict, List, Tuple

BASE_VOCAB_SIZE = 256


# Read UTF-8 text file and return contents as string
def read_file(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


# Encode text as UTF-8 bytes
def utf_encode(text: str) -> bytes:
    return text.encode("utf-8")


# Analyze text and return character, word, byte statistics
def analyze_text(text: str) -> Dict[str, int]:
    char_length = len(text)
    word_length = len(text.split())
    utf8_bytes = list(text.encode("utf-8"))
    byte_length = len(utf8_bytes)
    unique_bytes = len(set(utf8_bytes))
    
    return {
        "char_length": char_length,
        "word_length": word_length,
        "byte_length": byte_length,
        "unique_bytes": unique_bytes,
    }


# Find all consecutive byte pairs and count their frequencies
def find_byte_pairs(utf8_bytes: List[int]) -> Tuple[List[Tuple[int, int]], Dict[Tuple[int, int], int]]:
    pairs = [
        (utf8_bytes[i], utf8_bytes[i + 1])
        for i in range(len(utf8_bytes) - 1)
    ]
    
    pair_counts = {}
    for p in pairs:
        if p not in pair_counts:
            pair_counts[p] = 0
        pair_counts[p] += 1
    
    return pairs, pair_counts


# Sort byte pairs by frequency (most frequent first)
def get_sorted_pairs(pair_counts: Dict[Tuple[int, int], int]) -> List[Tuple[int, int]]:
    return sorted(pair_counts.keys(), key=lambda x: pair_counts[x], reverse=True)


# Build vocabulary from 256 base bytes plus most frequent pairs
def build_vocab_from_pairs(sorted_pairs: List[Tuple[int, int]], vocab_size: int) -> List[Tuple]:
    vocab = [(b,) for b in range(BASE_VOCAB_SIZE)]
    max_pair_add = max(vocab_size - len(vocab), 0)
    selected_pairs = sorted_pairs[:max_pair_add]
    vocab.extend(selected_pairs)
    return vocab


# Display vocabulary tokens with byte sequences and decoded strings
def visualize_vocab(vocab: List[Tuple], limit: int = 40) -> None:
    print(f"Total vocab size: {len(vocab)}\n")
    print(f"Showing first {limit} tokens:\n")
    for i, tok in enumerate(vocab[:limit]):
        b = bytes(tok)
        try:
            s = b.decode("utf-8", errors="replace")
        except:
            s = ""
        print(f"{i:3d} | bytes: {list(b)!r:<15} | str: {s!r}")


# Export vocabulary to JSON format
def format_vocab_json(vocab: List[Tuple], output_path: str = "vocab.json") -> None:
    import json
    
    vocab_json = []
    for token_id, tok in enumerate(vocab):
        b = bytes(tok)
        try:
            s = b.decode("utf-8")
        except:
            s = ""
        
        vocab_json.append({
            "token_id": token_id,
            "utf8_bytes": list(tok),
            "string": s
        })
    
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(vocab_json, f, ensure_ascii=False, indent=2)
    
    print(f"Saved vocab.json with {len(vocab_json)} tokens.")


# Export vocabulary to plain text format
def format_vocab_text(vocab: List[Tuple], output_path: str = "tokens.vocab") -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        for token_id, tok in enumerate(vocab):
            b = bytes(tok)
            try:
                s = b.decode("utf-8")
            except:
                s = ""
            
            line = f"{token_id:<4d} {str(list(tok)): <15} {s}\n"
            f.write(line)
    
    print(f"tokens.vocab created with {len(vocab)} tokens.")


# Complete pipeline: analyze text, find pairs, build vocab, export formats
def build_vocab_pipeline(
    file_path: str,
    vocab_size: int = 300,
    json_output: str | None = None,
    vocab_output: str | None = None,
    show_stats: bool = True,
) -> Tuple[List[Tuple], Dict]:
    text = read_file(file_path)
    stats_dict = analyze_text(text)
    
    if show_stats:
        print("Step-1 | Analyse")
        print(f"Length of word/characters in text: {stats_dict['word_length']} / {stats_dict['char_length']}")
        print(f"Bytes length: {stats_dict['byte_length']} | Unique Bytes Length: {stats_dict['unique_bytes']}\n")
    
    utf8_bytes = list(text.encode("utf-8"))
    pairs, pair_counts = find_byte_pairs(utf8_bytes)
    sorted_pairs = get_sorted_pairs(pair_counts)
    
    if show_stats:
        print("Step-2 | Pairing")
        print(f"Total pairs: {len(pairs)}")
        print(f"Unique pairs: {len(pair_counts)}")
        print("\nTop 10 Most Frequent Pairs")
        print("---------------------------")
        for i, pair in enumerate(sorted_pairs[:10]):
            print(f"Pair: {pair} | Count: {pair_counts[pair]}")
        print()
    
    vocab = build_vocab_from_pairs(sorted_pairs, vocab_size)
    
    if show_stats:
        print("Step-3 | Merging")
        print(f"Target vocab size: {vocab_size}")
        print(f"Final vocab size: {len(vocab)}\n")
    
    if show_stats:
        print("Step-4 | Visualising")
        visualize_vocab(vocab, limit=40)
        print()
    
    if json_output:
        print("Step-5 | Formatting")
        print("1-) JSON Formatting")
        format_vocab_json(vocab, json_output)
        print()
    
    if vocab_output:
        if not json_output:
            print("Step-5 | Formatting")
        print("2-) Vocab Formatting")
        format_vocab_text(vocab, vocab_output)
        print()
    
    return vocab, stats_dict
