class Parser:
    def __init__(self, file_path):
        """Inicializa el parser y lee el archivo de entrada."""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                input_text = file.read()
        except FileNotFoundError:
            raise Exception(f"Error: No se pudo abrir el archivo '{file_path}'.")

        # Espaciamos los símbolos clave para facilitar el parsing
        for symbol in ["[", "]", ".", "|", ":=", ":", ","]:
            input_text = input_text.replace(symbol, f" {symbol} ")
        self.words = input_text.lower().split()
        self.index = 0
        self.variables = set()
        self.procedures = {}

    def next_word(self):
        """Obtiene la siguiente palabra y avanza el índice."""
        if self.index < len(self.words):
            word = self.words[self.index]
            self.index += 1
            return word
        return None

    def match(self, expected):
        """Verifica que la palabra actual sea la esperada y avanza."""
        if self.words[self.index] != expected:
            raise Exception(f"Error: Se esperaba '{expected}', pero se encontró '{self.words[self.index]}'.")

    def parse(self):
        """Procesa el input y valida la sintaxis."""
        while self.index < len(self.words):
            word = self.next_word()
            if word.isdigit():
                continue  # Ignorar números de línea
            elif word == "|":
                self.parse_declaracion_variables()
            elif word == "proc":
                self.parse_procedimiento()
            elif word == "[":
                self.parse_main_block()
            else:
                raise Exception(f"Error: palabra inesperada '{word}'.")

    def parse_declaracion_variables(self):
        """Procesa la declaración de variables globales o locales."""
        local_variables = set()
        while self.index < len(self.words):
            word = self.next_word()
            if word == "|":
                break
            local_variables.add(word)
        self.variables.update(local_variables)

    def parse_procedimiento(self):
        """Procesa la declaración de procedimientos."""
        nombre = self.next_word()
        params = []
        # Leer parámetros opcionales
        while self.words[self.index] not in ["["]:
            param = self.next_word()
            if param == ":":
                param = self.next_word()  # Obtener el nombre del parámetro
                params.append(param)
        self.procedures[nombre] = params
        self.match("[")
        self.parse_block()
        self.match("]")

    def parse_main_block(self):
        """Procesa el bloque principal fuera de los procedimientos."""
        self.parse_block()
        self.match("]")

    def parse_block(self):
        """Procesa un bloque de código dentro de corchetes."""
        word = self.next_word()
        while self.index < len(self.words):
            word = self.next_word()
            if word == "]":
                self.index -= 1  # Para que el corchete de cierre sea manejado correctamente
                break
            self.parse_statement(word)

    def parse_statement(self, word):
        """Procesa una sentencia dentro de un procedimiento o bloque."""
        print(word)
        if word in self.variables:
            self.match(":=")
            self.next_word()  # Valor de la asignación
            self.match(".")
        elif word in self.procedures:
            # Validar argumentos
            expected_params = self.procedures[word]
            for _ in range(len(expected_params)):
                param_value = self.next_word()
                if param_value.isdigit() or param_value in self.variables:
                    continue
                else:
                    raise Exception(f"Error: Parámetro inválido '{param_value}' en la llamada a '{word}'.")
            self.match(".")
        elif word in ["if:", "while:", "repeat:"]:
            self.parse_control_structure(word)
        elif word in ["move:", "turn:", "face:", "put:", "pick:", "goto:", "jump:", "nop"]:
            self.parse_robot_command(word)
        elif word in "|":
            self.parse_declaracion_variables()
        else:
            raise Exception(f"Error: Instrucción desconocida '{word}'.")

    def parse_control_structure(self, keyword):
        """Procesa estructuras de control como if, while, repeat."""
        self.next_word()  # Leer la condición o el número de repeticiones
        if keyword == "if:":
            self.match("then:")
        elif keyword == "repeat:":
            self.match("for:")
            self.next_word()  # Número de repeticiones
            self.match("repeat:")
        
        self.match("[")
        self.parse_block()
        self.match("]")

        if keyword == "if:":
            self.match("else:")
            self.match("[")
            self.parse_block()
            self.match("]")

    def parse_robot_command(self, command):
        """Procesa comandos del robot como mover, girar, etc."""
        while self.index < len(self.words):
            word = self.next_word()
            if word == ".":
                break
            if word in ["#", "ofType:", "inDir:", "toThe:", "with:"]:
                continue  # Son preposiciones válidas
            if word.isdigit() or word in self.variables:
                continue  # Valores numéricos o variables son válidos
            raise Exception(f"Error: Argumento inválido '{word}' en el comando '{command}'.")

if __name__ == "__main__":
    file_path = input("Ingrese el nombre del archivo de código: ")
    try:
        parser = Parser(file_path)
        parser.parse()
        print("¡Sintaxis correcta!")
    except Exception as e:
        print(f"Error: {e}")