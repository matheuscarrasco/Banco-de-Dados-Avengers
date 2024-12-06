from string import capwords
from model.vingador import Vingador
from os import system
from model.database import Database
 
class Interface:
 
 
    def __init__(self):
        Vingador.carregar_herois()
        self.menu_principal()
 
    def menu_principal(self):
        self.exibe_titulo_app()
        while True:
            self.exibe_titulo("Menu Principal")
            print("1 - Cadastrar Vingador")
            print("2 - Listar Vingadores")
            print("3 - Convocar Vingador")
            print("4 - Aplicar Tornozeleira")
            print("5 - Aplicar Chip GPS")
            print("6 - Listar Detalhes do Vingador")
            print("7 - Emitir Mandado de Prisão")
            print("0 - Sair", end="\n\n")
            opcao = input("Digite a opção desejada: ")
 
            if opcao == '1':
                self.exibe_titulo_app()
                self.exibe_titulo("<< Cadastro de Vingador")
                self.cadastrar_vingador()
                self.aguardar_enter()
            elif opcao == '2':
                self.exibe_titulo_app()
                self.exibe_titulo("<< Lista de Vingadores")
                Vingador.listar_vingadores()
                self.aguardar_enter()
            elif opcao == '3':
                self.exibe_titulo_app()
                self.exibe_titulo("<< Convocação de Vingador")
                self.convocar_vingador()
                self.aguardar_enter()
            elif opcao == '4':
                self.exibe_titulo_app()
                self.exibe_titulo("<< Aplicação de Tornozeleira")
                self.aplicar_tornozeleira()
                self.aguardar_enter()
            elif opcao == '5':
                self.exibe_titulo_app()
                self.exibe_titulo("<< Aplicação de Chip GPS")
                self.aplicar_chip_gps()
                self.aguardar_enter()
            elif opcao == '6':
                self.exibe_titulo_app()
                self.exibe_titulo("<< Listar Detalhes do Vingador")
                self.listar_detalhes_vingador()
                self.aguardar_enter()
            elif opcao == '7':
                self.exibe_titulo_app()
                self.exibe_titulo("<< Emitir Mandato de Prisão")
                self.mandado_prisao()
                self.aguardar_enter()
            elif opcao == '0':
                exit()
            else:
                print("Opção inválida.")
                self.aguardar_enter()
                self.menu_principal()
 
    def cadastrar_vingador(self):
        nome_heroi = input("Nome do herói: ")
        nome_real = input("Nome real: ")
        categoria = input("Categoria: ").capitalize()
        poderes = input("Poderes (separados por vírgula): ").split(',')
        poder_principal = input("Poder Principal: ")
        fraquezas = input("Fraquezas: (separadas por vírgula): ").split(',')
        nivel_forca = int(input("Nível de Força: "))
 
 
       
        try:
            db = Database()
            db.connect()
 
            query = "INSERT INTO heroi (nome_heroi, nome_real, categoria, poderes, poder_principal, fraquezas, nivel_forca) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            values = (nome_heroi, nome_real, categoria, ', ' .join(poderes), poder_principal, ', '.join(fraquezas), nivel_forca)
 
            cursor = db.execute_query(query, values)
 
            Vingador(cursor.lastrowid, nome_heroi, nome_real, categoria, poderes, poder_principal, fraquezas, nivel_forca)
        except Exception as e:
            print('Erro ao salvar vingador no banco de dados: {e}')
        finally:
            db.disconnect()
 
        print(f"Vingador(a) '{nome_heroi}' cadastrado com sucesso.")
        self.aguardar_enter()
 
    def aguardar_enter(self):
        input("\nPressione Enter para continuar...")
        self.menu_principal()
 
    def convocar_vingador(self):
 
        nome_heroi = input("Nome do herói: ")
        for vingador in Vingador.lista_vingadores:
            if nome_heroi in vingador.nome_heroi or nome_heroi in vingador.nome_real:
                try:
                    db = Database()
                    db.connect()
 
                    motivo = capwords(input("motivo: "))
                    status = capwords(input("status (Pendente, Compareceu, Ausente): "))
                    opcoes_validas = ["Pendente", "Ausente","Compareceu"]
                     
                    if status not in opcoes_validas:
                        print(f'Opção "{status}" inválida. Opções válidas {', '.join(opcoes_validas)}.\n faça a convocação novamente')
                        self.aguardar_enter()
                        return
                   
                    if nome_heroi in vingador.nome_heroi or nome_heroi in vingador.nome_real:
                   
                        query = f"Select heroi_id from heroi where (nome_heroi like '%{nome_heroi}%') or (nome_real like '%{nome_heroi}%') limit 1"
                        heroi_id = db.select(query)
 
                        query = "INSERT INTO convocacao (heroi_id, nome_heroi, motivo,status) VALUES (%s,%s,%s,%s)"
                        values = (int(heroi_id[0][0]), nome_heroi,motivo, status)
                        db.execute_query(query, values)
                   
                                           
                except Exception as e:
                    print('Erro ao convocar Vingador: {e}')
                finally:
                    db.disconnect()
 
                print(vingador.convocar())
                self.aguardar_enter()
                return
           
       
        print(f"Vingador(a) '{nome_heroi}' não encontrado.")
        self.aguardar_enter()
 
 
    def aplicar_tornozeleira(self):
 
        nome_heroi = input("Nome do herói: ")
        for vingador in Vingador.lista_vingadores:
            if nome_heroi in vingador.nome_heroi or nome_heroi in vingador.nome_real:
                try:
                    status = input("status (Inativa, Ativa): ")
                    opcoes_validas = ["Ativa", "Inativa"]
                     
                    if status not in opcoes_validas:
                        print(f'Opção "{status}" inválida. Opções válidas {', '.join(opcoes_validas)}.\n faça a seleção novamente')
                        self.aguardar_enter()
                        return
                       
                   
 
                    if nome_heroi in vingador.nome_heroi or nome_heroi in vingador.nome_real:
                        db = Database()
                        db.connect()
                        query = f"Select heroi_id from heroi where (nome_heroi like '%{nome_heroi}%') or (nome_real like '%{nome_heroi}%') limit 1"
                        heroi_id = db.select(query)
                       
 
                        query = "INSERT INTO tornozeleira (heroi_id, nome_heroi, status) VALUES (%s,%s,%s)"
                        values = (int(heroi_id[0][0]), nome_heroi, status)
                        db.execute_query(query, values)
 
                                           
                except Exception as e:
                    print(f'Erro ao colocar tornozeleira: {e}')
                    self.aguardar_enter()
                finally:
                    db.disconnect()
                self.aguardar_enter()
                return
                   
        print(f'Vingador(a) "{nome_heroi}" não encontrado')
        self.aguardar_enter()
               
 
    def aplicar_chip_gps(self):
        nome_heroi = capwords(input("Nome do herói: "))
        for vingador in Vingador.lista_vingadores:
            if nome_heroi in vingador.nome_heroi or nome_heroi in vingador.nome_real:
                try:
                   
                    localizacao_atual = capwords(input("localização atual: "))
                    ultima_localizacao = capwords(input("última localização : "))
                   
                    db = Database()
                    db.connect()
 
                    query = f"Select heroi_id from heroi where (nome_heroi like '%{nome_heroi}%') or (nome_real like '%{nome_heroi}%') limit 1"
                   
                    heroi_id = db.select(query) #retorna uma lista de tuplas
                    heroi_id = int(heroi_id[0][0])
 
                    # if heroi_id == vingador.heroi_id:
                    query = f"select id_tornozeleira from tornozeleira where (heroi_id like '%{heroi_id}%') limit 1"
                   
                    id_tornozeleira = db.select(query)
                    id_tornozeleira = int(id_tornozeleira[0][0])
               
                    query = "INSERT INTO chip_gps (heroi_id, id_tornozeleira, localizacao_atual, ultima_localizacao) VALUES (%s,%s,%s,%s)"
 
                    values = (heroi_id, id_tornozeleira, localizacao_atual, ultima_localizacao)
                    db.execute_query(query, values)
 
                except Exception as e:
                    print(f'Erro ao colocar tornozeleira: {e}')
                    self.aguardar_enter()
                finally:
                    db.disconnect()
                self.aguardar_enter()
                return
           
                print(vingador.aplicar_chip_gps())
                self.aguardar_enter()
 
        print(f"Vingador(a) '{nome_heroi}' não encontrado.")
        self.aguardar_enter()
 
    def listar_detalhes_vingador(self):
        nome_heroi = capwords(input("Nome do herói: "))
        for vingador in Vingador.lista_vingadores:
            if nome_heroi in vingador.nome_heroi or nome_heroi in vingador.nome_real:
                vingador.listar_detalhes_vingador()
                self.aguardar_enter()
                return
        print(f"Vingador(a) '{nome_heroi}' não encontrado.")
        self.aguardar_enter()
 
    def mandado_prisao(self):
        nome_heroi = input("Nome do herói: ")
        for vingador in Vingador.lista_vingadores:
            if nome_heroi in vingador.nome_heroi or nome_heroi in vingador.nome_real:
                try:
                    db = Database()
                    db.connect()
 
                    motivo = capwords(input("motivo: "))
                    status = capwords(input("status (Procurado, Detenção, Cumprido, Cancelado): "))
                    opcoes_validas = ["Procurado","Detenção", "Cumprido","Cancelado"]
                     
                    if status not in opcoes_validas:
                        print(f'Opção "{status}" inválida. Opções válidas {', '.join(opcoes_validas)}.\n faça a convocação novamente')
                        self.aguardar_enter()
                        return
                   
                    if nome_heroi in vingador.nome_heroi or nome_heroi in vingador.nome_real:
                   
                        query = f"Select heroi_id from heroi where (nome_heroi like '%{nome_heroi}%') or (nome_real like '%{nome_heroi}%') limit 1"
                        heroi_id = db.select(query)
 
                        query = "INSERT INTO mandado_prisao (heroi_id, motivo,status) VALUES (%s,%s,%s)"
                        values = (int(heroi_id[0][0]), motivo, status)
                        db.execute_query(query, values)
                   
                                           
                except Exception as e:
                    print('Erro ao convocar Vingador: {e}')
                finally:
                    db.disconnect()
 
                print(vingador.mandado_prisao())
                self.aguardar_enter()
                return
       
    @staticmethod
    def exibe_titulo(titulo):
        print(f"\n{titulo}")
        print('-' * len(titulo))
 
    @staticmethod
    def exibe_titulo_app():
        system('cls')
        print('''
 
███████████████▀█████████████████████████████████████
█▄─█─▄█▄─▄█─▄▄▄▄█▄─▄█▄─▄████▀▄─██▄─▀█▄─▄█─▄─▄─█▄─▄▄─█
██▄▀▄███─██─██▄─██─███─██▀██─▀─███─█▄▀─████─████─▄█▀█
▀▀▀▄▀▀▀▄▄▄▀▄▄▄▄▄▀▄▄▄▀▄▄▄▄▄▀▄▄▀▄▄▀▄▄▄▀▀▄▄▀▀▄▄▄▀▀▄▄▄▄▄▀        
        ''')