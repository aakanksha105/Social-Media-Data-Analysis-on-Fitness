-- Add the created_utc column to reddit_posts table
ALTER TABLE reddit_posts ADD COLUMN created_utc TIMESTAMP NOT NULL;
