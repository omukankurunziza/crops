from flask import render_template, request, redirect, url_for, abort
from . import main
from ..models import User, Disease, Comment, Subscribe, Symptom
from .. import db,photos
from .forms import DiseaseForm, CommentForm, SubscribeForm, SymptomForm
from flask_login import login_required, current_user
import datetime
from ..email import mail_message
import os
# from ..request import get_quotes
#Views


@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data
    '''

    title = 'Home - Welcome to my favorite Crop!!'
    diseases = Disease.query.order_by(Disease.date_posted.desc()).all()
    # quotes= get_quotes()
    return render_template('index.html', title=title,  diseases=diseases)


@main.route('/disease/new/<int:id>', methods=['GET', 'POST'])
@login_required
def new_disease(id):
    disease_form = DiseaseForm()
    disease= Disease.query.filter_by(id=id).first()
    # if 'photo' in request.files:
    #     filename = photos.save(request.files['photo'])
    #     path = f'photos/{filename}'
    #     Disease.picture_url = path
    if disease_form.validate_on_submit():
        # f = disease_form.image.data
        # img = current_user.username + "__" + f.filename
        # img = secure_filename(img)
        # f.save(os.path.join("./static/photos/", img))
        name = disease_form.name.data
        control = disease_form.control.data
        category=disease_form.category.data
        symptoms=disease_form.symptoms.data

        users = User.query.all()
        disease.name=name
        disease.control=control
        disease.category=category
        disease.symptoms=symptoms
        disease.approved="True"
        db.session.commit()
        # Update disease instance
        # new_disease = Disease(name=name, control=control, disease=current_user,category=category,symptoms=symptoms)

        # Save disease method
        # new_disease.save_disease()

        # for user in users:
        #     if user.subscription:
        #         mail_message("New Disease", "email/new_disease",user.email, user=user)

        return redirect(url_for('.all_diseases'))

    # else:
    #     return redirect(url_for('.index'))

    title = 'New disease'
    return render_template('new_disease.html', title=title, disease_form=disease_form)

@main.route('/symptom/new', methods=['GET', 'POST'])

def new_symptom():
    symptom_form = SymptomForm()
   
    if symptom_form.validate_on_submit():
        
        symptoms=symptom_form.symptoms.data

        # users = User.query.all()
        
        # Update disease instance
        new_symptom = Disease(symptoms=symptoms, approved='False')
        db.session.add(new_symptom)
        db.session.commit()

        # Save disease method
        # new_symptom.save_symptom()

        # for user in users:
        #     if user.subscription:
        #         mail_message("New Disease", "email/new_disease",user.email, user=user)

        return redirect(url_for('.all_symptoms'))

    # else:
    #     return redirect(url_for('.index'))

    title = 'New symptom'
    return render_template('new_symptom.html', title=title, symptom_form=symptom_form)

# @main.route('/agronomist', methods=['GET', 'POST'])
# @login_required
# def new_agronomist():
#     agronomist_form = AgronomistForm()
#     if agronomist_form.validate_on_submit():
#         name = agronomist_form.name.data
#         title = agronomist_form.title.data
        
#         # users = User.query.all()

#         # Update disease instance
#         new_agronomist = Agronomist(name=name, title=title)

#         # Save disease method
#         new_agronomist.save_agronimist()

#         # for user in users:
#         #     if user.subscription:
#         #         mail_message("New Disease", "email/new_disease",user.email, user=user)

#         # return redirect(url_for('.index'))

#     # else:
#     #     return redirect(url_for('.index'))

#     title = 'New agronomist'
#     return render_template('agronomist.html', title=title, agronomist_form=agronomist_form)


# @main.route('/user_diseases/new', methods=['GET', 'POST'])



# def user_disease():
#     user_diseases_form = User_diseasesForm()
#     # if User_diseasesForm.validate_on_submit():
#     symptom = User_diseasesForm.name.data
        

#         # users = User.query.all()

#         # Update disease instance
#     new_user_diseases = User_diseases(symptom=symptom)

#         # Save disease method
#     new_user_diseases.save_user_diseases()

#         # for user in users:
#         #     if user.subscription:
#         #         mail_message("New Disease", "email/new_disease",user.email, user=user)

#         # return redirect(url_for('.index'))

#     # else:
#     #     return redirect(url_for('.index'))

#     title = 'New user disease'
#     return render_template('user_diseases.html', title=title, disease_form=disease_form)
# def all_symptom():
#     user_diseases = User_diseases.query.order_by(user_diseases.date_posted.desc()).all()

#     title = 'Symptom posts'

#     return render_template('user_diseases.html', title=title, user_diseases=user_diseases)


@main.route('/diseases')
def all_diseases():
    # diseases = Disease.query.order_by(Disease.date_posted.desc()).all()
    diseases = Disease.query.filter_by(approved='True').all()
    print(diseases)
    title = 'Diseases posts'

    return render_template('diseases.html', title=title, diseases=diseases)

@main.route('/symptom')
def all_symptoms():
    # symptom = Symptom.query.order_by(Symptom.date_posted.desc()).all()
    symptoms = Disease.query.filter_by(approved='False').all()
    title = 'Diseases posts'

    return render_template('symptoms.html', title=title, symptoms=symptoms)


@main.route('/symptom/<int:id>', methods=['GET', 'POST'])
def symptom_detail(id):
    form = CommentForm()
    symptom = Disease.get_disease(id)

    if form.validate_on_submit():
        comment = form.names.data
        username = form.symptoms.data
        new_comment = Comment(username=username,comment=comment, symptom=symptom)

        new_comment.save_comment()

    comments = Comment.get_comments(symptom)

    title = f'{symptom.name}'
    return render_template('symptom.html', title=title, symptom=symptom, form=form, comments=comments)

@main.route('/disease/<int:id>', methods=['GET', 'POST'])
def disease(id):
    form = CommentForm()
    disease = Disease.get_disease(id)
    title = f'{disease.name}'
    return render_template('disease.html', title=title, disease=disease)


@main.route('/delete_comment/<id>/<disease_id>', methods=['GET', 'POST'])
@login_required
def delete_comment(id, disease_id):
    comment = Comment.query.filter_by(id=id).first()

    db.session.delete(comment)
    db.session.commit()

    return redirect(url_for('main.disease', id=disease_id))


@main.route('/approve/<id>', methods=['GET', 'POST'])
@login_required
def approve(id):
    symptom = Symptom.query.filter_by(id=id).first()

    db.session.approve(symptom)
    db.session.commit()

    return redirect(url_for('main.all_symptoms'))


@main.route('/subscribe/', methods=['GET', 'POST'])

def subscribe():
    """
    Function that enables one to subscribe to the disease crop
    """
    form = SubscribeForm()
    if form.validate_on_submit():
        subscribe = Subscribe(email=form.email.data)
        db.session.add(subscribe)
        db.session.commit()
        return redirect(url_for('main.index'))

    return render_template('auth/subscribe.html', form=form)



@main.route('/disease/update/<id>', methods=['GET', 'POST'])
@login_required
def update_disease(id):
    form = DiseaseForm()

    disease = Disease.query.filter_by(id=id).first()

    form.name.data = disease.name
    form.text.data = disease.text

    if form.validate_on_submit():
        name = form.title.data
        text = form.text.data

        disease.name = name
        disease.text = text

        db.session.commit()

        return redirect(url_for('main.disease', id=disease.id))

    return render_template('update.html', form=form)

