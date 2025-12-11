-- Script para poblar datos de prueba
-- Contraseña para todas las cuentas: 123456

-- 1. Insertar Roles
INSERT INTO roles (nombre, descripcion, estado, created_at, updated_at) 
VALUES 
('admin', 'Administrador del sistema', 'activo', NOW(), NOW()),
('usuario', 'Usuario estandar del sistema', 'activo', NOW(), NOW());

-- 2. Insertar Cuentas (1 Admin, 4 Usuarios)
INSERT INTO cuentas (usuario, contrasena, email, rol_id, estado, fecha_creacion, created_at, updated_at) 
VALUES
('admin', 'scrypt:32768:8:1$Knlif8ghpqQHMO6C$47a0fdc5a0f00f153598feafa3198d350e74837bf885db4f9792141530af55c07bd4db3973ff6262d37929818da570759a08a18a97e27ef3dabd93a9f8174286', 'admin@sistema.com', (SELECT id FROM roles WHERE nombre='admin' LIMIT 1), 'activo', NOW(), NOW(), NOW()),
('juan.perez', 'scrypt:32768:8:1$Knlif8ghpqQHMO6C$47a0fdc5a0f00f153598feafa3198d350e74837bf885db4f9792141530af55c07bd4db3973ff6262d37929818da570759a08a18a97e27ef3dabd93a9f8174286', 'juan.perez@usuario.com', (SELECT id FROM roles WHERE nombre='usuario' LIMIT 1), 'activo', NOW(), NOW(), NOW()),
('maria.gomez', 'scrypt:32768:8:1$Knlif8ghpqQHMO6C$47a0fdc5a0f00f153598feafa3198d350e74837bf885db4f9792141530af55c07bd4db3973ff6262d37929818da570759a08a18a97e27ef3dabd93a9f8174286', 'maria.gomez@usuario.com', (SELECT id FROM roles WHERE nombre='usuario' LIMIT 1), 'activo', NOW(), NOW(), NOW()),
('carlos.mamani', 'scrypt:32768:8:1$Knlif8ghpqQHMO6C$47a0fdc5a0f00f153598feafa3198d350e74837bf885db4f9792141530af55c07bd4db3973ff6262d37929818da570759a08a18a97e27ef3dabd93a9f8174286', 'carlos.mamani@usuario.com', (SELECT id FROM roles WHERE nombre='usuario' LIMIT 1), 'activo', NOW(), NOW(), NOW()),
('ana.lopez', 'scrypt:32768:8:1$Knlif8ghpqQHMO6C$47a0fdc5a0f00f153598feafa3198d350e74837bf885db4f9792141530af55c07bd4db3973ff6262d37929818da570759a08a18a97e27ef3dabd93a9f8174286', 'ana.lopez@usuario.com', (SELECT id FROM roles WHERE nombre='usuario' LIMIT 1), 'activo', NOW(), NOW(), NOW());

-- 3. Insertar Ciudadanos (10 registros con ubicaciones en La Paz)
INSERT INTO ciudadanos (nombre, apellido, ci, telefono, email, direccion, latitud, longitud, fecha_nacimiento, estado, created_at, updated_at) 
VALUES
('Juan', 'Quispe', '1234567 LP', '70011111', 'juan.quispe@ciudadano.com', 'Av. Mariscal Santa Cruz, Centro', -16.4950, -68.1360, '1985-04-12', 'activo', NOW(), NOW()),
('Maria', 'Flores', '2345678 LP', '70022222', 'maria.flores@ciudadano.com', 'Calle Sagarnaga', -16.4970, -68.1375, '1990-08-25', 'activo', NOW(), NOW()),
('Pedro', 'Choque', '3456789 LP', '70033333', 'pedro.choque@ciudadano.com', 'Av. 6 de Agosto, Sopocachi', -16.5060, -68.1300, '1982-11-05', 'activo', NOW(), NOW()),
('Lucia', 'Vargas', '4567890 LP', '70044444', 'lucia.vargas@ciudadano.com', 'Plaza Abaroa', -16.5100, -68.1290, '1995-02-15', 'activo', NOW(), NOW()),
('Carlos', 'Gutierrez', '5678901 LP', '70055555', 'carlos.gutierrez@ciudadano.com', 'Av. Arce, San Jorge', -16.5150, -68.1250, '1988-06-30', 'activo', NOW(), NOW()),
('Ana', 'Mendoza', '6789012 LP', '70066666', 'ana.mendoza@ciudadano.com', 'Estadio Hernando Siles, Miraflores', -16.4980, -68.1230, '1992-09-18', 'activo', NOW(), NOW()),
('Jorge', 'Silva', '7890123 LP', '70077777', 'jorge.silva@ciudadano.com', 'Plaza Villarroel', -16.4880, -68.1150, '1980-12-01', 'activo', NOW(), NOW()),
('Sofia', 'Ramos', '8901234 LP', '70088888', 'sofia.ramos@ciudadano.com', 'Av. Camacho', -16.4990, -68.1330, '1998-03-22', 'activo', NOW(), NOW()),
('Miguel', 'Condori', '9012345 LP', '70099999', 'miguel.condori@ciudadano.com', 'Calle Jaen, Casco Viejo', -16.4920, -68.1350, '1986-07-07', 'activo', NOW(), NOW()),
('Elena', 'Cruz', '0123456 LP', '70000000', 'elena.cruz@ciudadano.com', 'El Prado', -16.5020, -68.1340, '1993-10-10', 'activo', NOW(), NOW());

-- 4. Insertar Zona (Polígono que cubre a tods los ciudadanos)
-- Coordenadas Bounding Box: 
-- Norte: -16.4800, Sur: -16.5200, Este: -68.1100, Oeste: -68.1400
INSERT INTO zonas (nombre, poligono_geojson, descripcion, tipo, estado, created_at, updated_at)
VALUES
('Zona Central La Paz', 
 '{"type": "Polygon", "coordinates": [[[-68.1400, -16.5200], [-68.1100, -16.5200], [-68.1100, -16.4800], [-68.1400, -16.4800], [-68.1400, -16.5200]]]}', 
 'Zona de cobertura principal que abarca el centro de La Paz, Sopocachi, Miraflores y alrededores.',
 'residencial', 
 'activo', 
 NOW(), 
 NOW());
