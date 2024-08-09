import connection


def get_sites():
    with connection.get_connection() as conn:
        c = conn.cursor()
        c.execute('SELECT name FROM sites')
        return [row[0] for row in c.fetchall()]

def get_formations():
    with connection.get_connection() as conn:
        c = conn.cursor()
        c.execute('''
        SELECT formations.name FROM formations
        ''')
        return [row[0] for row in c.fetchall()]


def get_modules():
    with connection.get_connection() as conn:
        c = conn.cursor()
        c.execute('''
        SELECT modules.name FROM modules
        ''')
        return [row[0] for row in c.fetchall()]


def get_years():
    with connection.get_connection() as conn:
        c = conn.cursor()
        c.execute('''
        SELECT years.year_name FROM years
        ''')
        return [row[0] for row in c.fetchall()]


def get_files():
    with connection.get_connection() as conn:
        c = conn.cursor()
        c.execute('''
        SELECT files.name,files.file FROM files
        ''')
        return [row for row in c.fetchall()]


def add_site(site_name):
    with connection.get_connection() as conn:
        c = conn.cursor()
        c.execute('INSERT INTO sites (name) VALUES (?)', (site_name,))
        conn.commit()


def add_formation(formation_name, site_name):
    with connection.get_connection() as conn:
        c = conn.cursor()
        c.execute('INSERT INTO formations (name, site_id) VALUES (?, (SELECT id FROM sites WHERE name = ?))', (formation_name, site_name))
        conn.commit()


def add_module(module_name, formation_name):
    with connection.get_connection() as conn:
        c = conn.cursor()
        c.execute('INSERT INTO modules (name, formation_id) VALUES (?, (SELECT id FROM formations WHERE name = ?))', (module_name, formation_name))
        conn.commit()


def add_year(year, module_name):
    with connection.get_connection() as conn:
        c = conn.cursor()
        c.execute('''
        INSERT INTO years (year, module_id) VALUES (?, 
        (SELECT id FROM modules 
        WHERE name = ?))
        ''', (year, module_name))
        conn.commit()


def add_file(file_name, content, year, module_name, text_content):
    with connection.get_connection() as conn:
        c = conn.cursor()
        c.execute('''
        INSERT INTO files (file_name, content, year_id, text_content) VALUES (?, ?, 
        (SELECT years.id FROM years 
        JOIN modules ON years.module_id = modules.id
        WHERE years.year = ? AND modules.name = ?),?)
        ''', (file_name, content, year, module_name, text_content))
        conn.commit()


def update_file_content(file_name, content):
    with connection.get_connection()('modules.db') as conn:
        c = conn.cursor()
        c.execute('''
        UPDATE files SET content = ? WHERE file_name = ?
        ''', (content, file_name))
        conn.commit()


def delete_site(site_name):
    with connection.get_connection() as conn:
        c = conn.cursor()
        c.execute('DELETE FROM sites WHERE name = ?', (site_name,))
        conn.commit()


def delete_formation(formation_name, site_name):
    with connection.get_connection() as conn:
        c = conn.cursor()
        c.execute('''
        DELETE FROM formations WHERE name = ? AND site_id = (SELECT id FROM sites WHERE name = ?)
        ''', (formation_name, site_name))
        conn.commit()


def delete_module(module_name, formation_name):
    with connection.get_connection() as conn:
        c = conn.cursor()
        c.execute('''
        DELETE FROM modules WHERE name = ? AND formation_id = (SELECT id FROM formations WHERE name = ?)
        ''', (module_name, formation_name))
        conn.commit()


def delete_year(year, module_name):
    with connection.get_connection() as conn:
        c = conn.cursor()
        c.execute('''= (SELECT id FROM modules WHERE name = ?)
        ''', (year, module_name))
        conn.commit()


def delete_file(file_name,year, module_name):
    with connection.get_connection() as conn:
        c = conn.cursor()
        c.execute('''
        DELETE FROM files WHERE file_name = ? and year_id = (SELECT id FROM years WHERE year = ? AND module_id = (SELECT id FROM modules WHERE name = ?))
        ''', (file_name,year, module_name))
        conn.commit()
