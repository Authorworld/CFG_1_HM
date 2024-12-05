import tkinter as tk
from tkinter import messagebox
from emulator import ShellEmulator


class ShellGUI:
    def __init__(self, root, emulator):
        self.emulator = emulator
        self.root = root
        self.root.title("Shell Emulator")

        self.output = tk.Text(self.root, height=20, width=80)
        self.output.pack()

        self.entry = tk.Entry(self.root, width=80)
        self.entry.pack()
        self.entry.bind("<Return>", self.execute_command)

    def execute_command(self, event):
        command = self.entry.get()
        self.entry.delete(0, tk.END)

        try:
            if command.startswith("ls"):
                result = self.emulator.ls()
            elif command.startswith("cd"):
                _, directory = command.split(maxsplit=1)
                self.emulator.cd(directory)
                result = f"Changed to {self.emulator.current_path}"
            elif command.startswith("find"):
                _, filename = command.split(maxsplit=1)
                result = self.emulator.find(filename)
            elif command.startswith("uniq"):
                _, file_path = command.split(maxsplit=1)
                result = self.emulator.uniq(file_path)
            elif command == "exit":
                self.root.quit()
                return
            else:
                result = "Unknown command"
        except Exception as e:
            result = f"Error: {e}"

        self.output.insert(tk.END, f"$ {command}\n{result}\n")


if __name__ == "__main__":
    emulator = ShellEmulator("config.json")
    root = tk.Tk()
    gui = ShellGUI(root, emulator)
    root.mainloop()
