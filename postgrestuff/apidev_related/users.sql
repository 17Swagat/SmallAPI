select * from users order by user_id;

-- delete from users;


INSERT INTO users (email, password) --(title, content, published, created_at) 
VALUES 
	('jonny@gmail.com', '$2b$12$ZD7Vvpeda2rxsOrwiOYLNeK7UfXzs1xkbAxKAERF5VZ.X8TGeLnye'),
	('andy@gmail.com', '$2b$12$.mDeWnNtR6yqIPUlfPGBMupiNDFK7X2VKmrmNehx1mXLzQkXBH2ya')

RETURNING *;



