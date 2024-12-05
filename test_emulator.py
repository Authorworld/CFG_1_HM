import unittest
from emulator import ShellEmulator


class TestShellEmulator(unittest.TestCase):
    def setUp(self):
        self.emulator = ShellEmulator("config.json")

    # ls
    def test_ls_success(self):
        self.assertIn("example_file.txt", self.emulator.ls())

    def test_ls_failure(self):
        self.emulator.current_path = "/nonexistent"
        with self.assertRaises(FileNotFoundError):
            self.emulator.ls()

    # cd
    def test_cd_success(self):
        self.emulator.cd("subdir")
        self.assertEqual(self.emulator.current_path, "/subdir")

    def test_cd_failure_nonexistent(self):
        with self.assertRaises(FileNotFoundError):
            self.emulator.cd("nonexistent_dir")

    def test_cd_failure_not_a_directory(self):
        with self.assertRaises(FileNotFoundError):
            self.emulator.cd("example_file.txt")

    # find
    def test_find_success(self):
        results = self.emulator.find("example_file.txt")
        self.assertTrue(any("example_file.txt" in r for r in results))

    def test_find_failure_nonexistent(self):
        results = self.emulator.find("nonexistent_file.txt")
        self.assertEqual(results, [])

    def test_find_failure_empty_argument(self):
        with self.assertRaises(TypeError):
            self.emulator.find()

    # uniq
    def test_uniq_success(self):
        unique_lines = self.emulator.uniq("example_file.txt")
        self.assertEqual(unique_lines, ["line1\n", "line2\n"])

    def test_uniq_failure_nonexistent_file(self):
        with self.assertRaises(FileNotFoundError):
            self.emulator.uniq("nonexistent_file.txt")

    def test_uniq_failure_directory(self):
        with self.assertRaises(FileNotFoundError):
            self.emulator.uniq("subdir")

    # exit
    def test_exit_success(self):
        with self.assertRaises(SystemExit):
            exit()

    def test_exit_failure_unexpected_behavior(self):
        with self.assertRaises(SystemExit):
            exit()



if __name__ == "__main__":
    unittest.main()
