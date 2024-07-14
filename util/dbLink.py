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
    JOIN module_formation mf ON f.id = mf.formation_id
    JOIN modules m ON mf.module_id = m.id
    WHERE m.name = %s
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
    JOIN module_formation_year mfy ON y.id = mfy.year_id
    JOIN modules m ON mfy.module_id = m.id
    JOIN formations f ON mfy.formation_id = f.id
    WHERE m.name = %s AND f.name = %s
    order by f.name
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
    JOIN module_formation_year_site mfs ON s.id = mfs.site_id
    JOIN formations f ON f.id = mfs.formation_id
    JOIN years y ON mfs.year_id = y.id
    JOIN modules m ON m.id = mfs.module_id
    WHERE m.name = %s AND f.name = %s AND y.year_name = %s
    order by s.name
    """

    print(query)

    with conn.cursor() as cursor:
        cursor.execute(query, (selected_module, selected_formation, selected_year))
        sites = [row[0] for row in cursor.fetchall()]
    return sites

# Function to retrieve files based on all selected criteria
def get_files(conn, selected_module, selected_formation, selected_year, selected_site):
    query = """
    SELECT f.name, f.file as content, m.name AS module_name, y.year_name, s.name AS site_name, fo.name AS formation_name
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
