import sqlite3
import os

def ejecutar_reingenieria():
    db_name = 'baseDedatosIng.db'
    
    # IMPORTANTE: Borra el archivo viejo para que se cree con la nueva columna
    if os.path.exists(db_name):
        os.remove(db_name)

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    
    # Creación de tablas según el diseño de reingeniería
    cursor.execute('CREATE TABLE carreras (clave TEXT PRIMARY KEY, nombre TEXT NOT NULL)')
    cursor.execute('CREATE TABLE materias (clave TEXT PRIMARY KEY, descri TEXT NOT NULL)')
    cursor.execute('CREATE TABLE versiones_plan (clave_plan TEXT PRIMARY KEY, descripcion TEXT)')

    # Tabla estructura_plan con fecalt y fecbaj 
    cursor.execute('''CREATE TABLE estructura_plan (
                        id_registro INTEGER PRIMARY KEY AUTOINCREMENT,
                        clave_plan TEXT NOT NULL,
                        carrera_id TEXT NOT NULL,
                        materia_id TEXT NOT NULL,
                        semestre TEXT CHECK(semestre BETWEEN '01' AND '10'),
                        fecalt TEXT,
                        fecbaj TEXT, 
                        FOREIGN KEY (clave_plan) REFERENCES versiones_plan(clave_plan),
                        FOREIGN KEY (carrera_id) REFERENCES carreras(clave),
                        FOREIGN KEY (materia_id) REFERENCES materias(clave))''')

    cursor.execute('''CREATE TABLE prerrequisitos (
                        id_registro_plan INTEGER NOT NULL,
                        materia_req_id TEXT NOT NULL,
                        FOREIGN KEY (id_registro_plan) REFERENCES estructura_plan(id_registro),
                        FOREIGN KEY (materia_req_id) REFERENCES materias(clave),
                        PRIMARY KEY (id_registro_plan, materia_req_id))''')

    # Datos maestros iniciales
    cursor.executemany("INSERT INTO carreras VALUES (?,?)", [
        ('05', 'ING. EN SIST COMPUTACIONALES EN SOFTWARE'),
        ('07', 'ING. EN SIST COMPUTACIONALES EN HARDWARE')])

    cursor.executemany("INSERT INTO materias VALUES (?,?)", [
        ('101', 'ALGEBRA SUPERIOR'), ('202', 'AlGEBRA LINEAL'),
        ('105', 'INTRODUCCION A LA COMPUTACION'), ('205', 'PROGRAMACION ORIENTADA A OBJETOS'),('301', 'ESTRUCTURA DE DATOS'),
        ('401', 'ESTRUCTURA DE DATOS AVANZADA')])

    cursor.executemany("INSERT INTO versiones_plan VALUES (?,?)", [('A', 'Plan de Estudios 1991'), ('B', 'Plan de Estudios 2016')])

    conn.commit()
    conn.close()

if __name__ == "__main__":
    ejecutar_reingenieria()