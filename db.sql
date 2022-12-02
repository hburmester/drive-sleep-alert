drop database  proyecto_cognitive;
create database proyecto_cognitive;
use proyecto_cognitive;
create table centrales(
	cod int primary key auto_increment,
	nombre_central varchar(20) unique not null,
	telefono int(9) not null,
	direccion varchar(50) not null,
	clave varchar(12) not null,
	suma_incidencias int not null
);
insert into centrales (nombre, telefono, direccion, clave, suma_incidencias) values('Prosegur', 987678654, 'Av. Velasco Astete 212', 'seguridad1', 0);
insert into centrales (nombre, telefono, direccion, clave, suma_incidencias) values('Primax', 921321321, 'Paseo de la república 130', 'seguridad2', 0);
insert into centrales (nombre, telefono, direccion, clave, suma_incidencias) values('Mapfre', 921325621, 'Paseo de la república 240', 'seguridad3', 0);

create table conductores(
	id_conductor int primary key auto_increment,
	nombre varchar(20) not null,
	apellido varchar(20) not null,
	edad int not null,
	cantidad_incidencias int not null,
	estatus_conductor int not null,
    placa_camion varchar(7) not null,
	nombre_central varchar(20) not null
);

create table incidencias(
	id_incidencia int primary key auto_increment,
	latitud float(10) not null,
	longitud float(10) not null,
	nombre varchar(20) not null,
	apellido varchar(20) not null,
	hora_infraccion varchar(20) not null,
	placa_camion varchar(7) not null
);
