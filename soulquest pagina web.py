from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
import openai
import re
from flask_sqlalchemy import SQLAlchemy

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
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    preguntas = db.Column(db.Text, nullable=False)  # Almacena las preguntas como texto
    respuestas_correctas = db.Column(db.Text, nullable=False)  # Almacena las respuestas correctas
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

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
            flash("Usuario o contraseña incorrectos. Inténtalo de nuevo.")
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
            flash("El nombre de usuario ya existe. Por favor, elige otro.")
            return redirect(url_for("Signup"))
        
        if existing_email:
            flash("El correo electrónico ya está registrado. Por favor, usa otro.")
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
                    # Generar nuevas preguntas y combinarlas con las preguntas existentes
                    nuevas_preguntas, nuevos_reactivos, nuevas_respuestas = chat(nombre_tema, 10)

                    # Combinar las preguntas y respuestas existentes con las nuevas
                    preguntas_existentes = tema_existente.preguntas.split("; ")
                    respuestas_existencias = tema_existente.respuestas_correctas.split("; ")
                    todas_preguntas = preguntas_existentes + nuevas_preguntas
                    todas_respuestas = respuestas_existencias + nuevas_respuestas

                    # Actualizar el tema con las nuevas preguntas y respuestas
                    tema_existente.preguntas = "; ".join(todas_preguntas)
                    tema_existente.respuestas_correctas = "; ".join(todas_respuestas)
                    db.session.commit()

                    # Redirigir a la página de trabajo
                    return redirect(url_for("workplace"))
            else:
                # Crear un nuevo tema si no existe
                nuevas_preguntas, nuevos_reactivos, nuevas_respuestas = chat(nombre_tema, 10)
                nuevo_tema = Tema(nombre=nombre_tema, preguntas="; ".join(nuevas_preguntas),
                                  respuestas_correctas="; ".join(nuevas_respuestas), usuario_id=user_id)
                db.session.add(nuevo_tema)
                db.session.commit()
                return redirect(url_for("workplace"))

        return render_template("lessons.html", usr=user, x=1)
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
            usuario.some_integer += 1
            db.session.commit()

            texto = session.get("texto", [])
            lista = session.get("lista", [])
            respuesta = session.get("respuesta", [])

            return render_template("lessons.html", usr=user, x=2, texto=texto[usuario.some_integer], dato=lista, a=usuario.some_integer)
        else:
            texto = session.get("texto", [])
            lista = session.get("lista", [])
            respuesta = session.get("respuesta", [])

            return render_template("lessons.html", usr=user, x=2, texto=texto[usuario.some_integer], dato=lista, a=usuario.some_integer)
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
        El usuario quiere aprender sobre este tema: {texto}

        Deberás darme una pregunta sobre ese tema siguiendo estas instrucciones:
        1. Harás preguntas sobre conceptos básicos de ejercicios y deportes, una por una.
        2. Para cada pregunta, proporcionarás un listado de 4 reactivos (opciones de respuesta) etiquetados como A, B, C, y D. Entre estas opciones, una debe ser la respuesta correcta.
        3. Las opciones de respuesta (reactivos) deben ser listadas bajo el título "Reactivos".
        4. El reactivo correcto debe ser listado por separado bajo el título "Respuesta correcta".
        5. Si el usuario comete más de 5 errores, proporcionarás una explicación del tema y sugerencias para mejorar el aprendizaje del tema.
        6. Cada pregunta debe ser numerada secuencialmente.
        7. No repitas preguntas.

        **Pregunta {i}:**
        """

        response = openai.Completion.create(
            engine="gpt-4o-mini",  # El motor de IA que deseas utilizar
            prompt=prompt_text,
            max_tokens=150
        )

        response_text = response.choices[0].text.strip()
        response_text = re.sub(r'Pregunta \d+:', '', response_text, flags=re.IGNORECASE)  # Remover 'Pregunta N:'
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
    return preguntas, reactivos_lista, respuestas_correctas

if __name__ == "__main__":
    app.run()
