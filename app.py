from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///notes.db"
app.config["SECRET_KEY"] = "dev-secret-key-change-this"
db = SQLAlchemy(app)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), default="General")
    pinned = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


with app.app_context():
    db.create_all()


@app.route("/")
def index():
    search = request.args.get("q", "").strip()
    category = request.args.get("category", "").strip()

    query = Note.query

    if search:
        query = query.filter(
            (Note.title.ilike(f"%{search}%")) | (Note.content.ilike(f"%{search}%"))
        )
    if category:
        query = query.filter_by(category=category)

    notes = query.order_by(Note.pinned.desc(), Note.updated_at.desc()).all()
    categories = [c[0] for c in db.session.query(Note.category).distinct()]

    return render_template(
        "index.html", notes=notes, categories=categories, search=search, active_category=category
    )


@app.route("/note/new", methods=["GET", "POST"])
def new_note():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        category = request.form.get("category", "General").strip() or "General"

        if not title or not content:
            flash("Title and content are required.", "error")
            return redirect(url_for("new_note"))

        note = Note(title=title, content=content, category=category)
        db.session.add(note)
        db.session.commit()
        flash("Note created.", "success")
        return redirect(url_for("index"))

    return render_template("form.html", note=None)


@app.route("/note/<int:note_id>/edit", methods=["GET", "POST"])
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        category = request.form.get("category", "General").strip() or "General"

        if not title or not content:
            flash("Title and content are required.", "error")
            return redirect(url_for("edit_note", note_id=note_id))

        note.title = title
        note.content = content
        note.category = category
        db.session.commit()
        flash("Note updated.", "success")
        return redirect(url_for("index"))

    return render_template("form.html", note=note)


@app.route("/note/<int:note_id>/delete", methods=["POST"])
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    flash("Note deleted.", "success")
    return redirect(url_for("index"))


@app.route("/note/<int:note_id>/pin", methods=["POST"])
def pin_note(note_id):
    note = Note.query.get_or_404(note_id)
    note.pinned = not note.pinned
    db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
