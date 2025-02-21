-- Create indexes to improve query performance
CREATE INDEX ON reddit_posts (subreddit);
CREATE INDEX ON reddit_posts (post_id);
CREATE INDEX ON reddit_posts (created_utc);
