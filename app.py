from flask import Flask,render_template,request,redirect,url_for,flash
from flask_mysqldb import MySQL



# inicializamos el servidor flask
app= Flask(__name__,static_folder='static',template_folder='templates')

#configuraciones para la conexion a la BD
app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']=""
app.config['MYSQL_DB']="dbcar"

app.secret_key='mysecretkey'

mysql=MySQL(app)



#declaramos una ruta

#ruta index o principal http://localhost:5000
#la ruta se compone de nombre y la funcion
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/registrar')
def registrar():
    return render_template('RegistrarUsuarios.html')

@app.route('/iniciars')
def iniciars():
    return render_template('requerimientos.html')


#Creando mi primer Decorador o ruta para el Home
@app.route('/mostrar')
def mostrar():
    
    CS=mysql.connection.cursor()
    CS.execute ("SELECT * FROM autos")
    mysql.connection.commit()
    data = CS.fetchall() #fetchall () Obtener todos los registros

    total = CS.rowcount #total de registros

    print(total)
    return render_template('consultar.html', dataAutos = data, dataTotal = total)

@app.route('/iniciar',methods=['POST'])
def iniciar():
    if request.method == 'POST':
        nombre= request.form['txtnombre']
        contraseña= request.form['txtcontra']
        CS = mysql.connection.cursor()
        CS.execute('select * from usuarios where usuario=(%s) and contrasena=(%s)', (nombre,contraseña))
        if (CS.rowcount == 1):
            flash('Acceso correcto')
            return render_template('requerimientos.html')
        else:
            flash('Usuario o contraseña incorrecta')
            return render_template('Login.html')




@app.route('/requerir',methods=['POST'])
def requerir():
    if request.method == 'POST':
        marca= request.form['txtmarca']
        presupuesto= request.form['txtpresupuesto']
        color= request.form['txtcolor']
        asientos= request.form['txtasientos']
        estado= request.form['txtestado']
        CS = mysql.connection.cursor()
        CS.execute('insert into requerimientos (marca,presupuesto,color,asientos,estado) values(%s,%s,%s,%s,%s)',(marca,presupuesto,color,asientos,estado))
        mysql.connection.commit()
    
    return redirect(url_for('mostrar'))
        
        
@app.route('/guardar',methods=['POST'])
def guardar():
    if request.method == 'POST':
        nombre= request.form['txtnombre']
        usuario= request.form['txtusuario']
        correo= request.form['txtcorreo']
        contrasena= request.form['txtcontrasena']
        CS = mysql.connection.cursor()
        CS.execute('insert into usuarios (nombre,usuario,correo,contrasena) values(%s,%s,%s,%s)',(nombre,usuario,correo,contrasena))
        mysql.connection.commit()

    flash('Usuario guardado')
    return render_template("requerimientos.html")

#ejecucion 
if __name__== '__main__':
    app.run(port= 5000, debug=True)