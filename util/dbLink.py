import connection

# Database connection function
def connect_db():
    return connection.get_connection()

# Function to retrieve modules from database
def get_modules(conn):
    query = "SELECT name FROM modules order by name"
    with conn.cursor() as cursor:
        cursor.execute(query)
        modules = [row[0] for row in cursor.fetchall()]
    return modules

# Function to retrieve formations based on selected module
def get_formations(conn, selected_module):
    query = """
    SELECT f.name
    FROM formations f
    order by f.name
    """
    with conn.cursor() as cursor:
        cursor.execute(query, (selected_module,))
        formations = [row[0] for row in cursor.fetchall()]
    return formations

# Function to retrieve years based on selected module and formation
def get_years(conn, selected_module, selected_formation):
    query = """
    SELECT y.year_name
    FROM years y
    order by y.year_name
    """
    with conn.cursor() as cursor:
        cursor.execute(query, (selected_module, selected_formation))
        years = [row[0] for row in cursor.fetchall()]
    return years

# Function to retrieve sites based on selected module, formation, and year
def get_sites(conn, selected_module, selected_formation, selected_year):
    query = """
    SELECT s.name
    FROM sites s
    order by s.name
    """
    print(query)

    with conn.cursor() as cursor:
        cursor.execute(query, (selected_module, selected_formation, selected_year))
        sites = [row[0] for row in cursor.fetchall()]
    return sites

def get_file(conn, id):
    query = """
    SELECT f.file as content
    FROM files f
    WHERE id=%s
    """
    params = []
    params.append(id)

    with conn.cursor() as cursor:
        cursor.execute(query, params)
        files = cursor.fetchall()

    for f in files:
        content = f
        return content
    
    return None

# Function to retrieve files based on all selected criteria
def get_files(conn, selected_module, selected_formation, selected_year, selected_site):
    query = """
    SELECT f.id,f.name, f.file,  m.name AS module_name, y.year_name, s.name AS site_name, fo.name AS formation_name
    FROM files f
    JOIN sites s ON f.site_id = s.id
    JOIN modules m ON f.module_id = m.id
    JOIN formations fo ON f.formation_id = fo.id
    JOIN years y ON f.year_id = y.id
    WHERE 1=1
    """
    params = []

    if selected_module:
        query += " AND m.name = %s"
        params.append(selected_module)

    if selected_formation:
        query += " AND fo.name = %s"
        params.append(selected_formation)

    if selected_year:
        query += " AND y.year_name = %s"
        params.append(selected_year)

    if selected_site:
        query += " AND s.name = %s"
        params.append(selected_site)

    query += "order by f.name"

    with conn.cursor() as cursor:
        cursor.execute(query, params)
        files = cursor.fetchall()

    return files
