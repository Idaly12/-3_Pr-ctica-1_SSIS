/* Script para generación de diagrama ER en erwin Data Modeler */

CREATE TABLE carreras (
    clave           VARCHAR(10) NOT NULL,
    nombre          VARCHAR(100) NOT NULL,
    PRIMARY KEY (clave)
);

CREATE TABLE materias (
    clave           VARCHAR(10) NOT NULL,
    descri          VARCHAR(100) NOT NULL,
    PRIMARY KEY (clave)
);

CREATE TABLE planes (
    id              INTEGER PRIMARY KEY,
    clave_plan      CHAR(1) NOT NULL,
    carrera_id      VARCHAR(10) NOT NULL,
    materia_id      VARCHAR(10) NOT NULL,
    semestre        VARCHAR(2) NOT NULL,
    fecalt          DATE,
    requi1          VARCHAR(10),
    CONSTRAINT fk_plan_carrera FOREIGN KEY (carrera_id) REFERENCES carreras (clave),
    CONSTRAINT fk_plan_materia FOREIGN KEY (materia_id) REFERENCES materias (clave)
);