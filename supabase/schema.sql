-- Italian Teacher Assistant Database Schema

-- Users Table
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL,
  full_name TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  last_login TIMESTAMP,
  current_level TEXT,
  xp_points INTEGER DEFAULT 0
);

-- Progress Table
CREATE TABLE progress (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  skill_area TEXT,
  level TEXT,
  correct_answers INTEGER,
  total_attempts INTEGER,
  last_practiced TIMESTAMP DEFAULT NOW()
);

-- Conversations Table
CREATE TABLE conversations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  started_at TIMESTAMP DEFAULT NOW(),
  ended_at TIMESTAMP,
  difficulty_level TEXT,
  topics_discussed TEXT[]
);

-- RLS (Row Level Security) Policies
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE progress ENABLE ROW LEVEL SECURITY;
ALTER TABLE conversations ENABLE ROW LEVEL SECURITY;

-- Users can only see their own data
CREATE POLICY "Users can only see their own data" ON users
  FOR ALL USING (auth.uid() = id);

CREATE POLICY "Users can only see their own progress" ON progress
  FOR ALL USING (auth.uid() = user_id);

CREATE POLICY "Users can only see their own conversations" ON conversations
  FOR ALL USING (auth.uid() = user_id);

-- Grant access to authenticated users
GRANT ALL ON users TO authenticated;
GRANT ALL ON progress TO authenticated;
GRANT ALL ON conversations TO authenticated;