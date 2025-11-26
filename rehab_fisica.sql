
CREATE TABLE usuarios (
    id VARCHAR(200) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    telefono VARCHAR(15) UNIQUE NOT NULL,
    rol VARCHAR(50) NOT NULL,
	contrasena VARCHAR(200) NOT NULL
);

CREATE TABLE ejercicios (
    id VARCHAR(200) PRIMARY KEY,
    numero_ejercicio INTEGER UNIQUE NOT NULL,
    descripcion TEXT NOT NULL,
    repeticiones_base INTEGER NOT NULL,
    dificultad VARCHAR(20) NOT NULL,
    fecha_creacion TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);

CREATE TABLE sesion (
    id VARCHAR(200)  PRIMARY KEY,
    fecha_creado TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
   
    id_ejercicio VARCHAR(200) NOT NULL,
    FOREIGN KEY (id_ejercicio) REFERENCES ejercicios (id),
    
    id_usuario VARCHAR(200)  NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuarios (id),

    repeticiones_logradas VARCHAR(200) NOT NULL,
    maximo_nivel_logrado VARCHAR(50)
);

ALTER TABLE sesion
ADD COLUMN fecha_termino TIMESTAMP WITHOUT TIME ZONE DEFAULT NULL;