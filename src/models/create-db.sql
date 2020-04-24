-- Create DB
CREATE DATABASE 'openff' DEFAULT CHARACTER SET 'utf8';
USE openff;

CREATE TABLE Categories (
    id int AUTO_INCREMENT NOT NULL,
    category_name varchar(500) NOT NULL UNIQUE,
    PRIMARY KEY (id)
) ENGINE=InnoDB;

CREATE TABLE Products(
	id int AUTO_INCREMENT NOT NULL,
	product_name text NOT NULL,
	brand varchar(100),
	barcode bigint NOT NULL UNIQUE,
	categories text NOT NULL,
	category_id int NOT NULL,
	nutrition_grades varchar(1) NOT NULL,
	stores text,
	substitute_id int,
	added_timestamp timestamp NOT NULL,
	updated_timestamp timestamp,
	CONSTRAINT fk_category_id
		FOREIGN KEY category_id REFERENCES Categories(id)
		ON DELETE CASCADE,
	CONSTRAINT fk_substitute_id
		FOREIGN KEY substitute_id REFERENCES Products(id)
		ON DELETE SET NULL,
	PRIMARY KEY (id)
) ENGINE=InnoDB;

