from shiny import App, ui, reactive, render
from shiny.types import SilentException

app_ui = ui.page_fluid(
    ui.h2("Agenda"),
    
    ui.input_text("titulo", "Nome da Tarefa"),
    ui.input_text_area("descricao", "Descrição da Tarefa"),
    ui.input_action_button("enviar", "Adicionar Tarefa"),

    ui.hr(),
    ui.h3("Tarefas:"),
    ui.output_ui("lista_tarefas")
)

def server(input, output, session):
    tarefas = reactive.Value([])
    next_id = reactive.Value(1)

    @reactive.Effect
    @reactive.event(input.enviar)
    def salvar_tarefa():
        if input.titulo() and input.descricao():
            nova_tarefa = {
                "id": next_id.get(),
                "titulo": input.titulo(),
                "descricao": input.descricao()
            }
            tarefas.set(tarefas.get() + [nova_tarefa])
            next_id.set(next_id.get() + 1)
            ui.update_text("titulo", value="")
            ui.update_text_area("descricao", value="")

    @output
    @render.ui
    def lista_tarefas():
        lista = tarefas.get()
        if not lista:
            return ui.p("Nenhuma tarefa cadastrada.")
        
        tag_list = []
        for tarefa in lista:
            btn_id = f"remover_{tarefa['id']}"
            
            @reactive.Effect
            @reactive.event(input[btn_id])
            def _():
                # Remove a tarefa correspondente
                id_para_remover = int(btn_id.split("_")[1])
                tarefas.set([t for t in tarefas.get() if t["id"] != id_para_remover])
                raise SilentException()  # Evita recarregamento desnecessário

            tag_list.append(
                ui.div(
                    ui.strong(tarefa["titulo"]),
                    ui.p(tarefa["descricao"]),
                    ui.input_action_button(
                        btn_id,
                        "Remover",
                        class_="btn-danger btn-sm"
                    ),
                    class_="mb-3 p-2 border rounded"
                )
            )
        
        return ui.TagList(*tag_list)

app = App(app_ui, server)