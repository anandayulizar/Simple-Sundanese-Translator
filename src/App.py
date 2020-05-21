from flask import Flask, escape, render_template, url_for, redirect, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, TextField
from wtforms.validators import DataRequired
from Translator import translate

class translationForm(FlaskForm):
    left = TextField('Indonesia', validators=[DataRequired()])
    right = TextField('Sunda', validators=[DataRequired()])
    pattern = RadioField('Choose Your Pattern', choices=[('KMP', 'KMP'), ('BM', 'BM'), ('Regex', 'Regex')], validators=[DataRequired()])

    submit = SubmitField('Match Key!')

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        sentence = request.form['left-translation']
        matcher = request.form['algorithm']
        language = request.form['submit'].lower() + '.txt'
        if (request.form['submit'] == 'Sunda'):
            isSunda = True
        else:
            isSunda = False

        result, isSentence = translate(language, sentence, matcher)

        return render_template('index.html', sentence=sentence, matcher=matcher, result=result, isSentence=isSentence, isSunda=isSunda)   
    except:   
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)