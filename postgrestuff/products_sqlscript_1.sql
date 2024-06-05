select * from products;

select name, price from products;
select id from products;

select name as Product_name, price as Product_price from products;

select * from products where id > 2;
select * from products where id > 0 and price < 2000;
select * from products where id > 0 and price < 2000;
select * from products where inventory = 0 or price < 2000;
select * from products where products.inventory = 0 or products.price > 2000;
select * from products where inventory != 0;
select * from products where inventory <> 0; -- "less than and greater than 0"

select * from products where name = 'Wine';
-- Regex in PostgreSQL:
select * from products where name ~ '^W';
select * from products where name ~ 'ne$';
-- xxx select * from products where name ~ '^W..$';



-- way 1:
select * from products where id = 1 or id = 3 or id = 5;
-- alt(better):
select * from products where id in (1, 3, 5);



-- 'LIKE' keyword:
----------------------------------------------
-- starting from 'TV'
select * from products where name LIKE 'TV%';
-- ending with 'e'
select * from products where name LIKE '%e';
-- having 'el' in between a string
select * from products where name LIKE '%el%';
----------------------------------------------


-- 'ORDER BY'
select * from products ORDER BY id;
select * from products ORDER BY id ASC; -- 'assending' order
select * from products ORDER BY id DESC; -- 'descending' order
select * from products order by inventory asc;

-- whenever there is a tie in inventory -> go order by price
select * from products order by inventory desc, price desc;
select * from products order by inventory desc, price asc; 
-- also 'asc' is the 'default' if nothing mentioned of 'desc' and 'asc':
select * from products order by inventory , price;

-- 'order' by 'created_time'
select * from products order by created_at;
select * from products order by created_at desc; -- recent comes first here..
-- where and order by:
select * from products where price > 100 order by created_at desc;

-- limiting number of rows: 
select * from products LIMIT 4; -- 4 rows
select * from products where price > 100 order by created_at desc LIMIT 5; -- 5 rows	
select * from products where price > 100 limit 3;


-- 
select * from products order by id limit 4;
-- skipping fast the first 2 of the above query:
select * from products order by id limit 4 offset 2; -- ❌
select * from products order by id limit 2 offset 2; -- ✅

select * from products order by id limit 4 offset 1; -- ❌
select * from products order by id limit 3 offset 1; -- ✅

-- Inserting Data into TABLE:
insert into products (name, price, inventory) values ('Keyboard MG250', 235, 5);
select * from products;

-- 'returning' keyword: Returning after insertion
------------------------------------------------------------------------------------------------
-- returning all cols:
insert into products (name, price, inventory) values ('Tesla CyberTruck', 100235, 5) returning *;
-- returning specific cols after insertion:
insert into products (name, price, inventory) values ('PS5', 10235, 5) returning name as "Product Name", price, inventory;
------------------------------------------------------------------------------------------------


-- inserting multiple rows
insert into products (name, price, inventory) values 
	('KTM Duke', 16235, 15), 
	('KTM RC', 26235, 5)
	returning *;



-- Deleting Entry:
select * from products;

delete from products where id = 16;
select * from products;

-- deleting and returning the deleted item:
delete from products where id = 9 returning *;

-- deleting rows based on a criteria:
delete from products where inventory < 0 returning *;

select * from products;

delete from products where inventory = 0 returning *;

select * from products;


-- Updating:
update products set name = 'Whiskey', price = 2000, inventory = 80 where id = 1 returning *;

select * from products order by id;

-- setting 'is_sale' for all to 'true'
update products set is_sale = true where id > 0 returning * ;









