from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
import openai
import re
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Text
# Configura tu clave de API de OpenAI
openai.api_key = ''

app = Flask(__name__)
app.permanent_session_lifetime = timedelta(days=5)
app.secret_key = "hello"

# Configuración de la base de datos SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Definición del modelo de base de datos para los usuarios
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    some_integer = db.Column(db.Integer, default=0)
    temas = db.relationship('Tema', backref='usuario', lazy=True)

    def __repr__(self):
        return f'<Usuario {self.username}>'

class Tema(db.Model):
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    preguntas = Column(Text, nullable=False)
    reactivos = Column(Text, nullable=True)  # Permitir valores nulos
    respuestas_correctas = Column(Text, nullable=True)  # Permitir valores nulos
    usuario_id = Column(Integer, db.ForeignKey('usuario.id'), nullable=False)

    def __repr__(self):
        return f'<Tema {self.nombre}>'

# Crear la base de datos y las tablas si no existen
with app.app_context():
    db.create_all()

@app.route("/", methods=["POST", "GET"])
def home():
    if "user" in session:
        user = session["user"]
        return render_template("Home.html", usr=user)
    else:
        usuarios = Usuario.query.all()
        has_users = len(usuarios) > 0  # Variable que indica si hay usuarios
        return render_template("Start.html",has_users=has_users)

@app.route("/Login", methods=["POST", "GET"])
def Login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["username"]
        password = request.form["password"]

        # Verificar si el usuario existe en la base de datos
        usuario = Usuario.query.filter_by(username=user).first()

        if usuario and usuario.password == password:
            session["user"] = user
            session["user_id"] = usuario.id  # Guarda el ID del usuario en la sesión    
            return redirect(url_for("home"))
        else:
            flash("Incorrect username or password. Please try again.")
            return redirect(url_for("Login"))
    else:
        if "user" in session:
            return redirect(url_for("home"))
        return render_template("Login.html")

@app.route("/Signup", methods=["POST", "GET"])
def Signup():
    if request.method == "POST":
        session.permanent = True
        user = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # Comprobar si el usuario ya existe
        existing_user = Usuario.query.filter_by(username=user).first()
        existing_email = Usuario.query.filter_by(email=email).first()
        
        if existing_user:
            flash("The username already exists. Please choose another one.")
            return redirect(url_for("Signup"))
        
        if existing_email:
            flash("The email is already registered. Please use another one.")
            return redirect(url_for("Signup"))

        # Crear un nuevo usuario
        nuevo_usuario = Usuario(username=user, email=email, password=password)

        # Añadir y confirmar cambios en la base de datos
        db.session.add(nuevo_usuario)
        db.session.commit()

        session["user"] = user
        session["user_id"] = nuevo_usuario.id  # Guarda el ID del usuario en la sesión    
        return redirect(url_for("home"))
    else:
        if "user" in session:
            return redirect(url_for("home"))
        return render_template("Signup.html")


@app.route("/Lessons", methods=["POST", "GET"])
def Lessons():
    if "user" in session:
        user = session["user"]
        user_id = session["user_id"]
        session["Resultados"]=0
        temas = Tema.query.filter_by(usuario_id=user_id).all()  # Obtener los temas del usuario actual
        if request.method == "POST":
            nombre_tema = request.form["texto"]

            # Verificar si el tema ya existe para el usuario actual
            tema_existente = Tema.query.filter_by(nombre=nombre_tema, usuario_id=user_id).first()

            if tema_existente:
                # Redirigir a la página de trabajo si el valor de some_integer es menor que 10
                usuario = Usuario.query.filter_by(id=user_id).first()
                if usuario.some_integer < 10:
                    return redirect(url_for("workplace"))
                else:
                    # Generar nuevas preguntas
                    nuevas_preguntas = chat(nombre_tema, 10)

                    # Combinar las preguntas existentes con las nuevas
                    preguntas_existentes = tema_existente.preguntas.split("; ")
                    todas_preguntas = preguntas_existentes + nuevas_preguntas

                    # Actualizar el tema con las nuevas preguntas
                    tema_existente.preguntas = "; ".join(todas_preguntas)
                    db.session.commit()

                    # Redirigir a la página de trabajo
                    return redirect(url_for("workplace"))
            else:
                # Crear un nuevo tema si no existe
                nuevas_preguntas, reactivos_lista, respuestas_correctas = chat(nombre_tema, 10)
                nuevo_tema = Tema(nombre=nombre_tema, preguntas="; ".join(nuevas_preguntas), usuario_id=user_id)
                db.session.add(nuevo_tema)
                db.session.commit()

                # Guardar la lista de reactivos en la sesión
                session['reactivos'] = reactivos_lista  # Aquí puedes inicializar con la lista vacía si es necesario
                session["respuestas"]= respuestas_correctas
                return redirect(url_for("workplace"))

        return render_template("lessons.html", usr=user, x=1, temas=temas)
    else:
        return redirect(url_for("Login"))





@app.route("/Logoff", methods=["POST", "GET"])
def Logoff():
    session.pop("user", None)
    session.pop("user_id", None)  # Elimina el ID del usuario de la sesión    
    return redirect(url_for("home"))
@app.route("/workplace", methods=["POST", "GET"])
def workplace():
    if "user" in session:
        user = session["user"]
        user_id = session["user_id"]

        # Obtener el usuario de la base de datos
        usuario = Usuario.query.filter_by(id=user_id).first()

        if request.method == "POST":
            # Check which button was pressed
            if "Dato" in request.form:
                if request.form["Dato"] == "Start new topic":
                    # Reset the integer and redirect to lessons with x=1
                    usuario.some_integer = 0
                    db.session.commit()
                    return redirect(url_for("Lessons"))

                elif request.form["Dato"] == "Continue Learning":
                    # Generate 10 new questions
                    nombre_tema = session["nombre_tema"]
                    nuevas_preguntas, nuevos_reactivos, nuevas_respuestas = chat(nombre_tema, 10)

                    # Store new questions, reactives, and correct answers in session
                    session["texto"] = nuevas_preguntas
                    session["reactivos"] = nuevos_reactivos
                    session["respuestas"] = nuevas_respuestas

                    return redirect(url_for("workplace"))

            # Increment the question counter
            usuario.some_integer += 1
            db.session.commit()

            # Get the selected option and check against the correct answer
            dato = request.form["Dato"]
            respuestas_correctas = session["respuestas"]
            opcion_seleccionada = dato[3:].strip()  # Remove first 3 chars
            respuesta_correcta = respuestas_correctas[0][3:].strip()

            # Increment result if correct
            if opcion_seleccionada == respuesta_correcta:
                session["Resultados"] += 1

            # If user has answered 10 questions, call chat for feedback
            if usuario.some_integer >= 10:
                correct_answers = session["Resultados"]
                flash(f"You answered {correct_answers} out of 10 questions correctly.")

                # Call chat to provide feedback or study material
                feedback_prompt = f"The user answered {correct_answers} out of 10 questions correctly on the topic {session['nombre_tema']}. Provide study material or references based on their performance."
                _, _, feedback_responses = chat(feedback_prompt, 1)

                # Flash the study material or feedback as a message
                flash(feedback_responses[0])

                # Redirect to the feedback page (x=3)
                return render_template("lessons.html", usr=user, x=3)

            # Get the list of reactives for the next question
            reactivos_lista = session['reactivos']
            preguntas = session["texto"]

            # Continue the lesson (x=2)
            return render_template("lessons.html", usr=user, x=2, texto=preguntas[usuario.some_integer], dato=reactivos_lista, a=usuario.some_integer)
    
    else:
        return redirect(url_for("Login"))




@app.route("/show_users", methods=["GET"])
def show_users():
    usuarios = Usuario.query.all()
    user_data = "<h1>Lista de Usuarios y Temas</h1><ul>"

    for usuario in usuarios:
        user_data += f'<li>ID: {usuario.id}, Nombre: {usuario.username}, Correo: {usuario.email}, Some Integer: {usuario.some_integer}'
        temas = Tema.query.filter_by(usuario_id=usuario.id).all()
        if temas:
            user_data += "<ul>"
            for tema in temas:
                user_data += f'<li>Nombre del Tema: {tema.nombre}, Preguntas: {tema.preguntas}</li>'
            user_data += "</ul>"
        else:
            user_data += "<p>No hay temas para este usuario.</p>"
        user_data += "</li>"
    
    user_data += "</ul>"
    return user_data

def chat(texto, numero_preguntas=10):
    preguntas = []
    reactivos_lista = []
    respuestas_correctas = []
    for i in range(1, numero_preguntas + 1):
        prompt_text = f"""
        The user wants to learn about this topic: {texto}
    Please provide a question about that topic following these instructions:
        1. You will ask questions about basic concepts of exercises and sports, one at a time.
        2. For each question, provide a list of 4 options labeled A, B, C, and D. Among these options, one must be the correct answer.
        3. The answer options must be listed under the title "Options".
        4. The correct answer must be listed separately under the title "Correct Answer".
        5. If the user makes more than 5 mistakes, you will provide an explanation of the topic and suggestions to improve the user's learning.
        6. Each question must be numbered sequentially.
        7. Do not repeat questions.
    **Question {i}:**
        """
        response = openai.chat.completions.create(
        model="gpt-4o-mini",  # El motor de IA que deseas utilizar
        messages = [
            {"role": "system", "content" : prompt_text},
            ]
       )
        response_text = response.choices[0].message.content
        response_text = response_text.replace("**", "")
        response_text = re.sub(r'Pregunta \d+:', '', response_text, flags=re.IGNORECASE)  # Remover 'Pregunta N:'
        print("HOLA")
        print(response_text)
        partes_texto = response_text.split("Reactivos:")
        if len(partes_texto) >= 2:
            # Parte de la pregunta
            texto_antes_de_opciones = partes_texto[0].strip()
            preguntas.append(texto_antes_de_opciones)

            # Parte de los reactivos
            opciones_y_respuesta = partes_texto[1].strip()
            if "Respuesta correcta:" in opciones_y_respuesta:
                reactivos, respuesta_correcta = opciones_y_respuesta.split("Respuesta correcta:")
                reactivos = reactivos.strip().split("\n")
                reactivos = [reactivo.strip() for reactivo in reactivos if reactivo.strip()]
                reactivos_lista.extend(reactivos)
                respuestas_correctas.append(respuesta_correcta.strip())
                print(reactivos_lista)
                print(respuestas_correctas)
    return preguntas, reactivos_lista, respuestas_correctas

if __name__ == "__main__":
    app.run()
