select * from users order by user_id;

-- delete from users;


INSERT INTO users (email, password) --(title, content, published, created_at) 
VALUES 
	('manny@gmail.com', '$2b$12$xlsJDgir50/KKkKLyd5OK.MSPYSe0nC1/wmRb6xxbhi46SumbGOJq'),
	('andy@gmail.com', '$2b$12$.mDeWnNtR6yqIPUlfPGBMupiNDFK7X2VKmrmNehx1mXLzQkXBH2ya')

RETURNING *;


delete from users where user_id = 8;


show PORT;
-- ALTER SYSTEM SET port = '5433'; -- didn't work!!