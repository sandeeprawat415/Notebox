# NoteBox 📝

A simple, clean note-taking web app built with Flask and SQLite. Create, edit, delete, pin, search, and categorize notes — all with a minimal, distraction-free UI.

## Features

- **Create / Edit / Delete** notes with title, content, and category
- **Pin** important notes to keep them at the top
- **Search** notes by title or content
- **Filter** by category
- **Timestamps** — see when each note was last updated
- No JavaScript frameworks — plain Flask + Jinja2 + vanilla CSS

## Tech Stack

- **Backend:** Flask, Flask-SQLAlchemy
- **Database:** SQLite (file-based, zero setup)
- **Frontend:** Jinja2 templates, custom CSS (no framework bloat)

## Setup

\`\`\`bash
# Clone the repo
git clone <your-repo-url>
cd notes-app

# Create a virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
\`\`\`

Visit `http://127.0.0.1:5000` in your browser. The SQLite database (`notes.db`) is created automatically on first run.

## Project Structure

\`\`\`
notes-app/
├── app.py                 # Flask app, routes, models
├── requirements.txt
├── static/
│   └── style.css
└── templates/
    ├── base.html
    ├── index.html          # Notes list, search, filter
    └── form.html           # Create/edit form
\`\`\`

## Possible Extensions

- Markdown rendering for note content
- Tagging system (many-to-many instead of single category)
- User authentication (multi-user support)
- Archive instead of hard delete
- REST API endpoints (DRF-style) for a future mobile/React frontend
- Export notes to PDF or Markdown files

## License

MIT
