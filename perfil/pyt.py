#Criar tabela de usuários
cursor.execute('''
CREATE TABLE IF NOT EXISTS usuario(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL,
    senha TEXT NOT NULL
)
''')

#Inserir dados na tabela
cursor.execute('''
INSERT INTO usuario(nome, email, senha)
VALUES('Igor', 'igor@email.com', '123456'),
      ('João', 'joao@email.com', '654321'),
      ('Maria', 'maria@email.com', '789456'),
      ('Pedro', 'pedro@email.com', '456123')
''')

#Selecionar todos os usuários
cursor.execute('SELECT * FROM usuario')
dados = cursor.fetchall()

for usuario in dados:
    print(usuario)

#Selecionar usuário por id
cursor.execute('SELECT * FROM usuario WHERE id = ?', (2,))
dado = cursor.fetchone()

print(dado)

#Atualizar usuário pelo id
cursor.execute('UPDATE usuario SET nome = ? WHERE id = ?', ('Joãozinho', 2))

#Excluir usuário pelo id
cursor.execute('DELETE FROM usuario WHERE id = ?', (2,))

conn.commit()
conn.close()

print()