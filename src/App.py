from flask import Flask, render_template, url_for,request
from Translator import translate

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        sentence = request.form['left-translation']
        matcher = int(request.form['algorithm'])
        dictionary = request.form['submit'].lower() + '.txt'
        isSunda = request.form['submit'] == 'Sunda'

        result, alternatives = translate(dictionary, sentence, matcher)

        return render_template('index.html', sentence=sentence, result=result, alternatives=alternatives, isSunda=isSunda)   
    except:   
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)