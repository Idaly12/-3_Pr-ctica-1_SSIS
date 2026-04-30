import sqlite3
import os

class DatabaseManager:
    def __init__(self):
        # Ruta dinámica para encontrar la base de datos en la misma carpeta
        self.db_path = os.path.join(os.path.dirname(__file__), "baseDedatosIng.db")

    def _ejecutar_query(self, query, params=(), fetch=False):
        """Método privado para manejar la conexión y ejecución de SQL."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(query, params)
        res = cursor.fetchall() if fetch else None
        conn.commit()
        conn.close()
        return res

    def obtener_catalogos(self):
        """Obtiene la información para llenar las barras desplegables (Dropdowns)."""
        # Obtenemos datos de las tablas maestras creadas en la reingeniería [cite: 27, 29, 30]
        planes = self._ejecutar_query("SELECT clave_plan, descripcion FROM versiones_plan", fetch=True)
        carreras = self._ejecutar_query("SELECT clave, nombre FROM carreras", fetch=True)
        materias = self._ejecutar_query("SELECT clave, descri FROM materias", fetch=True)
        return planes, carreras, materias

    def leer_registros(self):
        """Consulta para mostrar la tabla con nombres legibles (Joins)."""
        query = """
            SELECT ep.id_registro, v.clave_plan, c.nombre, m.descri, ep.semestre
            FROM estructura_plan ep
            JOIN versiones_plan v ON ep.clave_plan = v.clave_plan
            JOIN carreras c ON ep.carrera_id = c.clave
            JOIN materias m ON ep.materia_id = m.clave
        """
        return self._ejecutar_query(query, fetch=True)

    def guardar_registro(self, plan, carrera, materia, semestre, rid=None):
        """Crea un nuevo registro o actualiza uno existente (Create/Update)."""
        if rid: # Si hay ID, es una actualización (UPDATE) [cite: 444]
            query = "UPDATE estructura_plan SET clave_plan=?, carrera_id=?, materia_id=?, semestre=? WHERE id_registro=?"
            params = (plan, carrera, materia, semestre, rid)
        else: # Si no hay ID, es una inserción nueva (INSERT) [cite: 445]
            query = "INSERT INTO estructura_plan (clave_plan, carrera_id, materia_id, semestre) VALUES (?, ?, ?, ?)"
            params = (plan, carrera, materia, semestre)
        self._ejecutar_query(query, params)

    def eliminar_registro(self, rid):
        """Elimina un registro específico (Delete)[cite: 446]."""
        self._ejecutar_query("DELETE FROM estructura_plan WHERE id_registro = ?", (rid,))

    def obtener_por_id(self, rid):
        """Recupera los datos de un solo registro para editarlos."""
        return self._ejecutar_query(
            "SELECT clave_plan, carrera_id, materia_id, semestre FROM estructura_plan WHERE id_registro=?", 
            (rid,), fetch=True
        )