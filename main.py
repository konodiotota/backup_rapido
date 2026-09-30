import os
import sys
import subprocess
import ctypes
import time

GREEN = '\033[92m'
RESET = '\033[0m'
PASTAS_EXCLUIDAS = ["Windows", "AppData", "Temp", "tmp", "$RECYCLE.BIN", "System Volume Information"]
ARQUIVOS_EXCLUIDOS = ["pagefile.sys", "hiberfil.sys", "swapfile.sys", "dumpstack.log", "dumpstack.log.tmp"]

def Tamanho_terminal(largura=520, altura=493):
    if os.name == 'nt':
        subprocess.run(f'mode con cols={largura} lines={altura}', shell=True)

def is_admin():
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        while True:
            print(f'{GREEN}Aplicativo não executado como Administrador, algumas funções podem não funcionar, quer continuar? [s] \ [n]{RESET}')
            escolha=input().upper().strip()
            if escolha == 'N':
                sys.exit()
            if escolha == 'S':
                return False
            else:
                print('Quer me burlar é? escolha invalida, coloca certo ae!\n')

def Clear_terminal():
    if os.name == 'nt':
        subprocess.run('cls', shell=True)
    else:
        subprocess.run(['clear'])

def Saldacao():
    print(f'\n' + '_' * 76 + '\n')
    print('''██████╗  █████╗  ██████╗██╗  ██╗██╗   ██╗██████╗
 ██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██║   ██║██╔══██╗
 ██████╔╝███████║██║     █████╔╝ ██║   ██║██████╔╝
 ██╔══██╗██╔══██║██║     ██╔═██╗ ██║   ██║██╔═══╝ 
 ██████╔╝██║  ██║╚██████╗██║  ██╗╚██████╔╝██║     
 ╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝     '''
 'Made by alves')
    print('[0] Sair')
    print('[1] Backup')
    print('[2] Transferencia backup')

def Choices():
    Saldacao()
    print(f'_' * 76 + '\n')
    choise = input(f'{GREEN}Escolha sua opção: {RESET}')
    if choise in ['0', '1', '2']:
        Clear_terminal()
    if choise == '0':
        print('Finalizando o sistema...')
        tempo=3
        for segunds in range(tempo, 0, -1):
            print(f'Finalizando em {segunds}')
            time.sleep(1)
            Clear_terminal()
    return choise

def Comando_robocopy(origem, destino):
    comando = [
        "robocopy", origem, destino,
        "/E", "/MT:16", "/COPY:DAT", "/DCOPY:T",
        "/R:0", "/W:0", "/XJ", "/NP", "/BYTES"
    ]
    if PASTAS_EXCLUIDAS:
        comando.append("/XD")
        comando.extend(PASTAS_EXCLUIDAS)

    if ARQUIVOS_EXCLUIDOS:
        comando.append("/XF")
        comando.extend(ARQUIVOS_EXCLUIDOS)

    if is_admin():
        comando.append("/B")
    else:
        print(f'{GREEN}Aviso: Não executado como administrador, o modo backup (/B) foi desativado.{RESET}')
        
    return comando

def Executar_robocopy(comando, funcao):
    print(f'\nComando executado:\n{subprocess.list2cmdline(comando)}')
    print('-' * 40)
    print(f'Começando, {funcao}...\n')
    
    try:
        # Removido o DEVNULL para que o usuário consiga acompanhar o progresso no terminal
        processo = subprocess.Popen(comando)
        processo.wait()
        
        # O robocopy retorna códigos de 0 a 7 para sucessos/avisos comuns
        if processo.returncode <= 7:
            print(f"\n{GREEN}{funcao} concluído com sucesso!{RESET}")
        else:
            print(f"\n{GREEN}O/A {funcao} terminou com avisos ou erros (Código: {processo.returncode}).{RESET}")
    except FileNotFoundError:
        print(f"\n{GREEN}Erro: O executável 'robocopy' não foi encontrado.{RESET}")
    except KeyboardInterrupt:
        print("\n\n⚠ Operação interrompida pelo usuário. Encerrando o robocopy...")
        try:
            processo.terminate()
            processo.wait(timeout=5)
        except Exception:
            processo.kill()
    finally:
        print('Limpando atributos')
        destino_path= comando[2]
        limpar_atributos=f'attrib -h -s {destino_path}'
        subprocess.run(limpar_atributos, shell=True)

def Choice_1():
    try:
        print('\nQual seria o caminho de origem do backup?')
        origem = input().strip().upper()
        if len(origem) == 1 and origem.isalpha():
            origem = origem + ":\\"

        if not origem or not os.path.exists(origem):
            print(f"\n{GREEN}Erro: O caminho de origem '{origem}' não foi encontrado ou não é válido.{RESET}")
            return

        print('\nOnde quer que o backup seja salvo?')
        destino = input().strip().upper()
        if len(destino) == 1 and destino.isalpha():
            destino = destino + ":\\"

        if not destino:
            print(f"\n{GREEN}Erro: Caminho de destino inválido.{RESET}")
            return

        # Opcional: Cria a pasta de destino caso ela não exista
        if not os.path.exists(destino):
            try:
                os.makedirs(destino)
            except Exception as e:
                print(f"\n{GREEN}Erro ao criar diretório de destino: {e}{RESET}")
                return

        # Gera o comando e o executa de fato
        comando = Comando_robocopy(origem=origem, destino=destino)
        Executar_robocopy(comando, funcao='backup')
    except KeyboardInterrupt:
            print("\n\n⚠ Operação interrompida pelo usuário. Encerrando o robocopy...")
            sys.exit()
    input("\nPressione Enter para voltar ao menu...")

def Choice_2():
    try:
        print('Qual seria o caminho de origem do backup ?')
        origem = input().upper().strip()
        if len(origem) == 1 and origem.isalpha():
            origem = origem + ":\\"
        if not origem or not os.path.exists(origem):
            print(f"\n{GREEN}Erro: O caminho de origem '{origem}' não foi encontrado.{RESET}")
            input("\nPressione Enter para voltar ao menu...")
            return
        print('Qual seria o caminho de destino do backup?')

        destino= input().upper().strip()
        if len(destino) == 1 and destino.isalpha():
            destino = destino + ":\\"
        
        if not destino or not os.path.exists(destino):
            print(f"\n{GREEN}Erro: O caminho de origem '{destino}' não foi encontrado.{RESET}")
            input("\nPressione Enter para voltar ao menu...")
            return

        comando = Comando_robocopy(origem=origem, destino=destino)
        Executar_robocopy(comando=comando,funcao='Transferencia Backup')
        input("\nPressione Enter para voltar ao menu...")
    except KeyboardInterrupt:
            print("\n\n⚠ Operação interrompida pelo usuário. Encerrando o robocopy...")
            sys.exit()

def Main():
    Tamanho_terminal(520, 493)
    while True:
        Clear_terminal()
        opcao = Choices()
        if opcao == '0':
            sys.exit()
        elif opcao == '1':
            Choice_1()
        elif opcao == '2':
            Choice_2()
        else:
            print("\nOpção inválida! Tente novamente.")

if __name__ == "__main__":
    Main()