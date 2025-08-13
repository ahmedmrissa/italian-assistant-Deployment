# Rasa Chatbot with Supabase Integration

This is a Rasa chatbot with Supabase integration for user authentication, progress tracking, and conversation history.

## Features
- Italian language support
- User authentication with Supabase
- Progress tracking
- Conversation history
- Grammar and vocabulary exercises

## Deployment to Fly.io

### Prerequisites
1. Install [Fly.io CLI](https://fly.io/docs/getting-started/installing-flyctl/)
2. Create a [Fly.io account](https://fly.io/app/sign-up/)
3. Create a [Supabase account](https://app.supabase.io/) and set up your database

### Deployment Steps

1. **Login to Fly.io**:
   ```bash
   fly auth login
   ```

2. **Launch your app**:
   ```bash
   fly launch
   ```
   - Choose a unique app name
   - Select your organization
   - Choose not to deploy yet (we need to set secrets first)

3. **Set environment variables**:
   ```bash
   fly secrets set SUPABASE_URL=your_supabase_url
   fly secrets set SUPABASE_KEY=your_supabase_key
   fly secrets set SUPABASE_DB_URL=your_supabase_db_url
   ```

4. **Deploy your app**:
   ```bash
   fly deploy
   ```

5. **Check deployment status**:
   ```bash
   fly status
   ```

6. **View logs**:
   ```bash
   fly logs
   ```

### Accessing Your Chatbot

After deployment, your chatbot will be available at `https://your-app-name.fly.dev`.

### Local Development

To run the chatbot locally:

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-supabase.txt
   ```

2. Train the model:
   ```bash
   rasa train
   ```

3. Run the Rasa server:
   ```bash
   rasa run --port 5005 --host 0.0.0.0
   ```

4. In a separate terminal, run the action server:
   ```bash
   rasa run actions --port 5055 --host 0.0.0.0
   ```

## Compatibility Fixes

This application includes fixes for common compatibility issues:
- Websockets version 9.1 for compatibility with Sanic
- Proper dependency installation order
- Environment variable support for cloud deployment
- Dual server configuration (Rasa server and action server)

These fixes ensure the application works correctly on any cloud platform including Fly.io, Heroku, Render, and others.# ahmedmrissa-italian-assistant-Deployment
# ahmedmrissa-italian-assistant-Deployment
# ahmedmrissa-italian-assistant-Deploymentt
# ahmedmrissa-italian-assistant-Deploymentt
# ahmedmrissa-italian-assistant-Deploymentt
# ahmedmrissa-italian-assistant-Deploymentt
