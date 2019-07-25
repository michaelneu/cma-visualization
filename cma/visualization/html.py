from .memory import generate_memory_with_pointers, get_cell_pointers

def generate_tab_pane_html(title, body):
    return f"""
        <div class="tab_pane">
            <h2>{title}</h2>
            <div class="tab_body" style="margin: 1rem 0rem;">{body}</div>
        </div>
    """

def generate_copyable_tab_pane_html(title, body):
    return generate_tab_pane_html(title, f"""
        <textarea
            style="font-family: monospace; padding: 1rem; border: 1px solid #bbb; border-radius: 5px; width: 100%; height: 10rem; resize: none;"
            readonly
        >{body}</textarea>
    """)

def generate_program_line_with_number(instruction, line_number, active=False):
    line_number_color = "#aaa"
    code_color = "black"

    if active:
        line_number_color = "red"
        code_color = "red"

    arguments = ", ".join(instruction.args)

    html = f"""
        <div class="instruction">
            <pre style="display: inline-block;">   </pre>
            <pre style="display: inline-block; color: {line_number_color};">% 3d</pre>
            <pre style="display: inline-block; color: {code_color};"> {instruction.name} {arguments}</pre>
        </div>
    """ % (line_number)

    return html

def generate_program_tab_pane_html(program, program_counter):
    indented_code = "\n".join([
        generate_program_line_with_number(instruction, line_number, line_number == program_counter)
        for line_number, instruction
        in enumerate(program)
    ])

    return generate_tab_pane_html("Code", f"""
        <div
            class="program"
            style="background-color: #f7f7f7; border: 1px solid #bbb; border-radius: 5px; padding: 1rem;"
        >{indented_code}</div>
    """)

def generate_cell_html(cell, _rendered_index):
    value, pointers = get_cell_pointers(cell)
    value_or_empty_string = value if value != None else ""
    pointer_list = ", ".join(pointers)

    return f"""
        <tr class="cell">
            <td class="value" style="border: 1px solid #333; text-align: center">{value_or_empty_string}</td>
            <td>{pointer_list}</td>
        </tr>
    """

def generate_dots_html(_rendered_index):
    return """
        <tr class="dots">
            <td style="border: 1px solid #333;">...</td>
        </tr>
    """

def generate_memory_with_pointers_html(pointed_memory):
    cells = generate_memory_with_pointers(pointed_memory, generate_cell_html, generate_dots_html)
    reversed_cells = reversed(cells)
    rendered_cells = "\n".join(reversed_cells)
    return f"""
        <table class="memory">
            {rendered_cells}
        </table>
    """

def generate_row_html(*columns):
    body = "\n".join(columns)
    return f"""
        <div class="row" style="margin: 0rem -1rem;">
            {body}
            <br style="clear: both;" />
        </div>
    """

def generate_column_html(width, *items):
    body = "\n".join(items)
    return f"""
        <div class="col-{width}" style="float: left; width: {width}%; padding: 0rem 1rem;">{body}</div>
    """

def generate_html_document(*items):
    body = "\n".join(items)
    return """<!doctype html>
<html>
    <head>
        <title>CMa Visualization</title>
        <style type="text/css">
            body {
                margin: 0rem;
                font-size: 14px;
                font-family: sans-serif;
            }

            * {
                box-sizing: border-box;
            }
        </style>
    </head>
    <body>
        %s
    </body>
</html>
    """ % body
