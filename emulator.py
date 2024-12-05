import os
import zipfile
import json
import shutil


class ShellEmulator:
    def __init__(self, config_path):
        with open(config_path) as f:
            config = json.load(f)

        self.fs_path = config["fs_path"]
        self.current_path = "/"
        self.virtual_fs = "./virtual_fs"

        if os.path.exists(self.virtual_fs):
            shutil.rmtree(self.virtual_fs)

        with zipfile.ZipFile(self.fs_path, 'r') as zip_ref:
            zip_ref.extractall(self.virtual_fs)

    def ls(self):
        path = os.path.join(self.virtual_fs, self.current_path.lstrip("/"))
        return os.listdir(path)

    def cd(self, directory):
        if directory == "..":
            # Переход на уровень выше
            self.current_path = os.path.dirname(self.current_path.rstrip("/"))
            if not self.current_path:
                self.current_path = "/"
        else:
            new_path = os.path.normpath(os.path.join(self.current_path, directory)).strip("/")
            abs_path = os.path.join(self.virtual_fs, new_path)
            if os.path.isdir(abs_path):
                self.current_path = "/" + new_path if new_path else "/"
            else:
                raise FileNotFoundError(f"No such directory: {directory}")

    def find(self, filename):
        results = []
        for root, _, files in os.walk(self.virtual_fs):
            if filename in files:
                results.append(os.path.relpath(os.path.join(root, filename), self.virtual_fs))
        return results

    def uniq(self, file_path):
        abs_path = os.path.join(self.virtual_fs, self.current_path.lstrip("/"), file_path)
        if os.path.isfile(abs_path):
            with open(abs_path, 'r') as f:
                lines = f.readlines()
            return list(dict.fromkeys(lines))
        raise FileNotFoundError(f"No such file: {file_path}")
