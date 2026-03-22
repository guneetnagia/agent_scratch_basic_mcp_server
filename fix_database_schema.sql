-- Enable pgvector
CREATE EXTENSION IF NOT EXISTS vector;

-- Create correct ideas table
CREATE TABLE IF NOT EXISTS ideas (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,

    contributor TEXT,
    submitter_email TEXT,
    department TEXT,

    business_value TEXT,
    technical_requirements TEXT,

    status TEXT DEFAULT 'Under Review',
    admin_notes TEXT,

    submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    vector_embedding VECTOR(384)
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_ideas_status ON ideas(status);
CREATE INDEX IF NOT EXISTS idx_ideas_department ON ideas(department);

-- Vector index (important for semantic search)
CREATE INDEX IF NOT EXISTS idx_ideas_vector_embedding 
ON ideas USING ivfflat (vector_embedding vector_cosine_ops)
WITH (lists = 100);