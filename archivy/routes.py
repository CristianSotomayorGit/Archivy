from wtforms import SelectField, PasswordField, StringField, SubmitField, ValidationError
from archivy import app, db, bcrypt
from flask import jsonify, render_template, url_for, flash, redirect, request
from flask_login import  login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length, ValidationError
from archivy.model import User, Project, Conversation, UserInfo
from sqlalchemy.exc import SQLAlchemyError
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
import os
from utility.pdfLoader import create_docsearch
# , search_pdf

##Load pdf
pdf_path = os.path.join("static", "newContentWithClasses.html") 

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class RegisterForm(FlaskForm):
    firstname = StringField(validators=[
                           InputRequired(), Length(min=4, max=40)], render_kw={"placeholder": "First Name"})
    lastname = StringField(validators=[
                           InputRequired(), Length(min=4, max=40)], render_kw={"placeholder": "Last Name"})
    email = StringField(validators=[
                           InputRequired(), Length(min=4, max=40)], render_kw={"placeholder": "Email"})
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')

class NewProjectForm(FlaskForm):
    name = StringField(validators=[
                           InputRequired(), Length(min=4, max=40)], render_kw={"placeholder": "Name"})
    address = StringField(validators=[
                           InputRequired(), Length(min=4, max=150)], render_kw={"placeholder": "Address"})
    description = StringField(validators=[
                           InputRequired(), Length(min=20, max=500)], render_kw={"placeholder": "Description"})

    submit = SubmitField('Add')

class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')

class MarketSurveyform(FlaskForm):

    industry_choices = [
        ('', 'Industry'),
        ('Academic', 'Academic'),
        ('Architecture', 'Architecture'),
        ('BuildingOwnerManager', 'Building Owner / Manager'),
        ('Construction', 'Construction'),
        ('Engineering', 'Engineering'),
        ('Government', 'Government'),
        ('Manufacturing', 'Manufacturing'),
        ('SpecialtyContractor', 'Specialty Contractor'),
        ('HomeOwner', 'Home Owner'),
        ('Other', 'Other')
    ]

    jurisdiction_choices = [
                ('', 'Jurisdiction'),

    ('Alabama', 'Alabama'),
    ('Alaska', 'Alaska'),
    ('Arizona', 'Arizona'),
    ('Arkansas', 'Arkansas'),
    ('California', 'California'),
    ('Colorado', 'Colorado'),
    ('Connecticut', 'Connecticut'),
    ('Delaware', 'Delaware'),
    ('Florida', 'Florida'),
    ('Georgia', 'Georgia'),
    ('Hawaii', 'Hawaii'),
    ('Idaho', 'Idaho'),
    ('Illinois', 'Illinois'),
    ('Indiana', 'Indiana'),
    ('Iowa', 'Iowa'),
    ('Kansas', 'Kansas'),
    ('Kentucky', 'Kentucky'),
    ('Louisiana', 'Louisiana'),
    ('Maine', 'Maine'),
    ('Maryland', 'Maryland'),
    ('Massachusetts', 'Massachusetts'),
    ('Michigan', 'Michigan'),
    ('Minnesota', 'Minnesota'),
    ('Mississippi', 'Mississippi'),
    ('Missouri', 'Missouri'),
    ('Montana', 'Montana'),
    ('Nebraska', 'Nebraska'),
    ('Nevada', 'Nevada'),
    ('New Hampshire', 'New Hampshire'),
    ('New Jersey', 'New Jersey'),
    ('New Mexico', 'New Mexico'),
    ('New York', 'New York'),
    ('North Carolina', 'North Carolina'),
    ('North Dakota', 'North Dakota'),
    ('Ohio', 'Ohio'),
    ('Oklahoma', 'Oklahoma'),
    ('Oregon', 'Oregon'),
    ('Pennsylvania', 'Pennsylvania'),
    ('Rhode Island', 'Rhode Island'),
    ('South Carolina', 'South Carolina'),
    ('South Dakota', 'South Dakota'),
    ('Tennessee', 'Tennessee'),
    ('Texas', 'Texas'),
    ('Utah', 'Utah'),
    ('Vermont', 'Vermont'),
    ('Virginia', 'Virginia'),
    ('Washington', 'Washington'),
    ('West Virginia', 'West Virginia'),
    ('Wisconsin', 'Wisconsin'),
    ('Wyoming', 'Wyoming')
]
    
    project_type_choices = [
    ('', 'Main Project Type'),
    ('Commercial', 'Commercial'),
    ('Education', 'Education'),
    ('Public', 'Public'),
    ('Residential', 'Residential'),
    ('Mixed', 'Mixed'),
    ('Other', 'Other')
    ]

    organization_size_choices = [('','Organization Size'),
                                 ('1-10','1-10'),
                                 ('11-50','11-50'),
                                 ('51-200','51-200'),
                                 ('201-1000','201-1000'),
                                 ('> 1000','> 1000')]


    industry= SelectField('Industry', choices=industry_choices, default='', validators=[InputRequired()])
    
    jurisdiction= SelectField('Jurisdiction', choices=jurisdiction_choices, default='', validators=[InputRequired()])

    project_type= SelectField('Project_req', choices=project_type_choices, default='', validators=[InputRequired()])

    organization_size= SelectField('Project_req', choices=organization_size_choices, default='', validators=[InputRequired()])

    desired_code_1 = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Desired Building Code #1"})

    desired_code_2 = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Desired Building Code #2"})

    submit = SubmitField('Submit')



# TODO: must build a landing page
@app.route('/')
def index():
    return render_template('code.html')

# @app.route('/iframe_sidebar_content')
# def iframe_sidebar_content():
#     filename = request.args.get('filename')

#     return render_template('codes/' + str(filename))

# @app.route('/iframe_code_content')
# def iframe_code_content():
#     filename = request.args.get('filename')

#     return render_template('codes/2010-design-standards_files/' + str(filename))

@app.route('/iframe')
def iframe():
    filename = request.args.get('filename')
    print('attempt  render')
    return render_template('codes/2010-design-standards/' + str(filename))


@app.route('/marketSurvey', methods=["GET", "POST"])
def marketSurvey():
    form = MarketSurveyform()

    try:
        if form.validate_on_submit():
            new_user_info = UserInfo(industry=form.industry.data,jurisdiction=form.jurisdiction.data, main_project_type=form.project_type.data, organization_size=form.organization_size.data, building_code_1=form.desired_code_1.data, building_code_2=form.desired_code_2.data, user_id=current_user.id)
            db.session.add(new_user_info)

            user_to_update = User.query.filter_by(id=current_user.id).first()
            user_to_update.hasAnswered = 1
            
            db.session.commit()
            return redirect(url_for('viewcode'))

    except SQLAlchemyError as e:
        db.session.rollback() 
        print(e)

    return render_template('marketsurvey.html', form=form)

@app.route('/viewcode')
def viewcode():
    return render_template('code.html')


@app.route('/conversation/<int:conversation_id>')
def conversation(conversation_id):
    return str(conversation_id)


@app.route('/project/<int:project_id>')
@login_required
def projectdetail(project_id):
    project = Project.query.filter_by(id=project_id).first()
    conversations=project.conversations
    if not project:
        flash('Project not found!', 'error')
        return redirect(url_for('login'))

    return render_template('project.html', project=project, conversations=conversations)


@app.route('/deleteproject/<int:project_id>', methods=['POST'])
@login_required
def deleteproject(project_id):
    try:
        # Query the project based on the project_id
        project = Project.query.get(project_id)
        
        # Ensure the current user owns the project before deleting
        if project and project.userid == current_user.id:
            db.session.delete(project)
            db.session.commit()
            flash('Project successfully deleted', 'success')
        else:
            flash('Unauthorized action or project not found', 'error')
            
    except SQLAlchemyError as e:
        db.session.rollback()
        flash('An error occurred while deleting the project', 'error')
        print(e)

    return redirect(url_for('profile'))


@app.route('/deleteconversation/<int:conversation_id>', methods=['POST'])
@login_required
def deleteconversation(conversation_id):
    try:
        # Query the project based on the project_id
        conversation = Conversation.query.get(conversation_id)
        
        # Ensure the current user owns the project before deleting
        if conversation:
            db.session.delete(conversation)
            db.session.commit()
            flash('Conversation successfully deleted', 'success')
        else:
            flash('Conversation project not found', 'error')
            
    except SQLAlchemyError as e:
        db.session.rollback()
        flash('An error occurred while deleting the conversation', 'error')
        print(e)

    return redirect(request.referrer or url_for('login'))

@app.route('/newproject', methods=["GET", "POST"])
@login_required
def newproject():
    form = NewProjectForm()

    try:
        print('yoooooooooooooooo')
        if form.validate_on_submit():
            new_project = Project(userid=current_user.id, name=form.name.data,address=form.address.data, description=form.description.data)
            db.session.add(new_project)
            db.session.commit()
            return redirect(url_for('profile'))
        else:
            print(form.name.data)
            print(form.address.data)
            print(form.description.data)

    except SQLAlchemyError as e:
        db.session.rollback() 
        print(e)

    return render_template('newproject.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))  # Assuming 'login' is the endpoint for your login page.


@app.route('/profile')
@login_required
def profile():
    user = User.query.filter_by(id=current_user.id).first()
    if not user:
        flash('User not found!', 'error')
        return redirect(url_for('login'))
    
    projects = user.projects

    return render_template('profile.html', user=user, projects=projects)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()


    try:
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data)
            new_user = User(firstname=form.firstname.data,lastname=form.lastname.data, email=form.email.data, username=form.username.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            print(form.firstname.data)
            print(form.lastname.data)
            print(form.email.data)
            print(form.username.data)
            print(form.password.data)

    except SQLAlchemyError as e:
        db.session.rollback() 
        print(e)

    return render_template('register.html',form=form)

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)

                # Prompt user for market research info
                if user.hasAnswered == False:
                    return redirect(url_for('marketSurvey'))
                
                else:
                    return redirect(url_for('viewcode'))
    return render_template('login.html', form=form)


print(app.config['OPEN_AI_SECRET_KEY'])


docsearch_obj= create_docsearch(
pdf_path,
openai_api_key = app.config['OPEN_AI_SECRET_KEY'],
pinecone_api_key='d8e80bbb-525e-475f-ac1c-4eae25c860bd',
index_name='langchain1'
)



@app.route('/code')
def code():
    return render_template('code.html')

@app.route('/process_message', methods=['POST'])
def process_message():
    data = request.get_json()
    message = data.get('message')
    # selectedText = data.get('selectedText')
    # openai.api_key = apiKey

    conversation_history = [ {
        "role": "system",
        "content": "You are a building codes expert with expertise in ADA Design Standards. Be friendly and helpful. Your replies should be in paragraphs with double spaces in between them, use numbered lists when necessary, and include a sources section at the bottom listing specific building code sections relevant to your response."
    },
    {"role": "user", "content": message}
]

    llm = ChatOpenAI(temperature=0, openai_api_key=app.config['OPEN_AI_SECRET_KEY'],model="gpt-4")
    chain = load_qa_chain(llm, chain_type='stuff')

    # Get the current directory (directory of app.py)

    # Example usage:


    docs =docsearch_obj.similarity_search(message)

    relatedChunks = []
    for doc in docs:
        print(doc.metadata)
        relatedChunks.append(doc.metadata)


        system_message = {
        "role": "system",
        "content": "You are a building codes expert with expertise in ADA Design Standards. Your replies should be in paragraphs with spaces in between them, use numbered lists when necessary, and include a sources section at the bottom listing specific building code sections relevant to your response."
    }    

    responseText = chain.run(input_documents=docs, question=conversation_history)
    # Process the message and selectedText, and generate a response
    # response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
    #                                     messages=[
    #                                         {"role": "system", "content": "You are a helpful assistant that helps construction professionals interpret building codes."},
    #                                         {"role": "user", "content": f"Message: {message} | Selected Text: {selectedText}"}
    #                                     ]
    #                                 )
    
    # responseText = response["choices"][0]["message"]["content"]
    
    # location = search_pdf(message, index_name='langchain1')

    print(responseText)
    print("")
    # print("Location in PDF:", location)
    print("")

    return jsonify(responseText=responseText, relatedChunks=relatedChunks)