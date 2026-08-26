import os


def main():
    folder = "createFile"
    os.makedirs(folder, exist_ok=True)

    out_path = os.path.join(folder, "output.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("hello\n")

    print(f"Wrote 'hello' to {out_path}")


if __name__ == "__main__":
    main()
