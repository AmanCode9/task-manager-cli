import os
import tempfile
import unittest
from tasks import TaskManager

class TestTaskManager(unittest.TestCase):
    def setUp(self):
        fd, path = tempfile.mkstemp()
        os.close(fd)
        os.remove(path)
        self.path = path
        self.mgr = TaskManager(filepath=path)

    def test_add_and_find(self):
        t = self.mgr.add_task("test", "desc", "2025-09-02")
        self.assertEqual(self.mgr.find(t.id).title, "test")

    def test_update_task(self):
        t = self.mgr.add_task("test")
        self.mgr.update(t.id, title="updated")
        self.assertEqual(self.mgr.find(t.id).title, "updated")

    def test_mark_complete(self):
        t = self.mgr.add_task("test")
        self.mgr.mark_complete(t.id)
        self.assertEqual(self.mgr.find(t.id).status, "Completed")

    def test_delete_task(self):
        t = self.mgr.add_task("test")
        self.mgr.delete(t.id)
        self.assertIsNone(self.mgr.find(t.id))

if __name__ == "__main__":
    unittest.main()
