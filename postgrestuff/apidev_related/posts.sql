select * from posts;

select * from posts order by post_id;

INSERT INTO posts (title, content, published, created_at) 
VALUES 
    ('First Post', 'This is the content of the first post.', true, '2024-06-01 10:00:00+00'),
    ('Second Post', 'This is the content of the second post.', false, '2024-06-02 11:00:00+00'),
    ('Third Post', 'Content for the third post goes here.', true, '2024-06-03 12:00:00+00'),
    ('Fourth Post', 'Fourth post content is quite interesting.', true, '2024-06-04 13:00:00+00'),
    ('Fifth Post', 'Here is the content for the fifth post.', false, '2024-06-05 14:00:00+00')
RETURNING *;


delete from posts;

delete from posts where post_id > 10;

INSERT INTO posts (post_title, post_content, creator_id) 
VALUES 
	('third post', 'post 3 content', 10)
RETURNING *;






















