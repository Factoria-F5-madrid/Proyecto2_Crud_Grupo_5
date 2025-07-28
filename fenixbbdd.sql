-- Tabla de categorías de productos
CREATE TABLE categorias (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion TEXT
);

-- Tabla de productos
CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    talla VARCHAR(10),
    color VARCHAR(30),
    precio NUMERIC(10,2) NOT NULL,
    stock INT DEFAULT 0,
    categoria_id INT NULL,
    creado_en TIMESTAMP DEFAULT now(),
    CONSTRAINT fk_categoria FOREIGN KEY (categoria_id) REFERENCES categorias(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

CREATE INDEX idx_categoria ON productos(categoria_id);
CREATE INDEX idx_nombre ON productos(nombre);

-- Tabla de clientes
CREATE TABLE clientes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo_electronico VARCHAR(100) NOT NULL UNIQUE,
    telefono VARCHAR(20),
    creado_en TIMESTAMP DEFAULT now()
);

CREATE INDEX idx_correo ON clientes(correo_electronico);

-- Tabla de pedidos (compras)
CREATE TABLE pedidos (
    id SERIAL PRIMARY KEY,
    cliente_id INT NOT NULL,
    fecha_pedido TIMESTAMP DEFAULT now(),
    CONSTRAINT fk_cliente FOREIGN KEY (cliente_id) REFERENCES clientes(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE INDEX idx_cliente ON pedidos(cliente_id);

-- Tabla de ítems por pedido
CREATE TABLE items_pedido (
    id SERIAL PRIMARY KEY,
    pedido_id INT NOT NULL,
    producto_id INT NOT NULL,
    cantidad INT DEFAULT 1 CHECK (cantidad > 0),
    CONSTRAINT fk_pedido FOREIGN KEY (pedido_id) REFERENCES pedidos(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_producto FOREIGN KEY (producto_id) REFERENCES productos(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE INDEX idx_pedido ON items_pedido(pedido_id);
CREATE INDEX idx_producto ON items_pedido(producto_id);
