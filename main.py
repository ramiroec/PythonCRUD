from flask import Flask, render_template, jsonify, request, redirect, url_for
import psycopg2

app = Flask(__name__)

# Configuración de la base de datos
db_config = {
    'dbname': 'bzvpsdcz',
    'user': 'bzvpsdcz',
    'password': '0RmfG9N5OyThBp8SC1oxQEnGin-bNjx5',
    'host': 'isabelle.db.elephantsql.com'
}

# Función para obtener todos los empleados
def obtener_todos_los_empleados():
    connection = psycopg2.connect(**db_config)
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM empleados;')
    empleados = cursor.fetchall()

    cursor.close()
    connection.close()

    return empleados

# Función para obtener un empleado por ID
def obtener_empleado_por_id(empleado_id):
    connection = psycopg2.connect(**db_config)
    cursor = connection.cursor()

    query = 'SELECT * FROM empleados WHERE empleado_id = %s;'
    cursor.execute(query, (empleado_id,))
    empleado = cursor.fetchone()

    cursor.close()
    connection.close()

    return empleado


# Ruta para eliminar un empleado por ID
@app.route('/api/empleados/<int:empleado_id>', methods=['DELETE'])
def eliminar_empleado(empleado_id):
    connection = psycopg2.connect(**db_config)
    cursor = connection.cursor()

    query = 'DELETE FROM empleados WHERE empleado_id = %s RETURNING *;'
    cursor.execute(query, (empleado_id,))
    empleado_eliminado = cursor.fetchone()

    connection.commit()
    cursor.close()
    connection.close()

    if empleado_eliminado:
        return jsonify({'mensaje': 'Empleado eliminado correctamente'})
    else:
        return jsonify({'mensaje': 'Empleado no encontrado'}), 404

@app.route('/', methods=['GET'])
def mostrar_todos_los_empleados_principal():
    empleados = obtener_todos_los_empleados()
    return render_template('empleados.html', empleados=empleados)

# Ruta para mostrar todos los empleados con HTML y CSS
@app.route('/empleados', methods=['GET'])
def mostrar_todos_los_empleados_html():
    empleados = obtener_todos_los_empleados()
    return render_template('empleados.html', empleados=empleados)


# Ruta para mostrar un empleado por ID con HTML y CSS
@app.route('/empleados/<int:empleado_id>', methods=['GET'])
def mostrar_empleado_por_id_html(empleado_id):
    empleado = obtener_empleado_por_id(empleado_id)

    if empleado:
        return render_template('empleados.html', empleado=empleado)
    else:
        return render_template('empleados.html', mensaje='Empleado no encontrado'), 404

# Ruta para obtener todos los empleados en formato JSON
@app.route('/api/empleados', methods=['GET'])
def obtener_todos_los_empleados_json():
    empleados = obtener_todos_los_empleados()
    return jsonify({'empleados': empleados})

# Ruta para obtener un empleado por ID en formato JSON
@app.route('/api/empleados/<int:empleado_id>', methods=['GET'])
def obtener_empleado_por_id_json(empleado_id):
    empleado = obtener_empleado_por_id(empleado_id)

    if empleado:
        return jsonify({'empleado': empleado})
    else:
        return jsonify({'mensaje': 'Empleado no encontrado'}), 404
#Funcion para insertar un empleado
def agregar_empleado(nombre, apellido, salario, fecha_contratacion):
  connection = psycopg2.connect(**db_config)
  cursor = connection.cursor()

  query = 'INSERT INTO empleados (nombre, apellido, salario, fecha_contratacion) VALUES (%s, %s, %s, %s) RETURNING *;'
  cursor.execute(query, (nombre, apellido, salario, fecha_contratacion))
  nuevo_empleado = cursor.fetchone()

  connection.commit()
  cursor.close()
  connection.close()

  return nuevo_empleado

# Ruta para mostrar el formulario de creación de empleado
@app.route('/empleado/crear', methods=['GET'])
def mostrar_formulario_crear_empleado():
    return render_template('crear_empleado.html')

# Ruta para manejar la creación de un nuevo empleado desde el formulario
@app.route('/api/empleado/crear', methods=['POST'])
def crear_empleado():
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    salario = request.form.get('salario')
    fecha_contratacion = request.form.get('fecha_contratacion')

    nuevo_empleado = agregar_empleado(nombre, apellido, salario, fecha_contratacion)

    return redirect("/empleados")



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
