import os
import tempfile
import connection
import convert as cvt

def update_file_blob(file_id, new_blob):
    with connection.get_connection() as conn:

        cursor = conn.cursor()

        query = """
        UPDATE files
        SET file = %s
        WHERE id = %s;
        """

        cursor.execute(query, (new_blob, file_id))

        conn.commit()

        cursor.close()

        return True

def process_file_for_year(source_year, dest_year):
    
    year_id_dest = get_year_id(dest_year) 

    file_record = get_files_by_year_pdf(year_id_dest)

    for file_id, file_name, file_blob in file_record:
        try:
            if ".pdf" in file_name:
                print (file_name)

                temp_input_file_pdf = tempfile.NamedTemporaryFile(delete=False, suffix="pdf")
                with open(temp_input_file_pdf.name, 'wb') as temp_file:
                    temp_file.write(file_blob)

                    temp_output_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")

                    cvt.replace_text_in_pdf(temp_input_file_pdf.name,temp_output_file.name, source_year, dest_year)
            
                    with open(temp_output_file.name, 'rb') as output_file:
                        updated_file_blob = output_file.read()

                    update_file_blob(file_id, updated_file_blob)

                    os.remove(temp_input_file_pdf.name)
                    os.remove(temp_output_file.name)
        except:
            print("Erreur " + file_name)

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


def duplicate_year(source,dest):
    with connection.get_connection() as conn:
        c = conn.cursor()
        c.execute('''
        insert into files (site_id,module_id,formation_id,year_id,name,content,file) 
        select site_id,module_id,formation_id,(select id from years where year_name = %s),name,content,file from files where year_id in (select id from years where year_name = %s)
        ''',(dest,source))        

    process_file_for_year(source,dest)


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

def get_files_by_year_pdf(year_id):
    with connection.get_connection() as conn:
        c = conn.cursor()
        c.execute('''
        SELECT id,name,file FROM files where year_id = %s
        ''',(year_id,))
        return [row for row in c.fetchall()]
        
def add_site(site_name):
    with connection.get_connection() as conn:
        c = conn.cursor()
        c.execute('INSERT INTO sites (name) VALUES (%s)', (site_name,))
        conn.commit()


def add_formation(formation_name):
    with connection.get_connection() as conn:
        c = conn.cursor()
        c.execute('INSERT INTO formations (name) VALUES (%s)', (formation_name,))
        conn.commit()


def add_module(module_name):
    with connection.get_connection() as conn:
        c = conn.cursor()
        c.execute('INSERT INTO modules (name) VALUES (%s', (module_name,))
        conn.commit()


def add_year(year):
    with connection.get_connection() as conn:
        c = conn.cursor()
        c.execute('''
        INSERT INTO years (year_name) VALUES (%s)
        ''', (year, ))
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
        UPDATE files SET content = %s WHERE file_name = %s
        ''', (content, file_name))
        conn.commit()


def delete_site(site_name):
    with connection.get_connection() as conn:
        c = conn.cursor()
        c.execute('DELETE FROM sites WHERE name = %s', (site_name,))
        conn.commit()


def delete_formation(formation_name):
    with connection.get_connection() as conn:
        c = conn.cursor()
        c.execute('''
        DELETE FROM formations WHERE name = %s
        ''', (formation_name, ))
        conn.commit()


def delete_module(module_name):
    with connection.get_connection() as conn:
        c = conn.cursor()
        c.execute('''
        DELETE FROM modules WHERE name = %s)
        ''', (module_name, ))
        conn.commit()


def delete_year(year):
    with connection.get_connection() as conn:
        c = conn.cursor()
        c.execute('''delete from years where year_name = %s)
        ''', (year))
        conn.commit()


def delete_file(id):
    with connection.get_connection() as conn:
        c = conn.cursor()
        c.execute('''
        DELETE FROM files WHERE id = %s
        ''', (id,))
        conn.commit()