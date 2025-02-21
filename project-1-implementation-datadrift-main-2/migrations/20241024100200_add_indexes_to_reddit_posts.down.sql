-- Drop the indexes from reddit_posts
DROP INDEX IF EXISTS reddit_posts_subreddit_idx;
DROP INDEX IF EXISTS reddit_posts_post_id_idx;
DROP INDEX IF EXISTS reddit_posts_created_utc_idx;
