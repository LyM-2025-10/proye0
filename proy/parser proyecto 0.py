class Parser:
    def __init__(self, file_path):
        """Inicializa el parser y lee el archivo de entrada."""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                input_text = file.read()
        except FileNotFoundError:
            raise Exception(f"Error: No se pudo abrir el archivo '{file_path}'.")

        # Espaciamos los símbolos clave para facilitar el parsing
        for symbol in ["[", "]", ".", "|", ","]:
            input_text = input_text.replace(symbol, f" {symbol} ")
        self.words = input_text.lower().split()
        veces = self.words.count(".")
        for i in range(0, len(self.words)-veces):
            if self.words[i] == ".":
                self.words.pop(i)
        self.index = 0
        self.variables = []
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
            elif self.index == len(self.words):
                break
            else:
                raise Exception(f"Error: palabra inesperada '{word}'.")

    def parse_declaracion_variables(self):
        """Procesa la declaración de variables globales o locales."""
        while self.index < len(self.words):
            word = self.next_word()
            if word == "|":
                break
            if word != ",":
                self.variables.append(word)

    
    def parse_robot_command(self, word, dict1, dict2):
        """Procesa comandos del robot como mover, girar, etc."""
        while self.index < len(self.words):
            if word in ["face:", "turn:"]:  
                valor = self.next_word()
                if not valor in dict2[word]:
                    raise Exception(f"Error: Argumento inválido '{valor}' en el comando '{word}'.")
                break
            elif word == "nop":
                self.index += 1
                break
            valor = self.next_word()
            if not valor.isdigit() and not valor in self.variables:
                raise Exception(f"Error: Parámetro inválido '{valor}' en la llamada a '{word}'.")
            valor1 = self.next_word()
            if valor1 not in dict1[word]:
                raise Exception(f"Error: Argumento inválido '{valor1}' en el comando '{word}'.")
            valor2 = self.next_word()
            if valor2 in dict2:
                self.index -= 1
                break
            elif valor2 == "]":
                break
            if word in ["jump:", "move:"]:
                if valor1 == dict1[word][0]:
                    if not valor2 in dict2[word][0:4]:
                        raise Exception(f"Error: Argumento inválido '{valor2}' en el comando '{word}'.")
                elif valor1 == dict1[word][1]:
                    if not valor2 in dict2[word][4:8]:
                        raise Exception(f"Error: Argumento inválido '{valor2}' en el comando '{word}'.")
            elif word == "goto:":
                if not valor2.isdigit() and not valor2 in self.variables:
                    raise Exception("Error: Argumento inválido '{valor2}' en el comando '{word}'.")
            else: 
                if valor2 not in dict2[word]:
                    raise Exception(f"Error: Argumento inválido '{valor2}' en el comando '{word}'.")
            valor = self.next_word()
            if valor != "]":
                self.index -= 1
            break
        
    def parse_procedimiento(self):
        """Procesa la declaración de procedimientos."""
        nombre = self.next_word()
        params = []
        # Leer parámetros opcionales
        while self.words[self.index] not in ["["]:
            param = self.next_word()
            if ":" not in param:    #  Obtener el nombre del parámetro
                params.append(param)
        self.procedures[nombre] = params
        self.match("[")
        self.parse_block(nombre)
        self.match("]")
        self.index += 1

    def parse_main_block(self):
        """Procesa el bloque principal fuera de los procedimientos."""
        self.index -= 1
        self.parse_block("a")
        self.match("]")

    def parse_block(self, nombre):
        """Procesa un bloque de código dentro de corchetes."""
        word = self.next_word()
        while self.index < len(self.words):
            word = self.next_word()
            if word == "]":
                self.index -= 1  # Para que el corchete de cierre sea manejado correctamente
                break
            self.parse_statement(word, nombre)

    def parse_statement(self, word, nombre):
        """Procesa una sentencia dentro de un procedimiento o bloque."""
        dict1 = {"put:": "oftype:", "pick": "oftype:", "move:": ["tothe:", "indir:"], "jump:": ["tothe:", "indir:"], "goto:": "with:"}
        dict2 = {"put:": ["#balloons", "#chips"], "pick:": ["#balloons", "#chips"], "move:": ["#front", "#right", "#left", "#back"
                ,"#north", "#south", "#west", "#east"], "jump:": ["#front", "#right", "#left", "#back", "#north", "#south", "#west", "#east"],
                "turn:": ["#left", "#right", "#around"], "face:": ["#north", "#south", "#west", "#east"]
                }
        dict3 = {"canput:": "oftype:", "canpick:": "oftype:", "canmove:": ["tothe:", "indir:"], "canjump:": ["tothe:", "indir:"]}
        dict4 = {"canput:": ["#balloons", "#chips"], "canpick:": ["#balloons", "#chips"], "canmove:": ["#front", "#right", "#left", "#back"
                ,"#north", "#south", "#west", "#east"], "canjump:": ["#front", "#right", "#left", "#back", "#north", "#south", "#west", "#east"],
                "canturn:": ["#left", "#right", "#around"], "facing:": ["#north", "#south", "#west", "#east"]
                }
        if word in self.variables:
            self.match(":=")
            self.index += 1
            valor = self.next_word()  # Valor de la asignación
            llave = list(self.procedures)[0]
            lista_param = self.procedures[llave]
            if valor not in lista_param:
                raise Exception(f"variable invalida") 
        elif word in ["move:", "turn:", "face:", "put:", "pick:", "goto:", "jump:", "nop"]:
            # Validar argumentos
            if nombre in self.procedures:
                if self.procedures[nombre] == []:
                    self.parse_robot_command(word, dict1, dict2)
                else:
                    lista_param = self.procedures[nombre]
                    for i in range(0, len(lista_param)):
                        if self.words[self.index] == word:
                            self.index += 1
                        self.parse_robot_command(word, dict1, dict2)
                    self.index -= 1
            else:
                self.parse_robot_command(word, dict1, dict2)
        elif word in ["putchips:", "putballoons:", "pickchips:", "pickballoons:"]:
            valor = self.next_word()
            if not valor.isdigit():
                raise Exception("no se reconoce el valor", valor)
            self.index += 1
            valor = self.next_word()
            if not valor.isdigit():
                raise Exception("no se reconoce el valor", valor)
            valor = self.next_word()
            if valor == "]":
                self.index -= 1
        elif word in ["if:", "while:", "repeat:"]:
            self.parse_control_structure(word, dict1, dict2, dict3, dict4)
        elif word in "|":
            self.parse_declaracion_variables()
        else:
            raise Exception(f"Error: Instrucción desconocida '{word}'.")

    def parse_control_structure(self, keyword, dict1, dict2, dict3, dict4):
        """Procesa estructuras de control como if, while, repeat."""
        if keyword == "while:":
            self.parse_robot_while(dict1, dict2, dict3, dict4)
        elif keyword == "if:":
            self.parse_robot_if(dict1, dict2, dict3, dict4)
        elif keyword == "for:":
            self.parse_robot_repeat(dict1, dict2)
        self.match("]")
            
    def parse_robot_while(self, dict1, dict2, dict3, dict4):
        while self.index < len(self.words):
            word = self.next_word()
            if word in ["facing:", "not:"]:
                valor = self.next_word()
                if word == "facing:":
                    if not valor in dict4[word]:
                        raise Exception(f"Error: Argumento inválido '{valor}' en el comando '{word}'.")
                self.index += 1
                self.match("do")
                self.index += 2
                word1 = self.next_word()
                self.parse_robot_command(word1, dict1, dict2)
                break
            if word not in dict3:
                raise Exception("condicional", word, "no reconocido")
            valor = self.next_word()
            if valor not in self.variables and not valor.isdigit():
                raise Exception("valor", valor, "no reconocido")
            valor1 = self.next_word()
            if valor1 not in dict3[word]:
                raise Exception("expresion", valor1, "no reconocido")
            valor2 = self.next_word()
            if word in ["canjump:", "canmove:"]:
                if valor1 == dict3[word][0]:
                    if not valor2 in dict4[word][0:4]:
                        raise Exception(f"Error: Argumento inválido '{valor2}' en el comando '{word}'.")
                elif valor1 == dict3[word][1]:
                    if not valor2 in dict4[word][4:8]:
                        raise Exception(f"Error: Argumento inválido '{valor2}' en el comando '{word}'.")
            elif valor2 not in dict4[word]:
                raise Exception("expresion", valor2, "no reconocido")
            self.match("do:")
            self.index += 3
            self.parse_robot_command(word[3:len(word)], dict1, dict2)
            break
    def parse_robot_if(self, dict1, dict2, dict3, dict4):
        while self.index < len(self.words):
            word = self.next_word()
            if word in ["facing:", "not:"]:
                valor = self.next_word()
                if word == "facing:":
                    if not valor in dict4[word]:
                        raise Exception(f"Error: Argumento inválido '{valor}' en el comando '{word}'.")
                self.index += 1
                self.match("then")
                self.index += 2
                word1 = self.next_word()
                self.parse_robot_command(word1, dict1, dict2)
                self.match("else:")
                self.index += 2
                word2 = self.next_word()
                self.parse_robot_command(word2, dict1, dict2)
            if word not in dict3:
                raise Exception("condicional", word, "no reconocido")
            valor = self.next_word()
            if valor not in self.variables and not valor.isdigit():
                raise Exception("valor", valor, "no reconocido")
            valor1 = self.next_word()
            if valor1 not in dict3[word]:
                raise Exception("expresion", valor1, "no reconocido")
            valor2 = self.next_word()
            if word in ["canjump:", "canmove:"]:
                if valor1 == dict3[word][0]:
                    if not valor2 in dict4[word][0:4]:
                        raise Exception(f"Error: Argumento inválido '{valor2}' en el comando '{word}'.")
                elif valor1 == dict3[word][1]:
                    if not valor2 in dict4[word][4:8]:
                        raise Exception(f"Error: Argumento inválido '{valor2}' en el comando '{word}'.")
            elif valor2 not in dict4[word]:
                raise Exception("expresion", valor2, "no reconocido")
            self.match("then:")
            self.index += 3
            self.parse_robot_command(word[3:len(word)], dict1, dict2)
            self.match("else:")
            self.index += 2
            word2 = self.next_word()
            self.parse_robot_command(word2, dict1, dict2)
            break
        
    def parse_robot_repeat(self, dict1, dict2):
         while self.index < len(self.words):
            valor = self.next_word()
            if valor not in self.variables and not valor.isdigit():
                raise Exception("valor", valor, "no reconocido")
            self.match("repeat:")
            self.index += 2
            word = self.next_word()
            self.parse_robot_command(word, dict1, dict2)
            break
            
if __name__ == "__main__":
    file_path = input("Ingrese el nombre del archivo de código: ")
    try:
        parser = Parser(file_path)
        parser.parse()
        print("¡Sintaxis correcta!")
    except Exception as e:
        print(f"{e}")
        