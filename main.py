from simpletoken import build_vocab_pipeline

FILE_PATH = "data/input/insan_ne_ile_yasar.txt"
VOCAB_SIZE = 300
JSON_OUTPUT = "data/output/tokens.json"
VOCAB_OUTPUT = "data/output/tokens.vocab"


# Run the complete BPE vocabulary building pipeline
def main() -> None:
    vocab, stats = build_vocab_pipeline(
        file_path=FILE_PATH,
        vocab_size=VOCAB_SIZE,
        json_output=JSON_OUTPUT,
        vocab_output=VOCAB_OUTPUT,
        show_stats=True,
    )
    
    print("\n" + "="*50)
    print("Summary")
    print("="*50)
    print(f"Vocabulary size: {len(vocab)}")
    print(f"Text statistics: {stats}")


if __name__ == "__main__":
    main()
