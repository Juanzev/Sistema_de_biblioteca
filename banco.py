import sqlite3

# ---------- MODELOS ---------- #
class Livro:
    def __init__(self, titulo, autor, ano, copias):
        self.titulo = titulo
        self.autor = autor
        self.ano = ano
        self.copias = copias

class Usuario:
    def __init__(self, nome, identificacao, contato):
        self.nome = nome
        self.identificacao = identificacao
        self.contato = contato

# ---------- BANCO DE DADOS ---------- #
def criar_tabelas():
    conn = sqlite3.connect("biblioteca.db")
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS livros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT,
        autor TEXT,
        ano INTEGER,
        copias INTEGER
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        identificacao TEXT UNIQUE,
        contato TEXT
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS emprestimos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        livro_id INTEGER,
        usuario_id INTEGER,
        FOREIGN KEY(livro_id) REFERENCES livros(id),
        FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
    )''')

    conn.commit()
    conn.close()

# ---------- FUNCIONALIDADES ---------- #
def cadastrar_livro():
    try:
        titulo = input("Título: ")
        autor = input("Autor: ")
        ano = int(input("Ano de publicação: "))
        copias = int(input("Número de cópias: "))

        conn = sqlite3.connect("biblioteca.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO livros (titulo, autor, ano, copias) VALUES (?, ?, ?, ?)",
                       (titulo, autor, ano, copias))
        conn.commit()
        conn.close()
        print("Livro cadastrado com sucesso!\n")
    except Exception as e:
        print("Erro ao cadastrar livro:", e)


def cadastrar_usuario():
    try:
        nome = input("Nome: ")
        identificacao = input("Número de identificação: ")
        contato = input("Contato: ")

        conn = sqlite3.connect("biblioteca.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (nome, identificacao, contato) VALUES (?, ?, ?)",
                       (nome, identificacao, contato))
        conn.commit()
        conn.close()
        print("Usuário cadastrado com sucesso!\n")
    except sqlite3.IntegrityError:
        print("Identificação já cadastrada.\n")
    except Exception as e:
        print("Erro ao cadastrar usuário:", e)


def emprestar_livro():
    try:
        id_usuario = input("ID do usuário: ")
        id_livro = input("ID do livro: ")

        conn = sqlite3.connect("biblioteca.db")
        cursor = conn.cursor()
        cursor.execute("SELECT copias FROM livros WHERE id=?", (id_livro,))
        livro = cursor.fetchone()

        if not livro:
            print("Livro não encontrado.\n")
        elif livro[0] <= 0:
            print("Livro indisponível para empréstimo.\n")
        else:
            cursor.execute("INSERT INTO emprestimos (livro_id, usuario_id) VALUES (?, ?)", (id_livro, id_usuario))
            cursor.execute("UPDATE livros SET copias = copias - 1 WHERE id = ?", (id_livro,))
            conn.commit()
            print("Livro emprestado com sucesso!\n")
        conn.close()
    except Exception as e:
        print("Erro ao emprestar livro:", e)


def devolver_livro():
    try:
        id_emprestimo = input("ID do empréstimo: ")
        conn = sqlite3.connect("biblioteca.db")
        cursor = conn.cursor()

        cursor.execute("SELECT livro_id FROM emprestimos WHERE id=?", (id_emprestimo,))
        emprestimo = cursor.fetchone()

        if not emprestimo:
            print("Empréstimo não encontrado.\n")
        else:
            livro_id = emprestimo[0]
            cursor.execute("DELETE FROM emprestimos WHERE id=?", (id_emprestimo,))
            cursor.execute("UPDATE livros SET copias = copias + 1 WHERE id = ?", (livro_id,))
            conn.commit()
            print("Livro devolvido com sucesso!\n")
        conn.close()
    except Exception as e:
        print("Erro ao devolver livro:", e)


def consultar_livros():
    criterio = input("Buscar por (titulo/autor/ano): ").lower()
    termo = input("Digite o termo de busca: ")

    query = ""
    if criterio == "titulo":
        query = "SELECT * FROM livros WHERE titulo LIKE ?"
    elif criterio == "autor":
        query = "SELECT * FROM livros WHERE autor LIKE ?"
    elif criterio == "ano":
        query = "SELECT * FROM livros WHERE ano = ?"
        termo = int(termo)
    else:
        print("Critério inválido.\n")
        return

    conn = sqlite3.connect("biblioteca.db")
    cursor = conn.cursor()
    cursor.execute(query, ("%"+str(termo)+"%",))
    resultados = cursor.fetchall()

    if resultados:
        for livro in resultados:
            print(livro)
    else:
        print("Nenhum livro encontrado.\n")
    conn.close()


def gerar_relatorios():
    conn = sqlite3.connect("biblioteca.db")
    cursor = conn.cursor()

    print("\n--- LIVROS DISPONÍVEIS ---")
    cursor.execute("SELECT * FROM livros WHERE copias > 0")
    for row in cursor.fetchall():
        print(row)

    print("\n--- LIVROS EMPRESTADOS ---")
    cursor.execute("""SELECT emprestimos.id, livros.titulo, usuarios.nome FROM emprestimos
                    JOIN livros ON emprestimos.livro_id = livros.id
                    JOIN usuarios ON emprestimos.usuario_id = usuarios.id""")
    for row in cursor.fetchall():
        print(row)

    print("\n--- USUÁRIOS CADASTRADOS ---")
    cursor.execute("SELECT * FROM usuarios")
    for row in cursor.fetchall():
        print(row)

    conn.close()

# ---------- MENU ---------- #
def menu():
    criar_tabelas()
    while True:
        print("\n--- MENU BIBLIOTECA ---")
        print("1. Cadastrar Livro")
        print("2. Cadastrar Usuário")
        print("3. Emprestar Livro")
        print("4. Devolver Livro")
        print("5. Consultar Livros")
        print("6. Gerar Relatórios")
        print("0. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_livro()
        elif opcao == "2":
            cadastrar_usuario()
        elif opcao == "3":
            emprestar_livro()
        elif opcao == "4":
            devolver_livro()
        elif opcao == "5":
            consultar_livros()
        elif opcao == "6":
            gerar_relatorios()
        elif opcao == "0":
            print("Saindo do sistema.")
            break
        else:
            print("Opção inválida.\n")

# ---------- INÍCIO ---------- #
if __name__ == "__main__":
    menu()
