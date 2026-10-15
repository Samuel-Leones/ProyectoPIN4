CREATE TABLE categorias (
	id BIGSERIAL NOT NULL, 
	nombre VARCHAR(255) NOT NULL, 
	descripcion VARCHAR(255), 
	estado BOOLEAN DEFAULT true NOT NULL, 
	creado TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	actualizado TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	PRIMARY KEY (id)
);
CREATE UNIQUE INDEX uq_categorias_nombre_activo ON categorias (nombre) WHERE estado;

CREATE TABLE clientes (
	id BIGSERIAL NOT NULL, 
	nombre VARCHAR(255) NOT NULL, 
	documento VARCHAR(255) NOT NULL, 
	telefono VARCHAR(255), 
	correo VARCHAR(255), 
	direccion VARCHAR(255), 
	estado BOOLEAN DEFAULT true NOT NULL, 
	creado TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	actualizado TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	PRIMARY KEY (id)
);
CREATE UNIQUE INDEX uq_clientes_documento_activo ON clientes (documento) WHERE estado;

CREATE TABLE modulos (
	id BIGSERIAL NOT NULL, 
	nombre VARCHAR(100) NOT NULL, 
	descripcion VARCHAR(255), 
	ruta VARCHAR(100) NOT NULL, 
	icono VARCHAR(50), 
	estado BOOLEAN DEFAULT true NOT NULL, 
	creado TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	actualizado TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (nombre), 
	UNIQUE (ruta)
);

CREATE TABLE proveedores (
	id BIGSERIAL NOT NULL, 
	nombre VARCHAR(255) NOT NULL, 
	nombre_contacto VARCHAR(255), 
	telefono VARCHAR(255), 
	correo VARCHAR(255), 
	estado BOOLEAN DEFAULT true NOT NULL, 
	creado TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	actualizado TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	PRIMARY KEY (id)
);
CREATE UNIQUE INDEX uq_proveedores_nombre_activo ON proveedores (nombre) WHERE estado;

CREATE TABLE registros_auditoria (
	id BIGSERIAL NOT NULL, 
	usuario_id BIGINT NOT NULL, 
	correo_usuario VARCHAR(255) NOT NULL, 
	accion VARCHAR(20) NOT NULL, 
	entidad_afectada VARCHAR(255) NOT NULL, 
	id_entidad_afectada BIGINT NOT NULL, 
	estado BOOLEAN DEFAULT true NOT NULL, 
	creado TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	actualizado TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	PRIMARY KEY (id)
);

CREATE TABLE roles (
	id BIGSERIAL NOT NULL, 
	nombre VARCHAR(50) NOT NULL, 
	descripcion VARCHAR(255), 
	estado BOOLEAN DEFAULT true NOT NULL, 
	creado TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	actualizado TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (nombre)
);

CREATE TABLE modulo_x_rol (
	id BIGSERIAL NOT NULL, 
	rol_id BIGINT NOT NULL, 
	modulo_id BIGINT NOT NULL, 
	puede_crear BOOLEAN DEFAULT false NOT NULL, 
	puede_editar BOOLEAN DEFAULT false NOT NULL, 
	puede_eliminar BOOLEAN DEFAULT false NOT NULL, 
	estado BOOLEAN DEFAULT true NOT NULL, 
	creado TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	actualizado TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT uq_modulo_x_rol UNIQUE (rol_id, modulo_id), 
	FOREIGN KEY(rol_id) REFERENCES roles (id), 
	FOREIGN KEY(modulo_id) REFERENCES modulos (id)
);

CREATE TABLE productos (
	id BIGSERIAL NOT NULL, 
	nombre VARCHAR(255) NOT NULL, 
	descripcion VARCHAR(255), 
	codigo VARCHAR(255) NOT NULL, 
	categoria_id BIGINT NOT NULL, 
	proveedor_id BIGINT, 
	precio NUMERIC(38, 2) NOT NULL, 
	stock_actual INTEGER NOT NULL, 
	stock_minimo INTEGER NOT NULL, 
	estado BOOLEAN DEFAULT true NOT NULL, 
	creado TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	actualizado TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (codigo), 
	FOREIGN KEY(categoria_id) REFERENCES categorias (id), 
	FOREIGN KEY(proveedor_id) REFERENCES proveedores (id)
);

CREATE TABLE usuarios (
	id BIGSERIAL NOT NULL, 
	correo VARCHAR(255) NOT NULL, 
	nombre_completo VARCHAR(255) NOT NULL, 
	contrasena VARCHAR(255) NOT NULL, 
	rol_id BIGINT NOT NULL, 
	estado BOOLEAN DEFAULT true NOT NULL, 
	creado TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	actualizado TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (correo), 
	FOREIGN KEY(rol_id) REFERENCES roles (id)
);

CREATE TABLE movimientos_inventario (
	id BIGSERIAL NOT NULL, 
	producto_id BIGINT NOT NULL, 
	tipo VARCHAR(20) NOT NULL, 
	cantidad INTEGER NOT NULL, 
	motivo VARCHAR(255), 
	usuario_id BIGINT NOT NULL, 
	estado BOOLEAN DEFAULT true NOT NULL, 
	creado TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	actualizado TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(producto_id) REFERENCES productos (id), 
	FOREIGN KEY(usuario_id) REFERENCES usuarios (id)
);

CREATE TABLE productos_compatibilidad (
	id BIGSERIAL NOT NULL, 
	producto_id BIGINT NOT NULL, 
	version_moto_id BIGINT NOT NULL, 
	descripcion_moto VARCHAR(255) NOT NULL, 
	estado BOOLEAN DEFAULT true NOT NULL, 
	creado TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	actualizado TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT uq_producto_version_moto UNIQUE (producto_id, version_moto_id), 
	FOREIGN KEY(producto_id) REFERENCES productos (id)
);
CREATE INDEX ix_productos_compatibilidad_version_moto ON productos_compatibilidad (version_moto_id);

CREATE TABLE ventas (
	id BIGSERIAL NOT NULL, 
	cliente_id BIGINT NOT NULL, 
	usuario_id BIGINT NOT NULL, 
	subtotal NUMERIC(38, 2) NOT NULL, 
	iva NUMERIC(38, 2) NOT NULL, 
	total NUMERIC(38, 2) NOT NULL, 
	estado_venta VARCHAR(20) NOT NULL, 
	estado BOOLEAN DEFAULT true NOT NULL, 
	creado TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	actualizado TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(cliente_id) REFERENCES clientes (id), 
	FOREIGN KEY(usuario_id) REFERENCES usuarios (id)
);

CREATE TABLE detalles_venta (
	id BIGSERIAL NOT NULL, 
	venta_id BIGINT NOT NULL, 
	producto_id BIGINT NOT NULL, 
	cantidad INTEGER NOT NULL, 
	precio_unitario NUMERIC(38, 2) NOT NULL, 
	estado BOOLEAN DEFAULT true NOT NULL, 
	creado TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	actualizado TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(venta_id) REFERENCES ventas (id), 
	FOREIGN KEY(producto_id) REFERENCES productos (id)
);

CREATE TABLE facturas (
	id BIGSERIAL NOT NULL, 
	venta_id BIGINT NOT NULL, 
	numero_factura VARCHAR(255) NOT NULL, 
	estado BOOLEAN DEFAULT true NOT NULL, 
	creado TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	actualizado TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (venta_id), 
	FOREIGN KEY(venta_id) REFERENCES ventas (id), 
	UNIQUE (numero_factura)
);

CREATE OR REPLACE FUNCTION fn_actualizar_campo_actualizado() RETURNS trigger AS $$
BEGIN
    NEW.actualizado = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_categorias_actualizado BEFORE UPDATE ON "categorias" FOR EACH ROW EXECUTE FUNCTION fn_actualizar_campo_actualizado();
CREATE TRIGGER trg_clientes_actualizado BEFORE UPDATE ON "clientes" FOR EACH ROW EXECUTE FUNCTION fn_actualizar_campo_actualizado();
CREATE TRIGGER trg_modulos_actualizado BEFORE UPDATE ON "modulos" FOR EACH ROW EXECUTE FUNCTION fn_actualizar_campo_actualizado();
CREATE TRIGGER trg_proveedores_actualizado BEFORE UPDATE ON "proveedores" FOR EACH ROW EXECUTE FUNCTION fn_actualizar_campo_actualizado();
CREATE TRIGGER trg_registros_auditoria_actualizado BEFORE UPDATE ON "registros_auditoria" FOR EACH ROW EXECUTE FUNCTION fn_actualizar_campo_actualizado();
CREATE TRIGGER trg_roles_actualizado BEFORE UPDATE ON "roles" FOR EACH ROW EXECUTE FUNCTION fn_actualizar_campo_actualizado();
CREATE TRIGGER trg_modulo_x_rol_actualizado BEFORE UPDATE ON "modulo_x_rol" FOR EACH ROW EXECUTE FUNCTION fn_actualizar_campo_actualizado();
CREATE TRIGGER trg_productos_actualizado BEFORE UPDATE ON "productos" FOR EACH ROW EXECUTE FUNCTION fn_actualizar_campo_actualizado();
CREATE TRIGGER trg_usuarios_actualizado BEFORE UPDATE ON "usuarios" FOR EACH ROW EXECUTE FUNCTION fn_actualizar_campo_actualizado();
CREATE TRIGGER trg_movimientos_inventario_actualizado BEFORE UPDATE ON "movimientos_inventario" FOR EACH ROW EXECUTE FUNCTION fn_actualizar_campo_actualizado();
CREATE TRIGGER trg_productos_compatibilidad_actualizado BEFORE UPDATE ON "productos_compatibilidad" FOR EACH ROW EXECUTE FUNCTION fn_actualizar_campo_actualizado();
CREATE TRIGGER trg_ventas_actualizado BEFORE UPDATE ON "ventas" FOR EACH ROW EXECUTE FUNCTION fn_actualizar_campo_actualizado();
CREATE TRIGGER trg_detalles_venta_actualizado BEFORE UPDATE ON "detalles_venta" FOR EACH ROW EXECUTE FUNCTION fn_actualizar_campo_actualizado();
CREATE TRIGGER trg_facturas_actualizado BEFORE UPDATE ON "facturas" FOR EACH ROW EXECUTE FUNCTION fn_actualizar_campo_actualizado();
