import unittest
from agents.base_agent import MemoryManager

class TestMemoryManager(unittest.TestCase):
    def setUp(self):
        self.memory_manager = MemoryManager(db_path="test_memory.db")

    def tearDown(self):
        if os.path.exists("test_memory.db"):
            os.remove("test_memory.db")

    def test_load_logs(self):
        with open("tru/Memory_Logs/test.log", 'w') as file:
            file.write("Test log entry\n")
        self.memory_manager.load_logs()
        self.assertEqual(self.memory_manager.collection.count(), 1)

    def test_add_log(self):
        self.memory_manager.add_log("New log entry")
        self.assertEqual(self.memory_manager.collection.count(), 1)

    def test_get_context_empty_db(self):
        self.assertEqual(self.memory_manager.get_context("example query"), "No logs available.")

    def test_get_context_varied_query_results(self):
        self.memory_manager.add_log("Log entry 1")
        self.memory_manager.add_log("Log entry 2")
        self.memory_manager.add_log("Log entry 3")
        context = self.memory_manager.get_context("entry")
        self.assertIn("Log entry 1", context)
        self.assertIn("Log entry 2", context)
        self.assertIn("Log entry 3", context)

if __name__ == "__main__":
    unittest.main()
