import sqlite3
import os

def ejecutar_reingenieria():
    db_name = 'baseDedatosIng.db'
    
    # 1. Limpieza preventiva: Si el archivo existe, lo borramos para crearlo de cero
    if os.path.exists(db_name):
        os.remove(db_name)
        print(f"--- Archivo anterior '{db_name}' eliminado para limpieza ---")

    # 2. Conexión e inicialización
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    print("--- Iniciando creación de tablas en 3FN ---")

    # --- TABLA CARRERAS (Basada en CARRERAS.DBF) ---
    cursor.execute('''
        CREATE TABLE carreras (
            clave TEXT PRIMARY KEY,
            nombre TEXT NOT NULL
        )
    ''')
    # Insertamos datos reales del archivo[cite: 3]
    carreras_datos = [
        ('05', 'ING. EN SIST COMPUTACIONALES EN SOFTWARE'),
        ('07', 'ING. EN SIST COMPUTACIONALES EN HARDWARE')
    ]
    cursor.executemany("INSERT INTO carreras VALUES (?,?)", carreras_datos)

    # --- TABLA MATERIAS (Basada en MATERIAS.DBF) ---
    cursor.execute('''
        CREATE TABLE materias (
            clave TEXT PRIMARY KEY,
            descri TEXT NOT NULL
        )
    ''')
    # Insertamos datos reales del archivo[cite: 4]
    materias_datos = [
        ('101', 'ALGEBRA SUPERIOR'),
        ('102', 'MATEMATICAS I'),
        ('103', 'FISICA I'),
        ('140', 'INTRODUCCION A LA COMPUTACION')
    ]
    cursor.executemany("INSERT INTO materias VALUES (?,?)", materias_datos)

    # --- TABLA PLANES (Reingeniería de ESC310 - 3FN) ---
    # Nota: Separamos la lógica de requisitos para cumplir con la normalización
    cursor.execute('''
        CREATE TABLE planes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            clave_plan TEXT NOT NULL,
            carrera_id TEXT NOT NULL,
            materia_id TEXT NOT NULL,
            semestre TEXT CHECK(semestre BETWEEN '01' AND '10'),
            fecalt TEXT,
            requi1 TEXT,
            FOREIGN KEY (carrera_id) REFERENCES carreras(clave),
            FOREIGN KEY (materia_id) REFERENCES materias(clave)
        )
    ''')
    
    # Insertamos algunos registros de ejemplo basados en PLANES.DBF[cite: 5]
    planes_datos = [
        ('A', '01', '101', '01', '1982-06-24', None),
        ('A', '01', '102', '01', '1982-06-25', None),
        ('A', '01', '201', '02', '1982-06-28', '102')
    ]
    cursor.executemany('''
        INSERT INTO planes (clave_plan, carrera_id, materia_id, semestre, fecalt, requi1) 
        VALUES (?,?,?,?,?,?)
    ''', planes_datos)

    conn.commit()
    conn.close()
    print(f"--- Proceso terminado: '{db_name}' está lista para revisarse ---")

if __name__ == "__main__":
    ejecutar_reingenieria()