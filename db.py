import sqlite3

# Initialize the database and create tables if they don't exist
def initialize_db():
    with sqlite3.connect('modules.db') as conn:
        c = conn.cursor()
        c.execute('''
        CREATE TABLE IF NOT EXISTS sites (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE
        )
        ''')
        c.execute('''
        CREATE TABLE IF NOT EXISTS formations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            site_id INTEGER,
            FOREIGN KEY (site_id) REFERENCES sites (id)
        )
        ''')
        c.execute('''
        CREATE TABLE IF NOT EXISTS modules (
            id INTEGER PRIMARY KEY,
            name TEXT,
            formation_id INTEGER,
            FOREIGN KEY (formation_id) REFERENCES formations (id)
        )
        ''')
        c.execute('''
        CREATE TABLE IF NOT EXISTS years (
            id INTEGER PRIMARY KEY,
            year TEXT,
            module_id INTEGER,
            FOREIGN KEY (module_id) REFERENCES modules (id)
        )
        ''')
        c.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY,
            file_name TEXT,
            content BLOB,
            text_content TEXT,    
            year_id INTEGER,
            extension TEXT,
            FOREIGN KEY (year_id) REFERENCES years (id)
        )
        ''')
        conn.commit()

def get_sites():
    with sqlite3.connect('modules.db') as conn:
        c = conn.cursor()
        c.execute('SELECT name FROM sites')
        return [row[0] for row in c.fetchall()]

def get_formations(site_name):
    with sqlite3.connect('modules.db') as conn:
        c = conn.cursor()
        c.execute('''
        SELECT formations.name FROM formations
        JOIN sites ON formations.site_id = sites.id
        WHERE sites.name = ?
        ''', (site_name,))
        return [row[0] for row in c.fetchall()]

def get_modules(formation_name):
    with sqlite3.connect('modules.db') as conn:
        c = conn.cursor()
        c.execute('''
        SELECT modules.name FROM modules
        JOIN formations ON modules.formation_id = formations.id
        WHERE formations.name = ?
        ''', (formation_name,))
        return [row[0] for row in c.fetchall()]

def get_years(module_name):
    with sqlite3.connect('modules.db') as conn:
        c = conn.cursor()
        c.execute('''
        SELECT years.year FROM years
        JOIN modules ON years.module_id = modules.id
        WHERE modules.name = ?
        ''', (module_name,))
        return [row[0] for row in c.fetchall()]

def get_files(year, module_name):
    with sqlite3.connect('modules.db') as conn:
        c = conn.cursor()
        c.execute('''
        SELECT files.file_name,files.content FROM files
        JOIN years ON files.year_id = years.id
        JOIN modules ON years.module_id = modules.id
        WHERE years.year = ? AND modules.name = ?
        ''', (year, module_name))
        return [row for row in c.fetchall()]

def add_site(site_name):
    with sqlite3.connect('modules.db') as conn:
        c = conn.cursor()
        c.execute('INSERT INTO sites (name) VALUES (?)', (site_name,))
        conn.commit()

def add_formation(formation_name, site_name):
    with sqlite3.connect('modules.db') as conn:
        c = conn.cursor()
        c.execute('INSERT INTO formations (name, site_id) VALUES (?, (SELECT id FROM sites WHERE name = ?))', (formation_name, site_name))
        conn.commit()

def add_module(module_name, formation_name):
    with sqlite3.connect('modules.db') as conn:
        c = conn.cursor()
        c.execute('INSERT INTO modules (name, formation_id) VALUES (?, (SELECT id FROM formations WHERE name = ?))', (module_name, formation_name))
        conn.commit()

def add_year(year, module_name):
    with sqlite3.connect('modules.db') as conn:
        c = conn.cursor()
        c.execute('''
        INSERT INTO years (year, module_id) VALUES (?, 
        (SELECT id FROM modules 
        WHERE name = ?))
        ''', (year, module_name))
        conn.commit()

def add_file(file_name, content, year, module_name, text_content):
    with sqlite3.connect('modules.db') as conn:
        c = conn.cursor()
        c.execute('''
        INSERT INTO files (file_name, content, year_id, text_content) VALUES (?, ?, 
        (SELECT years.id FROM years 
        JOIN modules ON years.module_id = modules.id
        WHERE years.year = ? AND modules.name = ?),?)
        ''', (file_name, content, year, module_name, text_content))
        conn.commit()

def update_file_content(file_name, content):
    with sqlite3.connect('modules.db') as conn:
        c = conn.cursor()
        c.execute('''
        UPDATE files SET content = ? WHERE file_name = ?
        ''', (content, file_name))
        conn.commit()

def delete_site(site_name):
    with sqlite3.connect('modules.db') as conn:
        c = conn.cursor()
        c.execute('DELETE FROM sites WHERE name = ?', (site_name,))
        conn.commit()

def delete_formation(formation_name, site_name):
    with sqlite3.connect('modules.db') as conn:
        c = conn.cursor()
        c.execute('''
        DELETE FROM formations WHERE name = ? AND site_id = (SELECT id FROM sites WHERE name = ?)
        ''', (formation_name, site_name))
        conn.commit()

def delete_module(module_name, formation_name):
    with sqlite3.connect('modules.db') as conn:
        c = conn.cursor()
        c.execute('''
        DELETE FROM modules WHERE name = ? AND formation_id = (SELECT id FROM formations WHERE name = ?)
        ''', (module_name, formation_name))
        conn.commit()

def delete_year(year, module_name):
    with sqlite3.connect('modules.db') as conn:
        c = conn.cursor()
        c.execute('''= (SELECT id FROM modules WHERE name = ?)
        ''', (year, module_name))
        conn.commit()

def delete_file(year, module_name):
    with sqlite3.connect('modules.db') as conn:
        c = conn.cursor()
        c.execute('''
        DELETE FROM files WHERE year_id = (SELECT id FROM years WHERE year = ? AND module_id = (SELECT id FROM modules WHERE name = ?))
        ''', (year, module_name))
        conn.commit()

# Initialize the database when the module is loaded
initialize_db()
