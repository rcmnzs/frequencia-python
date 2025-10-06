import sqlite3

# Verificar alunos
conn = sqlite3.connect('data/alunos_db.sqlite')
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM alunos')
total_alunos = cursor.fetchone()[0]
print(f"Total de alunos: {total_alunos}")
conn.close()

# Verificar horários
conn = sqlite3.connect('data/horarios_db.sqlite')
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM horarios')
total_horarios = cursor.fetchone()[0]
print(f"Total de horários: {total_horarios}")
conn.close()