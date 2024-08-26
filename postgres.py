import connection


def get_site_id(site_name):
    with connection.get_connection() as conn:
        c = conn.cursor()
        c.execute('SELECT id FROM sites where name = %s',(site_name,))
        row = c.fetchone()
        return row [0]

def get_module_id(module_name):
    with connection.get_connection() as conn:
        c = conn.cursor()
        c.execute('SELECT id FROM modules where name = %s',(module_name,))
        row = c.fetchone()
        return row [0]

def get_formation_id(formation):
    with connection.get_connection() as conn:
        c = conn.cursor()
        c.execute('SELECT id FROM formations where name = %s',(formation,))
        row = c.fetchone()
        return row [0]
    
def get_year_id(years):
    with connection.get_connection() as conn:
        c = conn.cursor()
        c.execute('SELECT id FROM years where year_name = %s',(years,))
        row = c.fetchone()
        return row [0]
  
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


def get_files_filter(year, module_name, formation, site):
    with connection.get_connection() as conn:
        c = conn.cursor()
        c.execute('''
        SELECT files.name,file, files.id as id FROM files
        JOIN years ON files.year_id = years.id
        JOIN modules ON files.module_id = modules.id
        JOIN sites on sites.id = files.site_id
        JOIN formations on formations.id = files.formation_id                                     
        WHERE years.year_name = %s AND modules.name = %s and formations.name = %s and sites.name = %s 
        ''', (year, module_name,formation,site))
        return [row for row in c.fetchall()]


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


def add_file(site, module, formation, year, content, file_name,file_bytes):
    with connection.get_connection() as conn:
        c = conn.cursor()
        c.execute('''
        INSERT INTO files (site_id,module_id,formation_id,year_id,name,content,file) VALUES ( 
        %s,%s,%s,%s,%s,%s,%s)
        ''', (get_site_id(site), get_module_id(module),get_formation_id(formation), get_year_id(year), file_name,content, file_bytes ))
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


def delete_file(id):
    with connection.get_connection() as conn:
        c = conn.cursor()
        c.execute('''
        DELETE FROM files WHERE id = %s
        ''', (id,))
        conn.commit()