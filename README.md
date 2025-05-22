# 📚 Sistema de Biblioteca em Python

Este é um sistema simples de gerenciamento de biblioteca, desenvolvido em Python com banco de dados SQLite. Ele permite cadastrar livros e usuários, realizar empréstimos e devoluções, consultar acervos e gerar relatórios.

## 🔧 Requisitos

- Python 3.x
- Biblioteca `sqlite3` (já incluída no Python por padrão)

## 📂 Estrutura

- `Livro` (classe): representa um livro com título, autor, ano de publicação e número de cópias.
- `Usuario` (classe): representa um usuário com nome, identificação única e contato.
- Banco de dados `biblioteca.db` com 3 tabelas:
  - `livros`: armazena os livros disponíveis.
  - `usuarios`: armazena os usuários cadastrados.
  - `emprestimos`: armazena os empréstimos realizados.

## 🚀 Funcionalidades

### 1. Cadastrar Livro
Solicita título, autor, ano e número de cópias e armazena no banco de dados.

### 2. Cadastrar Usuário
Solicita nome, número de identificação (único) e contato. Impede duplicatas.

### 3. Emprestar Livro
Verifica se o livro está disponível e realiza o empréstimo ao usuário, decrementando o número de cópias disponíveis.

### 4. Devolver Livro
Solicita o ID do empréstimo, exclui o registro e incrementa novamente o número de cópias do livro.

### 5. Consultar Livros
Permite buscar livros por título, autor ou ano de publicação.

### 6. Gerar Relatórios
Exibe:
- Livros disponíveis
- Livros emprestados (com nome do usuário)
- Usuários cadastrados

## 🧪 Execução

Para rodar o programa:

```bash
python biblioteca.py
```
🛠️ Observações
- Os dados são persistidos em um arquivo SQLite (biblioteca.db).

- O sistema é totalmente em linha de comando.

- Ideal para testes, protótipos ou aprendizado de CRUD com SQLite.

👨‍💻 Autor
*Desenvolvido por: Juan Patrick.*
