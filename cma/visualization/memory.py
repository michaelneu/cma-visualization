class PointedCell:
    def __init__(self, value, pointer):
        self.value = value
        self.pointer = pointer

def point_to_cells(memory, pointers):
    pointed_memory = memory[::]

    for pointer, location in pointers.items():
        if 0 <= location < len(pointed_memory):
            pointed_memory[location] = PointedCell(pointed_memory[location], pointer)

    return pointed_memory

def get_cell_pointers(cell):
    pointers = []

    while isinstance(cell, PointedCell):
        pointers.append(cell.pointer)
        cell = cell.value

    return cell, pointers

def generate_memory_with_pointers(pointed_memory, render_cell, render_dots):
    skipped_cells = []
    rendered_dots = False
    rendered_index = 0

    for memory_index, cell in enumerate(pointed_memory):
        if cell == None and not rendered_dots:
            rendered_dots = True
            skipped_cells.append(
                render_dots(rendered_index)
            )
            rendered_index += 1
        elif cell != None:
            rendered_dots = False
            skipped_cells.append(
                render_cell(cell, rendered_index, memory_index)
            )
            rendered_index += 1

    return skipped_cells
