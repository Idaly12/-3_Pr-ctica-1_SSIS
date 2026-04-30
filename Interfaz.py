import flet as ft
from CRUD import DatabaseManager

def main(page: ft.Page):
    db = DatabaseManager()
    
    # Configuración general de la ventana
    page.title = "Práctica 1"
    page.bgcolor = "#F8FAFC"
    page.padding = 30
    page.theme_mode = ft.ThemeMode.LIGHT

    # --- CAMPOS DE ENTRADA (Dropdowns y Text) ---
    txt_id = ft.Text(visible=False) # ID oculto para saber qué editamos
    
    dd_plan = ft.Dropdown(label="Plan de Estudios", expand=1)
    dd_carrera = ft.Dropdown(label="Carrera", expand=1)
    dd_materia = ft.Dropdown(label="Materia", expand=1)
    txt_semestre = ft.TextField(label="Semestre (01-10)", width=150)

    # --- TABLA DE DATOS ---
    tabla_datos = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("PLAN")),
            ft.DataColumn(ft.Text("CARRERA")),
            ft.DataColumn(ft.Text("MATERIA")),
            ft.DataColumn(ft.Text("SEM.")),
        ],
    )

    # --- FUNCIONES DE LA INTERFAZ ---
    def actualizar_interfaz():
        # Llenar Dropdowns con datos reales de la DB
        planes, carreras, materias = db.obtener_catalogos()
        dd_plan.options = [ft.dropdown.Option(p[0], f"{p[0]} - {p[1]}") for p in planes]
        dd_carrera.options = [ft.dropdown.Option(c[0], c[1]) for c in carreras]
        dd_materia.options = [ft.dropdown.Option(m[0], m[1]) for m in materias]
        
        # Refrescar la tabla
        tabla_datos.rows.clear()
        for r in db.leer_registros():
            tabla_datos.rows.append(
                ft.DataRow(
                    cells=[ft.DataCell(ft.Text(r[1])), ft.DataCell(ft.Text(r[2])), 
                           ft.DataCell(ft.Text(r[3])), ft.DataCell(ft.Text(str(r[4])))],
                    on_select_change=lambda e, rid=r[0]: cargar_para_editar(rid)
                )
            )
        page.update()

    def cargar_para_editar(rid):
        datos = db.obtener_por_id(rid)
        if datos:
            txt_id.value = str(rid)
            dd_plan.value, dd_carrera.value, dd_materia.value, txt_semestre.value = datos[0]
            page.update()

    def guardar_click(e):
        if dd_plan.value and dd_carrera.value and dd_materia.value:
            db.guardar_registro(dd_plan.value, dd_carrera.value, dd_materia.value, 
                               txt_semestre.value, txt_id.value if txt_id.value else None)
            limpiar_formulario()
            actualizar_interfaz()

    def eliminar_click(e):
        if txt_id.value:
            db.eliminar_registro(txt_id.value)
            limpiar_formulario()
            actualizar_interfaz()

    def limpiar_formulario(e=None):
        txt_id.value = ""
        dd_plan.value = dd_carrera.value = dd_materia.value = txt_semestre.value = None
        page.update()

    # --- DISEÑO VISUAL ---
    page.add(
        ft.Column([
            ft.Text("Práctica 1.", size=28, weight="bold"),
            ft.Container(
                content=ft.Column([
                    ft.Row([dd_plan, dd_carrera]),
                    ft.Row([dd_materia, txt_semestre]),
                    ft.Row([
                        ft.ElevatedButton("Guardar", icon=ft.Icons.SAVE, on_click=guardar_click),
                        ft.ElevatedButton("Eliminar", icon=ft.Icons.DELETE, on_click=eliminar_click, color="red"),
                        ft.TextButton("Limpiar", on_click=limpiar_formulario),
                    ])
                ], spacing=20),
                padding=20, border=ft.border.all(1, "#E2E8F0"), border_radius=10, bgcolor="white"
            ),
            ft.Divider(height=20),
            ft.Text("Registros en Sistema", size=20, weight="bold"),
            ft.Container(content=tabla_datos, border_radius=10)
        ])
    )

    actualizar_interfaz()

if __name__ == "__main__":
    ft.run(main)