CREATE DATABASE openff DEFAULT CHARACTER SET utf8;
USE openff;
CREATE TABLE Categories (
    id int AUTO_INCREMENT NOT NULL,
    category_name varchar(500) NOT NULL,
    UNIQUE (category_name),
    PRIMARY KEY (id)
);
CREATE TABLE Products(
	id int AUTO_INCREMENT NOT NULL,
	product_name text NOT NULL,
	brands text,
	code bigint NOT NULL,
	categories text NOT NULL,
	nutrition_grades varchar(1) NOT NULL,
	stores text,
	substitute_id int,
	url text NOT NULL,
	added_timestamp int NOT NULL,
	updated_timestamp int,
	CONSTRAINT fk_substitute_id
		FOREIGN KEY (substitute_id) REFERENCES Products(id)
		ON DELETE SET NULL,
	UNIQUE (code),
	PRIMARY KEY (id)
);
CREATE TABLE Prod_in_Cat(
	category_id int NOT NULL,
	product_id int NOT NULL,
	CONSTRAINT fk_category_id
		FOREIGN KEY (category_id) REFERENCES Categories(id)
		ON DELETE CASCADE,
	CONSTRAINT fk_product_id
		FOREIGN KEY (product_id) REFERENCES Products(id)
		ON DELETE CASCADE,
	PRIMARY KEY (category_id, product_id)
);