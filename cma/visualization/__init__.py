from .html import generate_tab_pane_html, generate_program_tab_pane_html, generate_row_html, generate_column_html, generate_column_html, generate_memory_with_pointers_html, generate_copyable_tab_pane_html, generate_html_document
from .tikz import generate_tikz_document, generate_memory_with_pointers_tikz
from .memory import point_to_cells

def render_vm_state_to_html(vm):
    code_html = generate_program_tab_pane_html(vm.C, vm.PC, vm.labels)
    pointed_memory = point_to_cells(vm.S, {
        "SP": vm.SP,
        "EP": vm.EP,
        "HP": vm.HP,
    })

    memory_html = generate_memory_with_pointers_html(pointed_memory)

    return generate_row_html(
        generate_column_html(
            30,
            generate_tab_pane_html(
                "Memory",
                memory_html,
            ),
        ),
        generate_column_html(
            70,
            code_html,
            generate_row_html(
                generate_column_html(
                    50,
                    generate_copyable_tab_pane_html(
                        "HTML",
                        generate_html_document(
                            code_html,
                            "<br />",
                            memory_html,
                        ),
                    ),
                ),
                generate_column_html(
                    50,
                    generate_copyable_tab_pane_html(
                        "LaTeX/Tikz",
                        generate_tikz_document(
                            generate_memory_with_pointers_tikz(pointed_memory),
                        )
                    ),
                ),
            ),
        ),
    )
