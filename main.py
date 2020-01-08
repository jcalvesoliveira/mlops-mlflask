from flask import Flask, request
from flask_basicauth import BasicAuth
from textblob import TextBlob
import pickle

modelo = pickle.load(open('modelo.sav','rb'))

colunas = ['tamanho','ano','garagem']

app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'julio'
app.config['BASIC_AUTH_PASSWORD'] = 'alura'

basic_auth = BasicAuth(app)

@app.route('/')
def home():
	return "Minha primeira API"

@app.route('/sentimento/<frase>')
@basic_auth.required
def sentimento(frase):
	tb = TextBlob(frase)
	tb_en = tb.translate(to='en')
	polaridade = tb_en.sentiment.polarity
	sentimento = "polaridade: {}".format(polaridade)
	return sentimento

@app.route('/cotacao', methods=['POST'])
@basic_auth.required
def cotacao():
	dados = request.get_json()
	lista = [dados[col] for col in colunas]
	predicao = modelo.predict([lista])
	return (str(predicao))


	
app.run(debug=True)