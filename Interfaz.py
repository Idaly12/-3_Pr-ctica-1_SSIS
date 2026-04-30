import flet as ft
from CRUD import DatabaseManager

def main(page: ft.Page):
    db = DatabaseManager()
    page.title = "Reingeniería - Practica 1"
    page.padding = 30
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # Esta columna contendra físicamente los Checkboxes 
    lista_checks = ft.Column(scroll=ft.ScrollMode.AUTO, height=150)

    # logica y validacion
    def formatear_fecha(e):
        # Filtra solo dígitos para aplicar la máscara
        v = "".join(filter(str.isdigit, e.control.value))
        
        # Validar Año (Rango 1982 - 2026)
        if len(v) >= 4:
            anio = int(v[:4])
            if anio < 1982: anio = 1982
            elif anio > 2026: anio = 2026
            v = str(anio) + v[4:]
        
        # Validar Mes (Máximo 12)
        if len(v) >= 6:
            mes = int(v[4:6])
            if mes > 12: v = v[:4] + "12" + v[6:]
            elif mes == 0: v = v[:4] + "01" + v[6:]
        
        # Validar Día (Máximo 31)
        if len(v) >= 8:
            dia = int(v[6:8])
            if dia > 31: v = v[:6] + "31" + v[8:]
            elif dia == 0: v = v[:6] + "01" + v[8:]

        # Aplicar formato YYYY/MM/DD para consistencia con la BD
        if len(v) > 4 and len(v) <= 6:
            v = v[:4] + "/" + v[4:]
        elif len(v) > 6:
            v = v[:4] + "/" + v[4:6] + "/" + v[6:8]
        
        e.control.value = v
        # Al escribir, se limpia el borde de error si lo tuviera
        if e.control.border_color == ft.Colors.RED and len(v) > 0:
            e.control.border_color = None
        page.update()

    def actualizar_prerrequisitos(e=None):
        # Desactiva la opción en los prerrequisitos que coincida con la materia seleccionada
        materia_seleccionada = dd_materia.value
        
        # Limpia el color de error si se seleccionó una materia válida
        if materia_seleccionada and dd_materia.border_color == ft.Colors.RED:
            dd_materia.border_color = None

        for check in lista_checks.controls:
            if materia_seleccionada and check.data == materia_seleccionada:
                check.disabled = True
                check.value = False
            else:
                check.disabled = False
        page.update()

    def limpiar_borde_error_dropdown(e):
        # Función auxiliar para limpiar bordes rojos al seleccionar una opción en los demás dropdowns
        if e.control.value and e.control.border_color == ft.Colors.RED:
            e.control.border_color = None
            page.update()

    # --- COMPONENTES ---
    txt_id = ft.Text(visible=False)
    dd_plan = ft.Dropdown(label="Plan", expand=1, on_select=limpiar_borde_error_dropdown)
    dd_carrera = ft.Dropdown(label="Carrera", expand=3, on_select=limpiar_borde_error_dropdown)
    dd_materia = ft.Dropdown(label="Materia", expand=True, on_select=actualizar_prerrequisitos)
    dd_semestre = ft.Dropdown(
        label="Semestre",
        options=[ft.dropdown.Option(f"{i:02d}") for i in range(1, 11)],
        width=160,
        on_select=limpiar_borde_error_dropdown
    )

    txt_fecalt = ft.TextField(label="Fecha Alta (YYYY/MM/DD)", on_change=formatear_fecha, expand=1)
    txt_fecbaj = ft.TextField(label="Fecha Baja (YYYY/MM/DD)", on_change=formatear_fecha, expand=1)

    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Plan")),
            ft.DataColumn(ft.Text("Carrera")),
            ft.DataColumn(ft.Text("Materia")),
            ft.DataColumn(ft.Text("Sem.")),
            ft.DataColumn(ft.Text("Alta")),
            ft.DataColumn(ft.Text("Baja")),
            ft.DataColumn(ft.Text("Acción")), 
        ],
        rows=[]
    )

    def cargar_catalogos():
        # Carga inicial de datos maestros desde la base de datos
        planes, carreras, materias = db.obtener_catalogos()
        dd_plan.options = [ft.dropdown.Option(p[0], p[1]) for p in planes]
        dd_carrera.options = [ft.dropdown.Option(c[0], c[1]) for c in carreras]
        dd_materia.options = [ft.dropdown.Option(m[0], m[1]) for m in materias]
        
        # Llena la lista de Checkboxes para representar la tabla de prerrequisitos
        lista_checks.controls.clear()
        for m in materias:
            lista_checks.controls.append(
                ft.Checkbox(label=m[1], value=False, data=m[0])
            )
        page.update()

    def refrescar():
        # Actualiza la vista de la tabla con los registros actuales
        registros = db.leer_registros()
        nuevas_filas = []
        for row in registros:
            rid = row[0]
            nuevas_filas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(row[0]))),
                        ft.DataCell(ft.Text(str(row[1]))),
                        ft.DataCell(ft.Text(str(row[2]))),
                        ft.DataCell(ft.Text(str(row[3]))),
                        ft.DataCell(ft.Text(str(row[4]))),
                        ft.DataCell(ft.Text(str(row[5]))),
                        ft.DataCell(ft.Text(str(row[6]))),
                        ft.DataCell(
                            ft.TextButton(
                                "Editar",
                                on_click=lambda e, id_reg=rid: seleccionar_fila(id_reg)
                            )
                        ),
                    ]
                )
            )
        tabla.rows = nuevas_filas
        page.update()

    def seleccionar_fila(rid):
        # Se obtiene el registro exacto por ID para recuperar las claves correctas de los dropdowns
        datos_registro = db.obtener_por_id(rid)
        if datos_registro:
            row = datos_registro[0]
            txt_id.value = str(rid)
            dd_plan.value = row[0]
            dd_carrera.value = row[1]
            dd_materia.value = row[2]
            dd_semestre.value = row[3]
            txt_fecalt.value = row[4]
            txt_fecbaj.value = row[5]
            
            # Sincroniza los Checkboxes con los prerrequisitos guardados en la BD
            reqs = db.obtener_requisitos_por_id(rid)
            for check in lista_checks.controls:
                check.value = True if check.data in reqs else False
            
            # Limpia los bordes rojos al seleccionar para editar
            for campo in [dd_plan, dd_carrera, dd_materia, dd_semestre, txt_fecalt]:
                campo.border_color = None
            
            # Valida las restricciones de materia en los prerrequisitos
            actualizar_prerrequisitos()

    def guardar(e):
        # Se definen los campos que son requeridos obligatoriamente
        campos_requeridos = [dd_plan, dd_carrera, dd_materia, dd_semestre, txt_fecalt]
        es_valido = True

        # Validación visual: pintar de rojo si el valor está vacío
        for campo in campos_requeridos:
            if not campo.value or str(campo.value).strip() == "":
                campo.border_color = ft.Colors.RED
                es_valido = False
            else:
                campo.border_color = None

        if not es_valido:
            page.update()
            return

        # Recolecta los IDs de las materias marcadas en la lista de seriación
        reqs_seleccionados = [
            check.data for check in lista_checks.controls if check.value == True
        ]
        
        # Ejecuta la operacion de guardado (Insert o Update) incluyendo requisitos
        db.guardar_registro(
            dd_plan.value, dd_carrera.value, dd_materia.value, 
            dd_semestre.value, txt_fecalt.value, txt_fecbaj.value,
            requisitos_ids=reqs_seleccionados,
            rid=txt_id.value if txt_id.value else None
        )
        limpiar()
        refrescar()

    def limpiar(e=None):
        # Restablece todos los campos del formulario
        txt_id.value = ""
        dd_plan.value = dd_carrera.value = dd_materia.value = dd_semestre.value = None
        txt_fecalt.value = txt_fecbaj.value = ""
        
        # colores de los bordes 
        for campo in [dd_plan, dd_carrera, dd_materia, dd_semestre, txt_fecalt, txt_fecbaj]:
            campo.border_color = None

        for check in lista_checks.controls:
            check.value = False
        
        # Restablece el estado de los componentes bloqueados
        actualizar_prerrequisitos()

    def eliminar(e):
        # Elimina el registro seleccionado previa validación de ID
        if txt_id.value:
            db.eliminar_registro(txt_id.value)
            limpiar()
            refrescar()

    #diseño
    page.add(
        ft.Text("Administración de Planes de Estudio - Reingeniería", size=24, weight="bold"),
        ft.Column([
            ft.Row([dd_plan, dd_carrera, dd_semestre]),
            ft.Row([dd_materia, txt_fecalt, txt_fecbaj]),
            ft.Text("Seleccionar Prerrequisitos (Seriación):", weight="bold"),
            ft.Container(
                content=lista_checks, 
                border=ft.border.all(1, ft.Colors.OUTLINE), 
                padding=10, 
                border_radius=5
            ),
            ft.Row([
                ft.FilledButton("Guardar", icon="save", on_click=guardar),
                ft.ElevatedButton("Limpiar", icon="cleaning_services", on_click=limpiar),
                ft.TextButton("Eliminar", icon="delete", icon_color="red", on_click=eliminar)
            ]),
            ft.Divider(),
            ft.Column([tabla], scroll=ft.ScrollMode.ALWAYS, height=300)
        ])
    )

    cargar_catalogos()
    refrescar()

ft.app(target=main)