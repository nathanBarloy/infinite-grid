import numpy as np
import math


class InfiniteGrid():

    def __init__(self, dimension=2, default=0, init_size=4, init_pos=None):
        self._dimension = dimension
        self._default = default
        if init_pos is None:
            init_pos = [0]*dimension
        else:
            assert len(init_pos) == dimension
        
        # the init position is in the middle of the grid
        self._origin = list(map(lambda x: x-init_size//2, init_pos))
        self._array = np.full([init_size]*dimension, default)
    

    def _get_offset(self, position):
        """This function checks how off is the given position in the grid.
        It will return a list of the offsets of each dimension.
        If the position is in the grid (i.e. all the offsets are 0),
        it will return None.
        """
        assert len(position) == self._dimension

        offsets = [0]*self._dimension
        for i, pos in enumerate(position):
            # Check if lower
            if pos < self._origin[i]:
                offsets[i] = pos - self._origin[i]
                continue
            # Check if higher
            if pos >= self._origin[i] + self._array.shape[i]:
                offsets[i] = pos - (self._origin[i] + self._array.shape[i]) + 1
                continue
        
        if all(map(lambda x: x==0, offsets)):
            return None
        else:
            return offsets
    

    def _is_in(self, position):
        """Check if the given position is in the grid."""
        return self._get_offset(position) is None
    

    def _shift_position(self, position):
        """Return the shifted position according to the origin."""
        res = []
        for i, pos in enumerate(position):
            res.append(pos - self._origin[i])
        return tuple(res)


    def __repr__(self):
        return self._array.__repr__()
    

    def __str__(self):
        return self._array.__str__()
    

    def __getitem__(self, key):
        if self._is_in(key):
            in_array_pos = self._shift_position(key)
            return self._array[in_array_pos]
        else:
            return self._default
    

    def __setitem__(self, key, value):
        offsets = self._get_offset(key)
        in_array_pos = self._shift_position(key)
        if offsets is None:
            self._array[in_array_pos] = value
        else:
            # We have to redimension the grid
            for i, off in enumerate(offsets):
                if off == 0:
                    continue
                if off > 0:
                    # First, compute the number of rows to add
                    pow_fact = math.ceil(math.log2(off/self._array.shape[i] + 1))
                    nb_add = self._array.shape[i] * (2 ** pow_fact - 1)
                    
                    # Create new array to add
                    new_shape = list(self._array.shape)
                    new_shape[i] = nb_add
                    new_shape = tuple(new_shape)
                    new_arr = np.full(new_shape, self._default)

                    # Add new array to grid
                    self._array = np.concatenate((self._array, new_arr), axis=i)
                
                else:  # off < 0
                    off = -off
                    # First, compute the number of rows to add
                    pow_fact = math.ceil(math.log2(off/self._array.shape[i] + 1))
                    nb_add = self._array.shape[i] * (2 ** pow_fact - 1)
                    
                    # Create new array to add
                    new_shape = list(self._array.shape)
                    new_shape[i] = nb_add
                    new_shape = tuple(new_shape)
                    new_arr = np.full(new_shape, self._default)

                    # Add new array to grid
                    self._array = np.concatenate((new_arr, self._array), axis=i)

                    # Update origin
                    self._origin[i] -= nb_add
            
            # Recompute coordinates, and set value
            in_array_pos = self._shift_position(key)
            self._array[in_array_pos] = value
