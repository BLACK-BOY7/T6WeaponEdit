import os
import sys
import json
import sqlite3

from pathlib import Path
from tkinter import messagebox
from typing import List, Any, Dict, Union


def create_path( path: str ) -> str:
    """
    Verifica se o caminho existe e o cria se não existir, e retorna o caminho absoluto.
    """
    # Transforma o caminho em um caminho absoluto
    path = os.path.abspath(path)

    # Verifica se o caminho não existe e o cria se necessário
    os.makedirs(path, exist_ok=True)

    # Retorna o caminho absoluto
    return path


def resource_path( relative_path: str ) -> str:
    if hasattr( sys, '_MEIPASS' ):
        return os.path.join( sys._MEIPASS, relative_path )
    return os.path.join( Path( __file__ ).parent.resolve(), relative_path )


def validate_input_fields( cost: str, costUp: str, costReUp: str, alias: str, roundUnlock: str, limit: str, killsUnlock: str, hsUnlock: str ) -> bool:
    if limit == None or limit == "":
        limit = "null"
    
    if roundUnlock == None or roundUnlock == "":
        roundUnlock = "null"
        
    if killsUnlock == None or killsUnlock == "":
        killsUnlock = "null"

    if hsUnlock == None or hsUnlock == "":
        hsUnlock = "null"

    if not cost:
        messagebox.showerror("Cost", "Você precisa prencher o campo Cost!")
        return True

    if not costUp:
        messagebox.showerror("Cost Up", "Você precisa prencher o campo Cost Up!")
        return True

    if not costReUp:
        messagebox.showerror("Cost Re-Up", "Você precisa prencher o campo Cost Re-Up!")
        return True
    
    if not alias:
        messagebox.showerror("Alias", "Você precisa prencher o campo Alias!")
        return True
    
    if not roundUnlock:
        messagebox.showerror("Round Unlock", "Você precisa prencher o campo Round Unlock!")
        return True

    if not limit:
        messagebox.showerror("Limit Round", "Você precisa prencher o campo Limit Round!")
        return True

    if not killsUnlock:
        messagebox.showerror("Kills Unlock", "Você precisa prencher o campo Kills Unlock!")
        return True

    if not hsUnlock:
        messagebox.showerror("Hs Unlock", "Você precisa prencher o campo Hs Unlock!")
        return True
    
    return False


def alias_( alias: str ) -> str:
    alias_array = alias.strip().strip(",").split(",")
    size = len( alias_array )
    alias = ""

    for numero, string in enumerate(alias_array):
        if numero < size -1 :
            alias += string.strip() + ","
            continue

        alias += string.strip()

    return alias


def cost_( cost: str ) -> Union[ str, int ]:
    if cost != "null":
        return int(cost)
    else:
        return cost


def add_weapon_database( className: str, nameid: str, nameString: str, alias, cost: str, costUp: str, costReUp: str, limitRound: str, roundUnlock: str, killsUnlock: str, hsUnlock: str ) -> None:
    if validate_input_fields(cost, costUp, costReUp, alias, roundUnlock, limitRound, killsUnlock, hsUnlock): # Adicionar base de dados de armas
        # caso de error dou um return para o bank de dados nem ser aberto.
        return
    
    if limitRound == None or limitRound == "":
        limitRound = "null"
    
    if roundUnlock == None or roundUnlock == "":
        roundUnlock = "null"
        
    if killsUnlock == None or killsUnlock == "":
        killsUnlock = "null"

    if hsUnlock == None or hsUnlock == "":
        hsUnlock = "null"

    alias = alias_(alias)

    connect = sqlite3.connect(create_path("file") + "/weapons.db") # Faço a conexão com o banco de dados, É caso ele não exista é criador um banco de dados. 

    cursor = connect.cursor() # Usor um Cursor para assim pode manipula os dados do banco ou para adicionar mais coisas ao mesmo.

    cursor.execute("""CREATE TABLE IF NOT EXISTS weapons( 
                    className text, nameId text PRIMARY KEY, nameString text, cost INTEGER, costUp text, costReUp text, limitRound text, 
                    roundUnlock text, killsUnlock text, hsUnlock text, alias text)""") # isso so vai acontece uma vez, que é a criação da tabela de weapons.
    
    try:
        cursor.execute("""INSERT INTO weapons(
                        className, nameid, nameString, cost, costUp, costReUp, limitRound, roundUnlock, killsUnlock, hsUnlock, alias) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,(className, nameid, nameString, cost, costUp, costReUp, limitRound, roundUnlock, killsUnlock, hsUnlock, alias)) #Coloca Os Dados No Banco De Dados.
    except sqlite3.IntegrityError:
        messagebox.showerror("weapon", "Esta arma já esta adicionada ao banco de dados.\n Ultilizar o outro modo para editá-la")
        #Estou a fecha para impidir problema de vazamento de dados, ou de ocupa espaço na memoria.
        cursor.close()
        connect.close()
        return

    cursor.close() # Fechando o cursor para evitar vazamento de recursos

    # vou usar nos try caso ocorrar algum error e claro.
    # connect.rollback() O rollback é uma forma de garantir a integridade dos dados do banco de dados em caso de erro ou problemas durante as transações.

    connect.commit() # Confirma as alterações realizadas na conexão ao banco de dados
    connect.close() # Encerra a conexão com o banco de dados

    messagebox.showinfo("Weapon", "Weapon Adicionada ao banco de dados com sucesso.")


def get_weapons_by_class_from_database( class_name: str ) -> List[str]: # obter armas por classe na base de dados
    connect = sqlite3.connect(create_path("file") + "/weapons.db") # Faço a conexão com o banco de dados, É caso ele não exista é criador um banco de dados. 

    cursor = connect.cursor() # Usor um Cursor para assim pode manipula os dados do banco ou para adicionar mais coisas ao mesmo.

    result = cursor.execute("SELECT nameString FROM weapons WHERE className=?", (class_name,)).fetchall() # O método fetchall() retorna uma lista contendo todas as linhas do resultado da consulta. Se não houver nenhuma linha, ele retorna uma lista vazia.

    cursor.close() # Fechando o cursor para evitar vazamento de recursos.
    connect.close() # Encerra a conexão com o banco de dados.

    weapon_names = [row[0] for row in result] # adiciona apenas os nomes das armas a uma lista
    return weapon_names #retun uma lista de armas.


def get_available_class_from_database() -> List[str]: # obter classe disponível na base de dados
    connect = sqlite3.connect(create_path("file") + "/weapons.db")
    cursor = connect.cursor()

    # Seleciona apenas o nome da coluna "className" e utiliza a cláusula DISTINCT para retornar somente valores únicos
    result = cursor.execute("SELECT DISTINCT className FROM weapons").fetchall() #Essa consulta seleciona todas as linhas da tabela weapons e retorna apenas os valores distintos encontrados na coluna className.

    cursor.close()
    connect.close()

    # Transforma a lista de tuplas retornada pelo fetchall em uma lista simples contendo apenas os nomes das classes
    return [row[0] for row in result]


def get_data_from_database_by_weaponName( weapon_name: str ) -> Dict[ str, str ] : # obter dados da base de dados por nome de arma. que seria a linha completa do nome dessa arma.
    connect = sqlite3.connect(create_path("file") + "/weapons.db") # Faço a conexão com o banco de dados, É caso ele não exista é criador um banco de dados. 

    cursor = connect.cursor() # Usor um Cursor para assim pode manipula os dados do banco ou para adicionar mais coisas ao mesmo.

    result = cursor.execute("SELECT * FROM weapons WHERE nameString=?", (weapon_name,)).fetchone() # O método fetchone() retorna a próxima linha do resultado da consulta como uma tupla. Se todas as linhas já tiverem sido retornadas, ele retorna None.

    columns = [col[0] for col in cursor.description] # lista de nomes de colunas cursor.description é uma propriedade que retorna uma lista de tuplas, onde cada tupla descreve uma coluna na consulta SQL executada. Cada tupla contém informações sobre a coluna, como nome, tipo de dados, comprimento máximo etc.
    result_dict = dict(zip(columns, result)) # transforma resultado em um dicionário, zip se columns for ['name', 'cost', 'limitRound'] e result for ('m1911_zm', 500, 'null'), zip(columns, result) resultaria na sequência de tuplas (('name', 'm1911_zm'), ('cost', 500), ('limitRound', 'null')). dict() cria um dicionário a partir da sequência de tuplas, em que cada tupla é interpretada como um par chave-valor.

    cursor.close() # Fechando o cursor para evitar vazamento de recursos.
    connect.close() # Encerra a conexão com o banco de dados.

    return result_dict # retorna um array com chaves.


def update_data_from_database( nameId: str, alias, cost: str, costUp: str, costReUp: str, limitRound: str, roundUnlock: str, killsUnlock: str, hsUnlock: str ) -> None:
    if validate_input_fields(cost, costUp, costReUp, alias, roundUnlock, limitRound, killsUnlock, hsUnlock): # Adicionar base de dados de armas
        # caso de error dou um return para o bank de dados nem ser aberto.
        return
    
    if limitRound == None or limitRound == "":
        limitRound = "null"
    
    if roundUnlock == None or roundUnlock == "":
        roundUnlock = "null"
        
    if killsUnlock == None or killsUnlock == "":
        killsUnlock = "null"

    if hsUnlock == None or hsUnlock == "":
        hsUnlock = "null"

    alias = alias_(alias)
    
    connect = sqlite3.connect(create_path("file") + "/weapons.db")

    cursor = connect.cursor()

    cursor.execute("""UPDATE weapons
                    SET cost = ?, costUp = ?, costReUp = ?, limitRound = ?, roundUnlock = ?, killsUnlock = ?, hsUnlock = ?, alias = ?
                    WHERE nameId = ?""", (cost, costUp, costReUp, limitRound, roundUnlock, killsUnlock, hsUnlock, alias, nameId))
    
    cursor.close()

    connect.commit()
    connect.close()

    messagebox.showinfo("Update Weapon", "Weapon Atualizada com sucesso!")


def has_weapon_in_database( text: str, messagem: bool=True ) -> bool: # Tem arma na base de dados
    if not os.path.exists(create_path("file") + "/weapons.db"):
        messagebox.showerror("file", "Você ainda não criou nem uma arma! Você Sera redirecionador para \"Create Weapon\"")
        return False

    try:
        connect = sqlite3.connect(create_path("file") + "/weapons.db")
        cursor = connect.cursor()

        # Execute uma query SQL para selecionar todas as linhas da tabela desejada.
        rows = cursor.execute("SELECT * FROM weapons LIMIT 1").fetchone() # Seleciona a tabela weapons e pego a primeira linha usando o LIMIT 1, que especifica para fetchone().

        cursor.close()
        connect.close()

        # Verifica se a primeira linha existe.
        if rows:
            return True
        elif not rows and messagem:
            messagebox.showerror("weapons", f"Nem uma arma encontrada para {text}!")
            return False

    except sqlite3.Error:
        messagebox.showerror("weapons", "Erro ao tentar acessar o banco de dados!")
        return False


def export_database_to_json() -> None: # Base de dados de exportação para a json
    if not has_weapon_in_database("Exporta!"):
        return
    
    connect = sqlite3.connect(create_path("file") + "/weapons.db")

    cursor = connect.cursor()

    data_base = cursor.execute("SELECT * FROM weapons")

    weapons = data_base.fetchall()

    columns = [description[0] for description in data_base.description]

    # Criar uma lista de dicionários para cada linha
    try:
        rows_list = {}
        for row in weapons:
            row_dict = {} 

            for i in range( len(columns) ):
                if columns[i] == "alias":
                    alias = row[i] # type: str
                    row_dict[columns[i]] = alias.split(",")
                    continue

                if columns[i] in ["costUp","costReUp","limitRound","roundUnlock","killsUnlock","hsUnlock"]:
                    row_dict[columns[i]] = cost_(row[i])
                    continue

                row_dict[columns[i]] = row[i]

            rows_list[ row_dict["nameId"] ] = row_dict

        with open( "weapons_list.json", "w" ) as file:
            json.dump( rows_list, file, indent=4 )

        if messagebox.askyesno("json", "Arquivo \"json\" criado com sucesso deja abrir?"):
            os.startfile( "weapons_list.json" )

    except:
        messagebox.showerror("Error","error do além!")


def delete_weapon_by_database( weapon_name: str ) -> None:
    if not(has_weapon_in_database("Deleta")):
        return

    connect = sqlite3.connect(create_path("file") + "/weapons.db")
    
    cursor = connect.cursor()

    cursor.execute("DELETE FROM weapons WHERE nameString = ?", (weapon_name,))
    cursor.close()

    connect.commit()
    connect.close()

    messagebox.showinfo("Weapon Delete", f"Arma {weapon_name} deletada com sucesso!")


def add_server( name: str, password: str, ip: str, port: str ) -> None:
    __file__name__ = Path( resource_path( "file\\Servers.db" ) )

    connect = sqlite3.connect( __file__name__ )

    cursor = connect.cursor()

    cursor.execute( """CREATE TABLE IF NOT EXISTS servers( name text PRIMARY KEY, password, ip, port )""" )

    try:
        cursor.execute( """INSERT INTO servers( name, password, ip, port ) VALUES( ?, ?, ?, ? )""",( name, password, ip, port ) )

    except sqlite3.IntegrityError():
        messagebox.showerror( "Server", "Este nome de servidor já existe" )
        cursor.close()
        connect.close()
        return

    cursor.close()

    connect.commit()
    connect.close()

    messagebox.showinfo( "Server", "Servidor adicionado com sucesso!" )


def create_table_to_servers() -> None:
    __file__name__ = Path( resource_path( "file\\Servers.db" ) )

    connect = sqlite3.connect( __file__name__ )

    cursor = connect.cursor()

    cursor.execute( """CREATE TABLE IF NOT EXISTS servers( name text PRIMARY KEY, password, ip, port )""" )

    cursor.close()
    connect.commit()


def get_servers() -> Dict[ str, str ]:
    __file__name__ = Path( resource_path( "file\\Servers.db" ) )

    create_table_to_servers() # chama essa função para criar a tanto o arquivo quanto a tabela servers

    connect = sqlite3.connect( __file__name__ )

    cursor = connect.cursor()

    results = cursor.execute( "SELECT * FROM Servers" ).fetchall()

    result_dict = {} # type: Dict[ str, str ]

    for result in results:
        key = result[0]
        valores = {
            "name": key,
            "password": result[1],
            "ip": result[2],
            "port": result[3]
        }

        result_dict[key] = valores

    cursor.close()
    connect.close()

    return result_dict


def delete_serve( name: str ) -> None:
    __file__name__ = Path( resource_path( "file\\Servers.db" ) )

    connect = sqlite3.connect( __file__name__ )

    cursor = connect.cursor()

    cursor.execute( "DELETE FROM servers WHERE name=?", ( name, )  )
    cursor.close()

    connect.commit()
    connect.close()


# if __name__ == "main":
#     export_database_to_json()
    # add_weapon_database("Lmgs", "lsat_zm", "LSAT", "LS,LSTA","222" )
