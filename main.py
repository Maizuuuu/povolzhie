from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

# Создаем и заполняем базу данных
def init_db():
    conn = sqlite3.connect('povolzhye.db')
    c = conn.cursor()
    
    # Удаляем таблицу, если она существует
    c.execute('DROP TABLE IF EXISTS subjects')
    
    # Создаем таблицу заново
    c.execute('''CREATE TABLE IF NOT EXISTS subjects
                 (id INTEGER PRIMARY KEY,
                 name TEXT,
                 population INTEGER,
                 climate TEXT,
                 agriculture TEXT,
                 relief TEXT,
                 area REAL,
                 image TEXT)''')
    
    # Пример данных
    subjects_data = [
    # Республики
    (1, 'Республика Татарстан', 3908000, 'Умеренный', 
     'Зерновые, животноводство', 'Равнины, возвышенности', 67847, 'tatarstan.jpg'),
    
    (2, 'Республика Калмыкия', 271135, 'Резко континентальный', 
     'Овцеводство, верблюдоводство', 'Степи, полупустыни', 74731, 'kalmykia.jpg'),
    
    # Области
    (3, 'Астраханская область', 1017514, 'Резко континентальный', 
     'Овощеводство, бахчеводство', 'Равнины, дельта Волги', 49024, 'astrakhan.jpg'),
    
    (4, 'Волгоградская область', 2491256, 'Умеренно-континентальный', 
     'Зерновые, подсолнечник', 'Степь, возвышенности', 112877, 'volgograd.jpg'),
    
    (5, 'Пензенская область', 1298238, 'Умеренно-континентальный', 
     'Зерновые, картофель', 'Равнины, лесостепь', 43352, 'penza.jpg'),
    
    (6, 'Самарская область', 3159000, 'Умеренно-континентальный', 
     'Пшеница, подсолнечник', 'Равнины, Жигулёвские горы', 53565, 'samara.jpg'),
    
    (7, 'Саратовская область', 2424800, 'Умеренно-континентальный', 
     'Зерновые, овощеводство', 'Степь, возвышенности', 101240, 'saratov.jpg'),
    
    (8, 'Ульяновская область', 1225264, 'Умеренно-континентальный', 
     'Зерновые, картофель', 'Равнины, лесостепь', 37181, 'ulyanovsk.jpg'),
    
]
    
    # Вставляем данные только если таблица пуста
    c.execute('SELECT COUNT(*) FROM subjects')
    count = c.fetchone()[0]
    
    if count == 0:
        c.executemany('INSERT INTO subjects VALUES (?,?,?,?,?,?,?,?)', subjects_data)
    
    conn.commit()
    conn.close()

init_db()


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/subjects')
def subjects():
    conn = sqlite3.connect('povolzhye.db')
    c = conn.cursor()
    c.execute('SELECT * FROM subjects')
    data = c.fetchall()
    conn.close()
    return render_template('subjects.html', subjects=data)
@app.route('/subject/<int:subject_id>')
def subject(subject_id):
    conn = sqlite3.connect('povolzhye.db')
    c = conn.cursor()
    c.execute('SELECT * FROM subjects WHERE id = ?', (subject_id,))
    subject_data = c.fetchone()
    conn.close()
    
    if subject_data:
        return render_template('subject.html', subject=subject_data)
    else:
        return "Субъект не найден", 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)