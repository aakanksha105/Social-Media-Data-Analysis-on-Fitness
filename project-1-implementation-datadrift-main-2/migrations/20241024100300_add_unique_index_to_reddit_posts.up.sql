-- Create a unique index to ensure no duplicate posts are inserted
CREATE UNIQUE INDEX ON reddit_posts (subreddit, post_id);
