CREATE TABLE IF NOT EXISTS marcas (
  id           BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  nombre       VARCHAR(100)    NOT NULL,
  pais_origen  VARCHAR(100)    NULL,
  estado       TINYINT(1)      NOT NULL DEFAULT 1,
  creado       TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  actualizado  TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_marcas_nombre (nombre)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS modelos (
  id           BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  marca_id     BIGINT UNSIGNED NOT NULL,
  nombre       VARCHAR(100)    NOT NULL,
  tipo         VARCHAR(50)     NULL,
  estado       TINYINT(1)      NOT NULL DEFAULT 1,
  creado       TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  actualizado  TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_modelos_marca_nombre (marca_id, nombre),
  CONSTRAINT fk_modelos_marca FOREIGN KEY (marca_id) REFERENCES marcas (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS versiones (
  id           BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  modelo_id    BIGINT UNSIGNED NOT NULL,
  anio         SMALLINT UNSIGNED NOT NULL,
  cilindraje   SMALLINT UNSIGNED NOT NULL,
  estado       TINYINT(1)      NOT NULL DEFAULT 1,
  creado       TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  actualizado  TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_versiones_modelo_anio_cc (modelo_id, anio, cilindraje),
  CONSTRAINT fk_versiones_modelo FOREIGN KEY (modelo_id) REFERENCES modelos (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
