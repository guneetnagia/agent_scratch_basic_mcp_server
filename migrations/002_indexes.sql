CREATE INDEX IF NOT EXISTS idx_ideas_fulltext
ON ideas
USING GIN (to_tsvector('english', title || ' ' || description));