import enum

class TipoToken(enum.Enum):
    PRIf = 1  
    PRElse = 2 
    PREnd = 3 
    PRWhile = 4 
    PRLoop = 5 
    PRFun=6 
    PRReturn=7 
    PRNew= 8 
    PRString = 9 
    PRInt = 10  
    PRChar = 11 
    PRBool = 12 
    PRTrue = 13 
    PRFalse = 14  
    PRAnd = 15 
    PROr= 16 
    PRNot = 17 
    OpRelMenor = 18  #<
    OpRelMenorIgual = 19 #<=  
    OpRelMayorIgual = 20  #>=
    OpRelMayor= 21  #>
    OpRelIgual = 22 #=
    OpRelDif = 23 #<>
    AbrePar = 24
    CierraPar = 25 
    OpAritMult = 26  
    OpAritDiv = 27
    OpAritSuma = 28
    OpAritSub = 29
    AbreCorchete = 30
    CierraCorchete = 31
    Coma = 32
    Asignar = 33 #:
    Var = 34 
    NumEnt = 35   
    Cadena = 36
    NL = 37 #\n
    Error = 38 #Agregue este tipo de token para que se asigne cuando es un error

class Token:
    nombre = TipoToken #tipotoken
    lexema = "" #string
    def __init__(self, nombre, lexema):
        self.nombre = nombre
        self.lexema = lexema
    
    def toString(self):
        temp =""
        temp += "<" + str(self.nombre)+" , "+str(self.lexema) + ">"
        return temp

class LectorDeArchivosTexto:
    def __init__(self):
        pass
    
    def Lector(self, filename):
        temp = open(filename,'r').read().split('\n')
        return temp



class AnalizadorLexico:
    
    operadoresArit = ["*", "/", "+", "-"]
    operadoresRela = ["<", ">", "="]
    parentesis = ["(", ")"]
    corchetes =["[", "]"]
    def __init__(self):
        pass

    def Variable(self, linea, idx):
        idx_temp = idx 
        lexema = ""
        while idx < len(linea) and linea[idx] not in self.operadoresArit and linea[idx] != " " and linea[idx]!= ":":
            lexema += linea[idx] 
            idx += 1

        tokenOF = Token(TipoToken.Var, lexema) 
        return tokenOF,idx
    
    def palabrasClave(self, linea, idx):
        idx_temp = idx 
        lexema = ""
        while idx < len(linea) and linea[idx].isalpha():
            lexema += linea[idx] 
            idx += 1

        c = lexema
        if c == "if" :
            tokenOF = Token(TipoToken.PRIf, c) 
        elif c == "else" :
            tokenOF = Token(TipoToken.PRElse, c) 
        elif c == "end" :
            tokenOF = Token(TipoToken.PREnd, c) 
        elif c == "while" :
            tokenOF = Token(TipoToken.PRWhile, c) 
        elif c == "loop" :
            tokenOF = Token(TipoToken.PRLoop , c) 
        elif c == "fun" :
            tokenOF = Token(TipoToken.PRFun, c) 
        elif c == "return" :
            tokenOF = Token(TipoToken.PRReturn, c) 
        elif c == "new" :
            tokenOF = Token(TipoToken.PRNew, c) 
        elif c == "string" :
            tokenOF = Token(TipoToken.PRString, c) 
        elif c == "int" :
            tokenOF = Token(TipoToken.PRInt, c) 
        elif c == "char" :
            tokenOF = Token(TipoToken.PRChar, c) 
        elif c == "bool" :
            tokenOF = Token(TipoToken.PRBool, c) 
        elif c == "true" :
            tokenOF = Token(TipoToken.PRTrue, c) 
        elif c == "false" :
            tokenOF = Token(TipoToken.PRFalse, c) 
        elif c == "and" :
            tokenOF = Token(TipoToken.PRAnd, c) 
        elif c == "or" :
            tokenOF = Token(TipoToken.PROr, c) 
        elif c == "not" :
            tokenOF = Token(TipoToken.PRNot, c) 
        else: 
            while idx < len(linea) and linea[idx] not in self.operadoresArit and linea[idx] != " " and linea[idx]!= ":":
                lexema += linea[idx] 
                idx += 1
            
            tokenOF = Token(TipoToken.Var, lexema)

       # idx += 1
        return tokenOF,idx

    def Numeros(self, linea, idx):
        idx_temp = idx 
        lexema = ""
        tipo = 0 #0 entero 1 real 2 error
        while idx < len(linea) and linea[idx].isdigit(): 
            lexema += linea[idx] 
            idx += 1
            
        if idx != len(linea):
            if linea[idx] == ".":
                lexema += linea[idx] 
                idx +=1
                tipo = 2
                while idx < len(linea) and linea[idx].isdigit(): 
                    tipo = 1
                    lexema += linea[idx] 
                    idx += 1
                 
                
        if tipo == 0: 
            tokenOF = Token(TipoToken.NumEnt, int(lexema)) 
        elif tipo == 1:
            tokenOF = Token(TipoToken.NumReal, lexema)  
        else:
            tokenOF = Token(TipoToken.Error, lexema) 

        return tokenOF,idx
    
    def operadorAritmetico(self, linea, idx):
        c = linea[idx]
        if c == "*" :
            tokenOF = Token(TipoToken.OpAritMult, c) 
        elif c == "/" :
            tokenOF = Token(TipoToken.OpAritDiv, c) 
        elif c == "+" :
            tokenOF = Token(TipoToken.OpAritSuma, c) 
        else: # c == "-" :
            tokenOF = Token(TipoToken.OpAritSub, c) 

        idx += 1
        return tokenOF,idx
    
    def operadorRelacional(self, linea, idx):
        lexema = ""
        tokenOF = Token
        c = linea[idx]
        lexema += linea[idx] 
        if c == "<" :
            idx += 1
            if idx != len(linea) and linea[idx] != " ":
                if linea[idx] == ">": #<>
                    lexema += linea[idx] 
                    tokenOF = Token(TipoToken.OpRelDif, lexema) 
                    idx += 1
                if linea[idx] == "=": #<=
                    lexema += linea[idx] 
                    tokenOF = Token(TipoToken.OpRelMenorIgual, lexema) 
                    idx += 1
            else: #<
                tokenOF = Token(TipoToken.OpRelMenor, lexema) 

        elif c == "=" :
            tokenOF = Token(TipoToken.OpRelIgual, lexema) 
            idx += 1
        elif c == ">" :
            idx += 1
            if idx != len(linea) and linea[idx] != " ":
                if linea[idx] == "=": #>=
                    lexema += linea[idx] 
                    tokenOF = Token(TipoToken.OpRelMayorIgual, lexema) 
                    idx += 1
            else: #>
                tokenOF = Token(TipoToken.OpRelMayor, lexema)
                
        else: # c == "-" :
            tokenOF = Token(TipoToken.Error, lexema) 
            idx += 1
        
        return tokenOF,idx
    
    def analizadorLexico(self, linea):
        tokens = list()
        index = 0
        while index < len(linea): #lee la linea por caracter

            if linea[index] == ":": #reconoce si es delimitador
                token = linea[index] 
                token_obj = Token(TipoToken.Asignar, token) 
                tokens.append(token_obj) 
                index += 1

            elif linea[index].isdigit(): #Si es un digito entonces llama a Numeros()
                token,index = self.Numeros(linea, index)
                tokens.append(token)

            elif linea[index].isalpha(): #Si es mayuscula llama a palabrasClave()
                token,index = self.palabrasClave(linea, index)
                tokens.append(token)

            elif linea[index].isalpha(): #Si es una letra llamo a variable()
                token,index = self.Variable(linea, index)
                tokens.append(token)
            
            elif linea[index] in self.operadoresArit: #Si esta en el array de operadoresArit
                token,index = self.operadorAritmetico(linea, index) #llamo a la funcion para saber cual es
                tokens.append(token)
            
            elif linea[index] in self.operadoresRela : 
                token,index = self.operadorRelacional(linea, index)
                tokens.append(token)
            
            elif linea[index] in self.parentesis:
                token = linea[index] 
                if linea[index] == "(":
                    token_obj = Token(TipoToken.AbrePar, token) 
                else:
                    token_obj = Token(TipoToken.CierraPar, token) 
                tokens.append(token_obj) 
                index += 1
            
            elif linea[index] in self.corchetes:
                token = linea[index] 
                if linea[index] == "[":
                    token_obj = Token(TipoToken.AbreCorchete, token) 
                else:
                    token_obj = Token(TipoToken.CierraCorchete, token) 
                tokens.append(token_obj) 
                index += 1
            
            elif linea[index] == ",": 
                token = linea[index] 
                token_obj = Token(TipoToken.Coma, token) 
                tokens.append(token_obj) 
                index += 1

            elif linea[index] == "%": #comentario, salto la linea
                index += len(linea)
            
            else: 
                index += 1 

        return tokens




lineas = LectorDeArchivosTexto().Lector("Parcial/prueba.txt")
lexico = AnalizadorLexico()
linea = 0
for linea in lineas:
    tokens = lexico.analizadorLexico(linea)
    for token in tokens:
        print (token.toString())


