
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    telefono VARCHAR(15) UNIQUE NOT NULL,
    rol VARCHAR(50) NOT NULL
);

CREATE TABLE ejercicios (
    id SERIAL PRIMARY KEY,
    numero_ejercicio INTEGER UNIQUE NOT NULL,
    descripcion TEXT NOT NULL,
    repeticiones_base INTEGER NOT NULL,
    dificultad VARCHAR(20) NOT NULL,
    fecha_creacion TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);

CREATE TABLE sesion (
    id SERIAL PRIMARY KEY,
    fecha_creado TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
   
    id_ejercicio INTEGER NOT NULL,
    FOREIGN KEY (id_ejercicio) REFERENCES ejercicios (id),
    
    id_usuario INTEGER NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuarios (id),

    repeticiones_logradas INTEGER NOT NULL,
    maximo_nivel_logrado VARCHAR(50)
);