from .memory import generate_memory_with_pointers, get_cell_pointers

def generate_cell_tikz(cell, rendered_index):
    value, pointers = get_cell_pointers(cell)
    value_or_empty_string = str(value) if value != None else ""

    if rendered_index == 0:
        tikz = r"\node[draw, minimum width=1cm, minimum height=0.5cm] (node_%d) {%s};" % (rendered_index, value_or_empty_string)
    else:
        tikz = r"\node[draw, minimum width=1cm, minimum height=0.5cm, above=0cm of node_%d] (node_%d) {%s};" % (rendered_index - 1, rendered_index, value_or_empty_string)

    if len(pointers) > 0:
        pointer_list = ", ".join(pointers)
        tikz += r"\node[right=0.5cm of node_%d] {%s};" % (rendered_index, pointer_list)

    return tikz

def generate_dots_tikz(rendered_index):
    if rendered_index == 0:
        return r"\node[draw, minimum width=1cm] (node_%d) {...};" % (rendered_index)

    return r"\node[draw, minimum width=1cm, above=0cm of node_%d] (node_%d) {...};" % (rendered_index - 1, rendered_index)

def generate_memory_with_pointers_tikz(pointed_memory):
    cells = generate_memory_with_pointers(pointed_memory, generate_cell_tikz, generate_dots_tikz)
    return "\n".join(cells)

def generate_tikz_document(drawing):
    return r"""\documentclass{standalone}
\usepackage{tikz}
\usetikzlibrary{positioning}

\begin{document}
    \begin{tikzpicture}
        %s
    \end{tikzpicture}
\end{document}
    """ % drawing