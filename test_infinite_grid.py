from infinite_grid import InfiniteGrid
import unittest as ut
import numpy as np


class TestInfiniteGrid(ut.TestCase):
    def test_creation(self):
        gr1 = InfiniteGrid()
        gr2 = InfiniteGrid(default='*')
        self.assertIsNotNone(gr1)
        self.assertIsNotNone(gr2)

    def test_get(self):
        grid = InfiniteGrid()
        self.assertEqual(grid[0,0], 0)
        self.assertEqual(grid[-1,7], 0)
    
    def test_set(self):
        grid = InfiniteGrid()
        grid[0,0] = 1
        self.assertEqual(grid[0,0], 1)
        self.assertEqual(grid[1,0], 0)
        arr = np.array([[0,0,0,0],
                        [0,0,0,0],
                        [0,0,1,0],
                        [0,0,0,0]])
        self.assertTrue(np.array_equal(grid._array, arr))

        grid[1,5] = 7
        grid[-1,1] = 3
        self.assertEqual(grid._origin, [-2, -2])
        arr = np.array([[0,0,0,0,0,0,0,0],
                        [0,0,0,3,0,0,0,0],
                        [0,0,1,0,0,0,0,0],
                        [0,0,0,0,0,0,0,7]])
        self.assertEqual(grid._array.shape, arr.shape)
        self.assertTrue(np.array_equal(grid._array, arr))
    
    def test_set_back(self):
        grid = InfiniteGrid(default=' ', init_size=2, init_pos=(1,1))
        grid[0,0] = 'x'
        self.assertEqual(grid[0,0], 'x')
        self.assertEqual(grid[1,0], ' ')
        self.assertEqual(grid._origin, [0, 0])
        arr = np.array([['x', ' '],
                        [' ', ' ']])
        self.assertTrue(np.array_equal(grid._array, arr))

        grid[-6,1] = 'o'
        self.assertEqual(grid._origin, [-6, 0])
        arr = np.array([[' ', 'o'],
                        [' ', ' '],
                        [' ', ' '],
                        [' ', ' '],
                        [' ', ' '],
                        [' ', ' '],
                        ['x', ' '],
                        [' ', ' '],])
        self.assertEqual(grid._array.shape, arr.shape)
        self.assertTrue(np.array_equal(grid._array, arr))

        grid[-5,-1] = 'v'
        self.assertEqual(grid._origin, [-6, -2])
        arr = np.array([[' ', ' ', ' ', 'o'],
                        [' ', 'v', ' ', ' '],
                        [' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' '],
                        [' ', ' ', 'x', ' '],
                        [' ', ' ', ' ', ' '],])
        self.assertEqual(grid._array.shape, arr.shape)
        self.assertTrue(np.array_equal(grid._array, arr))



if __name__ == "__main__":
    ut.main()