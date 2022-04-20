import sqlite3

conexao = sqlite3.connect('banco.db')
cursor = conexao.cursor()

cria_tabela = "CREATE TABLE IF NOT EXISTS hoteis (hotel_id text PRIMARY KEY,\
 nome text, estrelas real, diaria real, cidade text)"

cria_hotel = "INSERT INTO hoteis VALUES ('alpha', 'Alpha Hotel', 4.3, 345.30, 'Rio de Janeiro')"

cursor.execute(cria_tabela)
cursor.execute(cria_hotel)
conexao.commit()
conexao.close()
