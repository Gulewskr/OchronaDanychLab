#bez autoryzacji
from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from .database import User, Note, ConnectorNote
from .notesCrypt import decryptNote, encryptNote
from .database import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    #Dodanie pobierania notatek tylko do których użytkownik ma dostęp
    publicNotes = Note.query.filter(Note.isPublic)

    for note in publicNotes:
        note.title = decryptNote(note.title)
        note.text = decryptNote(note.text)

    return render_template('index.html', publicNotes = publicNotes)

@main.route('/profile')
@login_required
def profile():
    usersData = User.query.all()
    return render_template('profile.html', name=current_user.login, UsersData = usersData)

@main.route('/notes')
def notes():
    #Dodanie pobierania notatek tylko do których użytkownik ma dostęp
    userNotes = Note.query.filter(Note.userID == current_user.login)
    publicNotes = Note.query.filter(Note.isPublic & (Note.userID != current_user.login))
    connectedNotes = Note.query.filter((ConnectorNote.userID == current_user.id) & (ConnectorNote.noteID == Note.id))
    
    #Odszyfrowanie notatki
    for note in userNotes:
        note.title = decryptNote(note.title)
        note.text = decryptNote(note.text)

    for note in publicNotes:
        note.title = decryptNote(note.title)
        note.text = decryptNote(note.text)

    for note in connectedNotes:
        note.title = decryptNote(note.title)
        note.text = decryptNote(note.text)

    return render_template('noteList.html', userNotes = userNotes, publicNotes = publicNotes, connectedNotes = connectedNotes)

    
@main.route('/notes/new')
@login_required
def addNote():
    return render_template('noteForm.html', name=current_user.login , UserID=current_user.id)

@login_required
@main.route('/notes/new', methods=['POST'])
def addNote_post():
    #Dane Notatki
    userId = current_user.login
    title = request.form.get('title')
    note = request.form.get('note')
    public = True if request.form.get('isPublic') else False
    users = request.form.get('users')

    #walidacja danych formularza

    allowedUsers = users.split(" ")

    #Szyfrowanie notatki

    #Utworzenie nowej notatki
    newNote = Note(
        title = encryptNote(title),
        text = encryptNote(note),
        isPublic = public,
        userID = userId )

    db.session.add(newNote)
    db.session.commit()

    noteID = Note.query.order_by(Note.id.desc()).first()

    for user in allowedUsers:
        _user = user.replace(' ', '')
        userData = User.query.filter(User.login == _user).first()
        if userData:
            connect = ConnectorNote(
                noteID = noteID.id,
                userID = userData.id
            )
            db.session.add(connect)
    db.session.commit()
    return redirect(url_for('main.profile'))