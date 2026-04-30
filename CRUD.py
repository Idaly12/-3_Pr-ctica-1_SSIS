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

    def guardar_registro(self, plan, carrera, materia, semestre, falt, fecbaj, requisitos_ids=None, rid=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if rid:
            query = "UPDATE estructura_plan SET clave_plan=?, carrera_id=?, materia_id=?, semestre=?, fecalt=?, fecbaj=? WHERE id_registro=?"
            cursor.execute(query, (plan, carrera, materia, semestre, falt, fecbaj, rid))
            cursor.execute("DELETE FROM prerrequisitos WHERE id_registro_plan = ?", (rid,))
            id_plan = rid
        else:
            query = "INSERT INTO estructura_plan (clave_plan, carrera_id, materia_id, semestre, fecalt, fecbaj) VALUES (?,?,?,?,?,?)"
            cursor.execute(query, (plan, carrera, materia, semestre, falt, fecbaj))
            id_plan = cursor.lastrowid

        if requisitos_ids:
            for req_id in requisitos_ids:
                cursor.execute("INSERT INTO prerrequisitos (id_registro_plan, materia_req_id) VALUES (?,?)", (id_plan, req_id))
        
        conn.commit()
        conn.close()

    def eliminar_registro(self, rid):
        if rid:
            self._ejecutar_query("DELETE FROM prerrequisitos WHERE id_registro_plan = ?", (rid,))
            self._ejecutar_query("DELETE FROM estructura_plan WHERE id_registro = ?", (rid,))

    def obtener_por_id(self, rid):
        return self._ejecutar_query(
            "SELECT clave_plan, carrera_id, materia_id, semestre, fecalt, fecbaj FROM estructura_plan WHERE id_registro=?", 
            (rid,), fetch=True
        )

    def obtener_requisitos_por_id(self, rid):
        query = "SELECT materia_req_id FROM prerrequisitos WHERE id_registro_plan = ?"
        res = self._ejecutar_query(query, (rid,), fetch=True)
        return [r[0] for r in res] if res else []