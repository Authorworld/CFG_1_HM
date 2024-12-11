import unittest
import os
import zipfile
from tempfile import TemporaryDirectory
from main import Shell  # Импортируем эмулятор


class TestShellEmulator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Создаем временный ZIP-архив для тестов"""
        cls.temp_zip = TemporaryDirectory()
        cls.zip_path = os.path.join(cls.temp_zip.name, "virtual_fs.zip")
        # Создаем тестовый ZIP-архив с файлами и директориями
        with zipfile.ZipFile(cls.zip_path, 'w') as archive:
            archive.writestr('file1.txt', 'Hello, world!\nLine 2\nLine 3\nHello, world!')
            archive.writestr('dir1/file2.txt', 'Sample content')

    @classmethod
    def tearDownClass(cls):
        """Удаляем временный ZIP-архив"""
        cls.temp_zip.cleanup()

    def setUp(self):
        """Создаем новый экземпляр эмулятора для каждого теста"""
        self.emulator = Shell(self.zip_path)

    def tearDown(self):
        """Удаляем эмулятор после каждого теста"""
        del self.emulator

    # Тесты для команды ls
    def test_ls_files(self):
        """Тест на команду ls для вывода файлов и директорий"""
        result = self.emulator.run_command("ls")
        self.assertIn('file1.txt', result)
        self.assertIn('dir1', result)

    def test_ls_detailed(self):
        """Тест на команду ls с флагом -l для подробного вывода"""
        result = self.emulator.run_command("ls -l")
        self.assertIn('file1.txt', result)
        self.assertIn('dir1', result)

    # Тесты для команды cd
    def test_cd_success(self):
        """Тест на команду cd для перехода в директорию"""
        result = self.emulator.run_command("cd dir1")
        self.assertEqual(self.emulator.get_current_path(), "/dir1")

    def test_cd_failure(self):
        """Тест на команду cd для перехода в несуществующую директорию"""
        result = self.emulator.run_command("cd non_existing_dir")
        self.assertEqual(result, "No such directory: non_existing_dir")

    # Тесты для команды find
    def test_find_success(self):
        """Тест на команду find для поиска файлов"""
        result = self.emulator.run_command("find file")
        self.assertIn("file1.txt", result)
        self.assertIn("dir1/file2.txt", result)

    def test_find_no_match(self):
        """Тест на команду find для поиска без совпадений"""
        result = self.emulator.run_command("find non_existing_file")
        self.assertEqual(result, "No matches found")

    # Тесты для команды uniq
    def test_uniq_success(self):
        """Тест на команду uniq для фильтрации уникальных строк"""
        result = self.emulator.run_command("uniq file1.txt")
        self.assertEqual(result, "Hello, world!\nLine 2\nLine 3")

    def test_uniq_failure(self):
        """Тест на команду uniq для несуществующего файла"""
        result = self.emulator.run_command("uniq non_existing_file.txt")
        self.assertEqual(result, "No such file: non_existing_file.txt")


if __name__ == "__main__":
    unittest.main()
