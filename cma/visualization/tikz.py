from .memory import generate_memory_with_pointers, get_cell_pointers, is_cell_oob

def generate_cell_tikz(cell, rendered_index, memory_index):
    value, pointers = get_cell_pointers(cell)

    fill_param = ", fill=black" if is_cell_oob(value) else ""
    above_param = r", above=0cm of node_%d" % (rendered_index - 1) if rendered_index != 0 else ""
    value_string = str(value) if value != None and not is_cell_oob(value) else ""
    address_string = r"""
        \node[left=0cm of node_%d, anchor=east, color=black!40] {\small %d};""" % (rendered_index, memory_index) if len(pointers)>0 or not is_cell_oob(value) else ""
    pointer_list = ", ".join(pointers)

    return r"""
        \node[draw, minimum width=1cm, minimum height=0.5cm%s%s] (node_%d) {%s};%s
        \node[right=0.5cm of node_%d, anchor=west] {%s};""" % (
            fill_param,
            above_param,
            rendered_index,
            value_string,
            
            address_string,
            
            rendered_index,
            pointer_list
        )

def generate_dots_tikz(rendered_index):
    if rendered_index == 0:
        return r"""
        \node[draw, minimum width=1cm] (node_%d) {...};""" % (rendered_index)

    return r"""
        \node[draw, minimum width=1cm, above=0cm of node_%d] (node_%d) {...};""" % (rendered_index - 1, rendered_index)

def generate_memory_with_pointers_tikz(pointed_memory, min_addr = None, max_addr = None):
    cells = generate_memory_with_pointers(pointed_memory, generate_cell_tikz, generate_dots_tikz, min_addr, max_addr)
    return "\n".join(cells)

def generate_tikz_document(drawing):
    return r"""\documentclass{standalone}
\usepackage{tikz}
\usetikzlibrary{positioning}

\begin{document}
    \begin{tikzpicture}%s
    \end{tikzpicture}
\end{document}
""" % drawing
