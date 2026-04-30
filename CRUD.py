import sqlite3
import os

class DatabaseManager:
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(__file__), "baseDedatosIng.db")

    def _ejecutar_query(self, query, params=(), fetch=False):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(query, params) 
        res = cursor.fetchall() if fetch else None
        conn.commit()
        conn.close()
        return res

    def obtener_catalogos(self):
        planes = self._ejecutar_query("SELECT clave_plan, descripcion FROM versiones_plan", fetch=True)
        carreras = self._ejecutar_query("SELECT clave, nombre FROM carreras", fetch=True)
        materias = self._ejecutar_query("SELECT clave, descri FROM materias", fetch=True)
        return planes, carreras, materias

    def leer_registros(self):
        query = """
            SELECT ep.id_registro, v.clave_plan, c.nombre, m.descri, ep.semestre, ep.fecalt, ep.fecbaj
            FROM estructura_plan ep
            JOIN versiones_plan v ON ep.clave_plan = v.clave_plan
            JOIN carreras c ON ep.carrera_id = c.clave
            JOIN materias m ON ep.materia_id = m.clave
        """
        return self._ejecutar_query(query, fetch=True)

    def guardar_registro(self, plan, carrera, materia, semestre, falt, fbaj, rid=None):
        if rid:
            query = "UPDATE estructura_plan SET clave_plan=?, carrera_id=?, materia_id=?, semestre=?, fecalt=?, fecbaj=? WHERE id_registro=?"
            params = (plan, carrera, materia, semestre, falt, fbaj, rid)
        else:
            query = "INSERT INTO estructura_plan (clave_plan, carrera_id, materia_id, semestre, fecalt, fecbaj) VALUES (?,?,?,?,?,?)"
            params = (plan, carrera, materia, semestre, falt, fbaj)
        self._ejecutar_query(query, params)

    def eliminar_registro(self, rid):
        if rid:
            self._ejecutar_query("DELETE FROM estructura_plan WHERE id_registro = ?", (rid,))

    def obtener_por_id(self, rid):
        return self._ejecutar_query(
            "SELECT clave_plan, carrera_id, materia_id, semestre, fecalt, fecbaj FROM estructura_plan WHERE id_registro=?", 
            (rid,), fetch=True
        )