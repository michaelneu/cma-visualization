class PointedCell:
    def __init__(self, value, pointer):
        self.value = value
        self.pointer = pointer

class OOBCell:
    pass

def point_to_cells(memory, pointers):
    pointed_memory = {location: memory[location] for location in range(len(memory))}

    for pointer, location in pointers.items():
        # get instead of [] to have PointedCells with value==OOBCell instead of KeyErrors for out-of-bounds pointers
        # Note that get will still return None if the location is undefined in memory.
        pointed_memory[location] = PointedCell(pointed_memory.get(location, OOBCell()), pointer)

    return pointed_memory

def is_cell_oob(cell):
    return isinstance(cell, OOBCell)

def get_cell_pointers(cell):
    pointers = []

    while isinstance(cell, PointedCell):
        pointers.append(cell.pointer)
        cell = cell.value

    return cell, pointers

def generate_memory_with_pointers(pointed_memory, render_cell, render_dots, min_addr = None, max_addr = None):
    if min_addr == None:
        min_addr = min(pointed_memory.keys())
    if max_addr == None:
        max_addr = max(pointed_memory.keys()) + 1

    skipped_cells = []
    rendered_dots = False
    rendered_index = 0

    for memory_index in range(min_addr, max_addr):
        # Note that get will still return None if the location is undefined in memory.
        cell = pointed_memory.get(memory_index, OOBCell())
        if cell == None and not rendered_dots and rendered_index != 0:
            rendered_dots = True
            skipped_cells.append(
                render_dots(rendered_index)
            )
            rendered_index += 1
        elif cell != None or rendered_index == 0:
            rendered_dots = False
            skipped_cells.append(
                render_cell(cell, rendered_index, memory_index)
            )
            rendered_index += 1

    return skipped_cells
