import os
import zipfile

def create_test_zip():
    os.makedirs("example_fs/subdir", exist_ok=True)

    with open("example_fs/example_file.txt", "w") as f:
        f.write("line1\nline2\nline1\n")

    with open("example_fs/subdir/another_file.txt", "w") as f:
        f.write("subdir file\n")

    with zipfile.ZipFile("example_fs.zip", "w") as zipf:
        for root, dirs, files in os.walk("example_fs"):
            for file in files:
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, "example_fs")
                zipf.write(full_path, relative_path)

    print("Test ZIP created: example_fs.zip")

if __name__ == "__main__":
    create_test_zip()
