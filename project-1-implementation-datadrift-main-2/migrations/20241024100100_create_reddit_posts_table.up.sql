-- Create the reddit_posts table
CREATE TABLE reddit_posts (
    id BIGSERIAL PRIMARY KEY,  -- Unique identifier for each post
    subreddit TEXT NOT NULL,  -- The name of the subreddit
    post_id TEXT NOT NULL,  -- The unique ID of the post from Reddit
    title TEXT NOT NULL,  -- The title of the Reddit post
    content TEXT,  -- The content of the post (may be empty for link posts)
    created_utc TIMESTAMP NOT NULL  -- When the post was created (from Reddit)
);
