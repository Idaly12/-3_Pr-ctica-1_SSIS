import flet as ft
from CRUD import DatabaseManager

def main(page: ft.Page):
    db = DatabaseManager()
    page.title = "Reingeniería - Practica 1"
    page.padding = 30
    page.theme_mode = ft.ThemeMode.LIGHT

    # --- LÓGICA DE VALIDACIÓN Y MÁSCARA ---
    def formatear_fecha(e):
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
            if dia > 31: v = v[:6] + "31"
            elif dia == 0: v = v[:6] + "01"

        # Aplicar Formato AAAA-MM-DD
        v = v[:8]
        nuevo = ""
        if len(v) > 0: nuevo = v[:4]
        if len(v) > 4: nuevo += "-" + v[4:6]
        if len(v) > 6: nuevo += "-" + v[6:8]
            
        if e.control.value != nuevo:
            e.control.value = nuevo
            e.control.update()

    # --- CAMPOS DE LA INTERFAZ ---
    txt_id = ft.Text(visible=False)
    dd_plan = ft.Dropdown(label="Plan", expand=1)
    dd_carrera = ft.Dropdown(label="Carrera", expand=2)
    dd_materia = ft.Dropdown(label="Materia", expand=2)
    
    dd_semestre = ft.Dropdown(
        label="Semestre", 
        width=140,
        options=[ft.dropdown.Option(str(i).zfill(2)) for i in range(1, 11)]
    )
    
    txt_fecalt = ft.TextField(label="Fecha Alta", hint_text="AAAA-MM-DD", expand=1, on_change=formatear_fecha)
    txt_fecbaj = ft.TextField(label="Fecha Baja", hint_text="AAAA-MM-DD", expand=1, on_change=formatear_fecha)

    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("PLAN")),
            ft.DataColumn(ft.Text("CARRERA")),
            ft.DataColumn(ft.Text("MATERIA")),
            ft.DataColumn(ft.Text("SEM.")),
            ft.DataColumn(ft.Text("ALTA")),
            ft.DataColumn(ft.Text("BAJA")),
        ],
    )

    def refrescar():
        res = db.obtener_catalogos()
        dd_plan.options = [ft.dropdown.Option(p[0]) for p in res[0]]
        dd_carrera.options = [ft.dropdown.Option(c[0], c[1]) for c in res[1]]
        dd_materia.options = [ft.dropdown.Option(m[0], m[1]) for m in res[2]]
        
        tabla.rows.clear()
        for r in db.leer_registros():
            tabla.rows.append(ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(r[1])), ft.DataCell(ft.Text(r[2])), 
                    ft.DataCell(ft.Text(r[3])), ft.DataCell(ft.Text(r[4])),
                    ft.DataCell(ft.Text(r[5])), ft.DataCell(ft.Text(r[6] if r[6] else "-"))
                ],
                on_select_change=lambda e, rid=r[0]: cargar(rid)
            ))
        page.update()

    def cargar(rid):
        d = db.obtener_por_id(rid)
        if d:
            txt_id.value = str(rid)
            dd_plan.value, dd_carrera.value, dd_materia.value, dd_semestre.value, txt_fecalt.value, txt_fecbaj.value = d[0]
            page.update()

    def guardar(e):
        db.guardar_registro(
            dd_plan.value, dd_carrera.value, dd_materia.value, 
            dd_semestre.value, txt_fecalt.value, txt_fecbaj.value,
            txt_id.value if txt_id.value else None
        )
        limpiar()
        refrescar()

    def limpiar(e=None):
        txt_id.value = ""
        dd_plan.value = dd_carrera.value = dd_materia.value = dd_semestre.value = None
        txt_fecalt.value = txt_fecbaj.value = ""
        page.update()

    # --- DISEÑO ---
    page.add(
        ft.Text("Administración de Planes de Estudio", size=24, weight="bold"),
        ft.Column([
            ft.Row([dd_plan, dd_carrera, dd_semestre]),
            ft.Row([dd_materia, txt_fecalt, txt_fecbaj]),
            ft.Row([
                ft.FilledButton("Guardar", icon=ft.Icons.SAVE, on_click=guardar),
                ft.FilledButton("Eliminar", icon=ft.Icons.DELETE, 
                                on_click=lambda _: (db.eliminar_registro(txt_id.value), limpiar(), refrescar()), 
                                bgcolor="red700"),
                ft.TextButton("Limpiar", on_click=limpiar)
            ])
        ], spacing=20),
        ft.Divider(),
        tabla
    )
    refrescar()

if __name__ == "__main__":
    ft.run(main)