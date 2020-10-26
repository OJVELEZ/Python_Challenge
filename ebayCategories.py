import sqlite3
from sqlite3 import Error
import xml.etree.ElementTree as ET
import os.path
from os import path
import sys


def removespecialchar(string):
    return string.replace("\"", "")


def value_variable(var):
    if var != None:
        return removespecialchar(var.text)
    else:
        return ""


def read_xml(path, ns, conn):
    tree = ET.parse(path)
    root = tree.getroot()
    count = root.find('ns:CategoryCount', ns)
    uptime = root.find('ns:UpdateTime', ns)
    cversion = root.find('ns:CategoryVersion', ns)
    rpriceallowed = root.find('ns:ReservePriceAllowed', ns)
    minpriceallowed = root.find('ns:MinimumReservePrice', ns)
    xmltimestamp = root.find('ns:Timestamp', ns)
    xmlack = root.find('ns:Ack', ns)
    xmlversion = root.find('ns:Version', ns)
    xmlbuild = root.find('ns:Build', ns)
    print(count.text)

    master_values = insert_master_table(count=count.text, uptime=uptime.text, cversion=cversion.text,
                                        rpriceallowed=rpriceallowed.text, minpriceallowed=minpriceallowed.text,
                                        xmltimestamp=xmltimestamp.text, xmlack=xmlack.text, xmlversion=xmlversion.text,
                                        xmlbuild=xmlbuild.text)

    try:
        cursor = conn.cursor()
        cursor.execute(master_values)
        conn.commit()
    except Error as e:
        print(f"Error inserting in main_category:{e}")

    for category in root.iter('{urn:ebay:apis:eBLBaseComponents}Category'):
        categoryid = category.find('ns:CategoryID', ns)
        bestoffer = category.find('ns:AutoPayEnabled', ns)
        autopay = category.find('ns:AutoPayEnabled', ns)
        categorylevel = category.find('ns:CategoryLevel', ns)
        categoryname = category.find('ns:CategoryName', ns)
        categoryparent = category.find('ns:CategoryParentID', ns)

        categoryid_val = value_variable(categoryid)
        bestoffer_val = value_variable(bestoffer)
        autopay_val = value_variable(autopay)
        categorylevel_val = value_variable(categorylevel)
        categoryname_val = value_variable(categoryname)
        categoryparent_val = value_variable(categoryparent)

        category_values = insert_detail_table(categoryid=categoryid_val,
                                              bestoffer=bestoffer_val,
                                              autopay=autopay_val,
                                              categorylevel=categorylevel_val,
                                              categoryname=categoryname_val,
                                              categoryparent=categoryparent_val)

        try:
            cursor = conn.cursor()
            cursor.execute(category_values)
            conn.commit()
        except Error as e:
            print(
                f"Error inserting in categories:{e} in category_id {categoryid}")


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def execute_ddl(conn, create_table_ddl):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_ddl)
    except Error as e:
        print(e)


def insert_master_table(**kwargs):
    insert_sentence = f"INSERT INTO main_category(count, uptime, cversion, rpriceallowed, \
                                                  minpriceallowed, xmltimestamp, xmlack, \
                                                  xmlversion, xmlbuild) VALUES \
    ({kwargs['count']}, \"{kwargs['uptime']}\", {kwargs['cversion']}, \"{kwargs['rpriceallowed']}\", \
     {kwargs['minpriceallowed']}, \"{kwargs['xmltimestamp']}\", \"{kwargs['xmlack']}\", \
     {kwargs['xmlversion']}, \"{kwargs['xmlbuild']}\")"

    return insert_sentence


def insert_detail_table(**kwargs):
    insert_sentence = f"INSERT INTO categories( categoryid, bestoffer, autopay, \
                                                 categorylevel, categoryname,categoryparent) VALUES \
    ({kwargs['categoryid']}, \"{kwargs['bestoffer']}\", \"{kwargs['autopay']}\", \
     {kwargs['categorylevel']}, \"{kwargs['categoryname']}\", {kwargs['categoryparent']})"

    return insert_sentence


def rebuild(database):

    if os.path.exists(database):
        os.remove(database)

    ddl_table_main_category = """ CREATE TABLE IF NOT EXISTS main_category(
                                    main_id integer primary key autoincrement,
                                    count integer,
                                    uptime text null,
                                    cversion integer null,
                                    rpriceallowed text null,
                                    minpriceallowed text null,
                                    xmltimestamp  text null,
                                    xmlack  text null,
                                    xmlversion integer null,
                                    xmlbuild text null
                                ); """
    ddl_table_categories = """CREATE TABLE IF NOT EXISTS categories(
                                categories_id integer primary key autoincrement,
                                categoryid integer,
                                bestoffer text null,
                                autopay text null,
                                categorylevel integer null,
                                categoryname text null,
                                categoryparent integer null
                            ); """

    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create main_category table
        execute_ddl(conn, ddl_table_main_category)
        # create categories table
        execute_ddl(conn, ddl_table_categories)

        # path of the xml
        # path = './resource/categories_short.xml'
        path = './resource/categories.xml'

        # namespace used on the xml
        ns = {'ns': 'urn:ebay:apis:eBLBaseComponents'}

        read_xml(path, ns, conn)

    else:
        print(f"Problems with the connection to the database: {database}")


def html_table(list_to_print):
    pass


def get_category(id, conn):
    try:
        category = None
        cursor = conn.cursor()
        cursor.execute(f"SELECT * from categories where categoryid = {id}")
        category = cursor.fetchone()
        return category
    except Error as e:
        print(
            f"Problems reading data from database table categories, error:{e}")


def get_childcategories(id, conn):
    try:
        categories = None
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT * from categories where categoryparent = {id} and categoryid <> {id} ")
        categories = cursor.fetchall()
        return categories
    except Error as e:
        print(
            f"Problems reading data from table categories categoryparent, error:{e}")


def render_category_list(f, category, conn):
    try:
        list_header = "<ul>"
        f.write(list_header)
        name = str(category[5])
        list_item = "<li>" + name + "</li>"
        f.write(list_item)
        categoryId = category[1]
        children = get_childcategories(categoryId, conn)
        if children != None and len(children) > 0:
            for child in children:
                render_category_list(f, child, conn)
                list_footer = "</ul>"
                f.write(list_footer)
    except Error as e:
        print(f"Problems rendering data {category[5]}, error:{e}")


def render(database, id):
    try:
        conn = sqlite3.connect(database)
        category = get_category(id, conn)
        html_file_name = id + '.html'
        f = open(html_file_name, 'w')
        header = """<!DOCTYPE html >
        <head >
        <meta charset ="utf-8">
        <link rel ="stylesheet" type ="text/css" href ="https: // maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css">
        <link href ="http: // fonts.googleapis.com/css?family = Open+Sans" rel ="stylesheet" type ="text/css">
        </head>
        <body>
        <h2> Ebay Categories List </h2>"""
        f.write(header)
        render_category_list(f, category, conn)
        conn.close()

    except Error as e:
        print(f"Problems reading data from database{database}, error:{e}")


def main(mode, id):
    database = r".\db\categories.db"

    if mode == "--rebuild":
        rebuild(database)
    elif mode == "--render":
        render(database, id)
    else:
        print(f"Unknown mode:{mode} {id}")


if __name__ == '__main__':

    numparams = len(sys.argv)
    if numparams == 2:
        main(sys.argv[1], 0)
    elif numparams == 3:
        main(sys.argv[1], sys.argv[2])
    else:
        print("Problems with the paramethers")
