import sqlite3
import os

def ejecutar_reingenieria():
    db_name = 'baseDedatosIng.db'
    
    # Limpieza 
    if os.path.exists(db_name):
        os.remove(db_name)

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    #llaves foraneas en SQLite
    cursor.execute("PRAGMA foreign_keys = ON")
    
    print("Base de Datos creada")

    # TABLA 1: CARRERAS
    cursor.execute('''CREATE TABLE carreras (
                        clave TEXT PRIMARY KEY,
                        nombre TEXT NOT NULL)''')

    # TABLA 2: MATERIAS 
    cursor.execute('''CREATE TABLE materias (
                        clave TEXT PRIMARY KEY,
                        descri TEXT NOT NULL)''')

    # TABLA 3: VERSIONES_PLAN 
    cursor.execute('''CREATE TABLE versiones_plan (
                        clave_plan TEXT PRIMARY KEY,
                        descripcion TEXT)''')

    # TABLA 4
    cursor.execute('''CREATE TABLE estructura_plan (
                        id_registro INTEGER PRIMARY KEY AUTOINCREMENT,
                        clave_plan TEXT NOT NULL,
                        carrera_id TEXT NOT NULL,
                        materia_id TEXT NOT NULL,
                        semestre TEXT CHECK(semestre BETWEEN '01' AND '10'),
                        fecalt TEXT,
                        FOREIGN KEY (clave_plan) REFERENCES versiones_plan(clave_plan),
                        FOREIGN KEY (carrera_id) REFERENCES carreras(clave),
                        FOREIGN KEY (materia_id) REFERENCES materias(clave))''')

    # TABLA 5: PRERREQUISITOS
    # Permite que una materia tenga múltiples requisitos de forma escalable
    cursor.execute('''CREATE TABLE prerrequisitos (
                        id_registro_plan INTEGER NOT NULL,
                        materia_req_id TEXT NOT NULL,
                        FOREIGN KEY (id_registro_plan) REFERENCES estructura_plan(id_registro),
                        FOREIGN KEY (materia_req_id) REFERENCES materias(clave),
                        PRIMARY KEY (id_registro_plan, materia_req_id))''')

    # insertar datos
    
    # Datos de Carreras
    cursor.executemany("INSERT INTO carreras VALUES (?,?)", [
        ('05', 'ING. EN SIST COMPUTACIONALES EN SOFTWARE'),
        ('07', 'ING. EN SIST COMPUTACIONALES EN HARDWARE')
    ])

    # Datos de Materias
    cursor.executemany("INSERT INTO materias VALUES (?,?)", [
        ('101', 'ALGEBRA SUPERIOR'),
        ('102', 'MATEMATICAS I'),
        ('140', 'INTRODUCCION A LA COMPUTACION'),
        ('201', 'MATEMATICAS II')
    ])

    # Versiones de Plan
    cursor.execute("INSERT INTO versiones_plan VALUES (?,?)", ('A', 'Plan de Estudios 1991'))

    # Estructura del Plan
    # relaicon: Carrera-Materia-Plan
    cursor.execute("INSERT INTO estructura_plan (clave_plan, carrera_id, materia_id, semestre, fecalt) VALUES (?,?,?,?,?)",
                   ('A', '05', '201', '02', '1982-06-28'))
    
    ultimo_id = cursor.lastrowid # Obtenemos el ID generado para asignar requisitos

    # Prerrequisitos
    cursor.execute("INSERT INTO prerrequisitos VALUES (?,?)", (ultimo_id, '102'))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    ejecutar_reingenieria()