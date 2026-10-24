from deep_translator import GoogleTranslator

MAX_CHARS = 4500  # Google's limit is about 5000 per request

def split_text(text, limit=MAX_CHARS):
    """Split long text into chunks that fit the limit."""
    chunks = []
    current = ""
    for line in text.splitlines(keepends=True):
        # Hard-split a single very long line
        while len(line) > limit:
            if current:
                chunks.append(current)
                current = ""
            chunks.append(line[:limit])
            line = line[limit:]
        if len(current) + len(line) > limit:
            chunks.append(current)
            current = ""
        current += line
    if current:
        chunks.append(current)
    return chunks


def translate_to_english(text):
    """Auto-detect the source language and translate to English."""
    translator = GoogleTranslator(source="auto", target="en")

    chunks = [
        chunk for chunk in split_text(text)
        if chunk.strip()
    ]

    if not chunks:
        return ""

    return "\n".join(translator.translate_batch(chunks))


def translate_file(input_path):
    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()
    result = translate_to_english(text)
    output_path = input_path.rsplit(".", 1)[0] + "_english.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result)
    return output_path


def main():
    print("=== Any Language -> English Translator ===")
    while True:
        print("\n1. Translate typed text")
        print("2. Translate a .txt file")
        print("3. Exit")
        choice = input("Choose 1, 2 or 3: ").strip()

        if choice == "1":
            text = input("Enter text: ").strip()
            if not text:
                print("Please type something.")
                continue
            try:
                print("English:", translate_to_english(text))
            except Exception as e:
                print("Error:", e)

        elif choice == "2":
            path = input("Path to .txt file: ").strip().strip('"')
            try:
                out = translate_file(path)
                print("Done! Saved to:", out)
            except FileNotFoundError:
                print("File not found. Check the path.")
            except Exception as e:
                print("Error:", e)

        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()