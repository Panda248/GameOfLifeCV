# Grid class for Game of Life implementation
# uses a padded grid

from grid import Grid
import numpy as np
import pyopencl as cl
from pyopencl import Context, CommandQueue
from pyopencl import array as cl_array

class GPUGrid(Grid):
    def __init__(self, cols: int, rows: int):
        super().__init__(cols, rows)
        self.context = cl.create_some_context(interactive=False)
        self.queue = cl.CommandQueue(self.context)
        self.program = cl.Program(self.context, open("life.cl").read()).build()
        self.kernel = cl.Kernel(self.program, "update")

    def update(self):
        
        prev = cl_array.to_device(self.queue, self.grid)
        new_grid = cl_array.empty(self.queue, self.grid.shape, dtype=self.grid.dtype)
        cols_padded = np.int32(self.cols + 2)
        rows = np.int32(self.rows)
        cols = np.int32(self.cols)
        if prev.data == None or new_grid.data == None:
            print("Error: OpenCL buffers not created properly")
            return
        
        self.kernel(self.queue, (self.rows, self.cols), None, 
            cols_padded, prev.data, new_grid.data)

        self.grid = new_grid.get()