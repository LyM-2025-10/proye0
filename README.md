# Proyecto 0 
## Participantes
### Sergio Alejandro Torres Melendez
### Julian Camilo Rivera Guzman

Este es un analizador sintáctico (parser) para un lenguaje de programación orientado a robots. El parser lee un 

archivo de entrada, analiza la sintaxis y verifica la corrección del código.

# Características

Lee el archivo de entrada y tokeniza el contenido.

Identifica declaraciones de variables, procedimientos y comandos.

Valida estructuras de control como if, while y repeat.

Verifica que el orden de los inputs de cada linea en el archivo cumpla con el lenguaje y detecta errores 

sintácticos en el código del robot.

# Estructura del Código

Parser: Clase principal que se encarga de analizar el código.

__init__(self, file_path): Inicializa el parser y carga el archivo de entrada.

next_word(self): Obtiene la siguiente palabra y avanza el índice.

match(self, expected): Verifica que la palabra actual sea la esperada.

parse(self): Procesa el input y valida la sintaxis.

parse_declaracion_variables(self): Procesa la declaración de variables.

parse_robot_command(self, word, dict1, dict2): Procesa comandos del robot.

parse_procedimiento(self): Procesa la declaración de procedimientos.

parse_main_block(self): Procesa el bloque principal.

parse_block(self, nombre): Procesa un bloque de código.

parse_statement(self, word, nombre): Procesa una sentencia.

parse_control_structure(self, keyword, dict1, dict2, dict3, dict4): Procesa estructuras de control.

parse_robot_while(self, dict1, dict2, dict3, dict4): Analiza bucles while.

parse_robot_if(self, dict1, dict2, dict3, dict4): Analiza estructuras condicionales if.

parse_robot_repeat(self, dict1, dict2): Analiza estructuras repeat.

# Uso

Ejecuta el parser: parser proyecto 0.py

Luego, introduce el nombre del archivo cuando se solicite.

Si el código es correcto, se mostrará: ¡Sintaxis correcta!

Si hay un error, se indicará el problema con un mensaje descriptivo.

# recomendaciones

Los archivos con un and solo los detecta si el and esta pegado a un mensaje, por ejemplo: andballons

