import unittest
from io import StringIO
import sys
import engine

class TestEngine(unittest.TestCase):

    def setUp(self):
        # Reset TRACE to False before each test
        engine.TRACE = False


    def test_search_data_found(self):
        """Test searching for an existing key using adaptive search."""
        data = [1, 2, 3, 4, 5]
        key = 3
        # Should return index 2
        pos = engine.search_data(data, key)
        self.assertEqual(pos, 2)

    def test_linear_search_direct(self):
        """Test linear_search directly."""
        data = [1, 3, 5]
        self.assertEqual(engine.linear_search(data, 2), 1)
        self.assertEqual(engine.linear_search(data, 0), 0)
        self.assertEqual(engine.linear_search(data, 6), 3)

    def test_binary_search_direct(self):
        """Test binary_search directly."""
        data = [1, 3, 5, 7, 9]
        self.assertEqual(engine.binary_search(data, 4), 2)  # Should point to 5
        self.assertEqual(engine.binary_search(data, 1), 0)  # Should point to 1
        self.assertEqual(engine.binary_search(data, 10), 5) # Should point to end
        self.assertEqual(engine.binary_search(data, 9), 4)  # Should point to 9

    def test_search_data_threshold(self):
        """Test that search_data respects the threshold (adaptive logic)."""
        data = list(range(10))
        original_threshold = engine.SEARCH_THRESHOLD
        try:
            # Case 1: threshold > size -> uses linear (verified by result)
            engine.SEARCH_THRESHOLD = 100
            self.assertEqual(engine.search_data(data, 5), 5)
            
            # Case 2: threshold <= size -> uses binary
            engine.SEARCH_THRESHOLD = 5
            self.assertEqual(engine.search_data(data, 5), 5)
        finally:
            engine.SEARCH_THRESHOLD = original_threshold

    def test_search_data_found_original(self):
        """Test searching for an existing key."""
        data = [1, 2, 3, 4, 5]
        key = 3
        # In the original code, search_data returns the index.
        # But wait, original code loop: for pos in range(len(data)): if key == data[pos]: break
        # It returns 'pos'. If not found, it returns len(data)-1 (loop finishes).
        # My plan is to fix it to return index of first element >= key.
        pos = engine.search_data(data, key)
        self.assertEqual(pos, 2) # Index of 3 is 2

    def test_search_data_not_found_insertion_point(self):
        """Test searching for a non-existent key to find insertion point."""
        data = [1, 3, 5]
        key = 2
        # Should return index 1 (where 3 is), because 3 >= 2
        pos = engine.search_data(data, key)
        self.assertEqual(pos, 1)

    def test_find_pos_highest(self):
        """Test find_pos when key is larger than all elements."""
        data = [1, 2, 3]
        key = 5
        # Should append 5 and return its index (3)
        # Note: original find_pos returns data[-1] if key > last, which is the value.
        # I am refactoring it to return the index.
        pos = engine.find_pos(data, key)
        self.assertEqual(pos, 3) 
        self.assertEqual(data[-1], 5)

    def test_find_pos_middle(self):
        """Test find_pos when key belongs in the middle."""
        data = [1, 3, 5]
        key = 2
        # Should return index 1.
        # The function `insert_key` is currently called only if key > last. 
        # If key < last, `search_data` is called.
        pos = engine.find_pos(data, key)
        self.assertEqual(pos, 1)

    def test_find_pos_existing(self):
        """Test find_pos when key already exists."""
        data = [1, 2, 3, 5]
        key = 5
        # returns len(data) which is index after end? Or index of last element?
        # If key == data[-1], original code returns len(data).
        # It seems it treats it as "already highest".
        # If I want consistent "position", index of 5 is 3.
        # But if it returns len(data), that's 4.
        # I will standardise to return the index of the element.
        pos = engine.find_pos(data, key)
        self.assertEqual(pos, 3)

    def test_edge_case_empty(self):
        """Test with empty array."""
        data = []
        key = 1
        pos = engine.find_pos(data, key)
        self.assertEqual(pos, 0)
        self.assertEqual(data, [1])

    def test_get_sum(self):
        """Test get_sum calculation."""
        data = [1, 2, 3, 4, 5]
        total = engine.get_sum(data)
        self.assertEqual(total, 15)
        
        data = []
        total = engine.get_sum(data)
        self.assertIsNone(total) # get_sum returns None if empty (and prints message)

if __name__ == '__main__':
    unittest.main()
