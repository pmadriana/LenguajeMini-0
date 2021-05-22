
import time


class Produccion:

    def __init__(self, texto):
      
        split_result = texto.split(':=')
        self.left = split_result[0].strip()


        total_rules = split_result[1].split('|')
        self.right = [rule.strip() for rule in total_rules]

    def __str__(self):
        return self.left + ' := ' + str(self.right)

class Gramatica:
  
    producciones = []
    terminales = set()
    noterminales = []
    TablaSintactica = dict()
    siguientes = dict()
    arbol1 =[]
    arbol2 =[]
    

    def __init__(self):

        self.nInicial = None
        self.terminales.add('$') 

    def getProduccion(self, izq):
      
        ret_value = list()
        for produccion in self.producciones:
            if produccion.left.replace(' ', '') == izq:
                for right in produccion.right:
                    ret_value.append(right)
                
        return ret_value

    def getProducciones(self):
     
        producciones = list()
        for nodo in self.noterminales:
            producciones.append(self.getProduccion(nodo))
        return producciones

    def getTerminals(self):
      
        for produccion in self.producciones:
            cur_left = produccion.left.replace(' ','')
            if cur_left not in self.noterminales: 
                self.noterminales.append(cur_left)

         
            if cur_left in self.terminales:
                self.terminales.remove(cur_left)
            
            for cur_right in produccion.right:
                tokens = cur_right.strip().split(' ')
                for token in tokens:
                    if len(token) < 1:
                        continue
                
                    if token not in self.noterminales:
                        self.terminales.add(token)

    def getPrimero(self, izq): #devuelve individualmente el primer
        primeros = list()

 
        for produccion in self.producciones:
            if produccion.left.replace(' ', '') == izq:
                for right in produccion.right:
                    tokens = right.strip().split(' ')
                 
                    if tokens[0] in self.terminales:
                        primeros.append(tokens[0])
                 
                    else:
                        nt_primeros = self.getPrimero(tokens[0])
                        primeros = primeros + nt_primeros

        return primeros

    def getPrimeros(self): #devuelve el comjunto de primeros de toda la gramatica
        primeros = dict()
        for nodo in self.noterminales:
            cur_primeros = self.getPrimero(nodo)
            primeros[nodo] = cur_primeros

        return primeros

    def getSiguiente(self, izq):
           # produccioness = self.getProducciones()
        for produccion in self.producciones:
            for right in produccion.right:
                tokens = right.split(' ')
                for i in range(len(tokens)): 
                    if (tokens[i] == izq): 
                        if ( i == len(tokens)-1): #si es el ultimo se toma los siguietnes de produccion.left
                            if( tokens[i] != produccion.left): #si no es de la forma expr' -> + term expr'
                                for t in self.siguientes[produccion.left]: 
                                    #if(t not in self.siguientes[izq]):
                                        self.siguientes[izq].append(t)
                        else:
                            if (tokens[i+1] in self.terminales):
                               # if(tokens[i+1] not in self.siguientes[izq]):
                                    self.siguientes[izq].append(tokens[i+1])
                            else:
                                if( tokens[i+1] != produccion.left):
                                    primeros_temp = self.getPrimero(tokens[i+1])
                                    for j in primeros_temp:
                                        if(j == "lambda"):
                                            for t in self.siguientes[tokens[i+1]]: 
                                                #if(t not in self.siguientes[tokens[i+1]]):
                                                    self.siguientes[izq].append(t)   
                                        else:
                                           # if(j not in self.siguientes[izq]):
                                                self.siguientes[izq].append(j)
        print("Siguientes de "+ izq)
        print(self.siguientes[izq])
                                
    def getSiguientes(self):
        for noterminal in self.noterminales:
            self.siguientes[noterminal] = list()
        
        self.siguientes[self.nInicial].append('$')
        for nt in self.noterminales:
            self.getSiguiente(nt)   

    def cargar(self, texto):
        check_newlines = texto.split('\n')
      
        for word in check_newlines:
            if len(word) <= 1:
                continue
         
            produccion = Produccion(word)
            
            print(produccion.left)
            self.producciones.append(produccion)
            if (len(self.producciones) == 1):
                self.nInicial = produccion.left.strip()

        self.getTerminals()

    def __str__(self):
     
        return_string = ""
      
        for produccion in self.producciones:
            return_string += (produccion.left + " := ")
            for i in range(len(produccion.right)):
              
                if i == len(produccion.right) - 1:
                    return_string += (produccion.right[i])
                
                else:
                    return_string += (produccion.right[i]) + " | "
            return_string += '\n'

        return return_string

    
            

    
    def insertarTabla(self, noterminal, terminal, value):
        if noterminal not in self.TablaSintactica:
            self.TablaSintactica[noterminal] = dict()
            self.noterminales.add(noterminal)
        self.TablaSintactica[noterminal][terminal] = value
        self.terminales.add(terminal)

    def imprimirTabla(self):
    
        print(" ".ljust(self.PADDING), end = ' ')
      
        terminal_list = list(self.terminales)
        for term in terminal_list:
            print(term.ljust(self.PADDING), end = ' ')

        print()
      
        for non_term in list(self.noterminales):
            print(non_term.ljust(self.PADDING), end = ' ')
            for term in terminal_list:
                if term not in self.TablaSintactica[non_term]:
                    print(" ".ljust(self.PADDING), end = ' ')
                else:
             
                    produccion = ""
                    for value in self.TablaSintactica[non_term][term]:
                        produccion += value + " "
                    print(produccion.ljust(self.PADDING), end = ' ')
            print()

    def buscar_produccion(self, Nt, T):
        producciones = self.getProduccion(Nt)
        if len(producciones) == 1:
            return producciones[0]
        for produccion in producciones: 
            if T in produccion:
                return produccion

    def crearTabla(self):
        for Nt in self.noterminales:
            #init table
            for T in self.terminales:
                if Nt not in self.TablaSintactica:
                    self.TablaSintactica[Nt] = dict()
                self.TablaSintactica[Nt][T] = "-"

            for T in self.getPrimero(Nt):
                if T != 'lambda':
                    self.insertarTabla(Nt, T, self.buscar_produccion(Nt, T))
                else:
                    for T2 in self.siguientes[Nt]:
                        self.insertarTabla(Nt, T2,'lambda')

    def parser(self, tokens):
        self.arbol1.clear()
        self.arbol2.clear()
        
        tokens.append('$') 
        cont = 0
        i = 0
        token = tokens[0]
        stack = []
        stack.append('$')
        stack.append(self.noterminales[0])
        self.arbol1.append(self.noterminales[0])
        self.arbol2.append(0)
  
        actual = 0
        cont += 1
        tos = stack[len(stack)-1]
        print("Pila"+"        "+"Entrada"+"        "+"Adicionar")
        while(True):
            if (tos == '$' and token == '$'):
                return True
            elif(tos in self.terminales):
                linea=""
                for op in stack:
                        linea+=str(op)
                linea+="        "
                for op in range(i,len(tokens)):
                            linea+=str(tokens[op])
                linea+="        "  
                print(linea)
                if(tos == token):
                    stack.pop()
                    i += 1
                    token = tokens[i]
                    actual += 1
                elif(tos == "lambda"):
                    stack.pop()
                    actual += 1
                else:
                    print("error")
            else:
                if ( self.TablaSintactica[tos][token] != '-'):
                    stack.pop()
                    temp = self.TablaSintactica[tos][token]
                    linea=""
                    for op in stack:
                            linea+=str(op)
                    linea+="        "
                    for op in range(i,len(tokens)):
                            linea+=str(tokens[op])
                    linea+="        "  
                    linea+=temp
                    print(linea)
                    temp = temp.split(' ')
                  #  print(temp)
                    sumar=1
                    for j in temp:
                        #print("hola")
                        self.arbol1.insert(actual+sumar,j)
                        self.arbol2.insert(actual+sumar,self.arbol2[actual]+1)
                        sumar += 1
                    actual += 1
                    for j in reversed(temp):
                        stack.append(j)
            tos = stack[len(stack)-1]

    def imprimir_arbol(self):
        
        print()
        for ip in range(len(self.arbol1)):

            tempString=""
            
            for it in range(self.arbol2[ip]):
                tempString+="   "
            tempString+=self.arbol1[ip]+ " -> " + str(self.arbol2[ip])
            print(tempString)

    
        
           

def main():

    gramatica = Gramatica()
   
    gramatica.cargar("""
    E  := T Ep
    Ep := + T Ep | lambda
    T  := F Tp
    Tp := * F Tp | lambda
    F  := ( E ) | id

""")
  

    print(gramatica)

   
    print("-------------")

    print()


    print("no terminales", gramatica.noterminales)
    print("terminales", gramatica.terminales, '\n')

    #primeros = gramatica.getPrimero('F')
    primeros = gramatica.getPrimeros()
    print("PRIMEROS")
    for i in primeros:
        print(i + ":")
        print(primeros[i])
    
    print()
    print("SIGUIENTES")
    gramatica.getSiguientes()
    gramatica.crearTabla()


  #  gramatica.imprimirTabla()
    print()
    
    t = ["id","+","id","$"]
    #lineaTemp = "Int a(1)"
   # t = ["120@240"]
    #tokens = a_lexico.analizadorLexico(lineaTemp)
    #tempString = a_lexico.expandir(tokens)
    
    linea = 0

    gramatica.parser(t)
    gramatica.imprimir_arbol()

if __name__ == '__main__':
    main()
