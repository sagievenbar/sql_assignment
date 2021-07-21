import mysql.connector


def connect_mysql(host_name, user_name, password):
    print('Connect to MySQL')
    try:
        connection = mysql.connector.connect(host=host_name, user=user_name, password=password)
        print('Connection success')
        return connection
    except mysql.connector.errors.ProgrammingError:
        print('ERROR: Incorrect password or username, Try again')
        return None
    except mysql.connector.errors.DatabaseError:
        print('ERROR: Incorrect hostname, Try again')
        return None


def create_database(connection, db_name):
    print('Create Database')
    cursor = connection.cursor()
    cursor.execute('SHOW DATABASES')
    res = cursor.fetchall()
    if (db_name,) not in res:
        cursor.execute('CREATE DATABASE  `%s`' % db_name)
        print('Database {} created'.format(db_name))
    else:
        print('Database {} already exists'.format(db_name))
    connection.close()


def create_table(host_name, user_name, password, db_name, tb_name, cols):
    print('Create Table')
    connection_with_table = mysql.connector.connect(host=host_name, user=user_name, password=password, database=db_name)
    cursor = connection_with_table.cursor()
    cursor.execute('SHOW TABLES')
    res = cursor.fetchall()
    if (tb_name,) in res:
        print('ERROR: Table {} already exists'.format(tb_name))
        connection_with_table.close()
        exit(1)

    cursor.execute('CREATE table {} ({})'.format(tb_name, cols))
    print('Table {} created successfully'.format(tb_name))
    return connection_with_table


def insert_into_tables(connection_with_table, tb_name, data):
    print('Insert the data into the table')
    cursor = connection_with_table.cursor()
    for i in data:
        cursor.execute('INSERT INTO {} values {}'.format(tb_name, i))
        connection_with_table.commit()

    print('The table has been updated')


cols_list = 'Acode int, Name text, Established year, Hub text, Destinations int, Alliance text, Planes int, Avgprice text'
data_list = [(1, 'Lufthansa', 1955, 'Germany', 220, 'Star', 294, '1,183$'),
             (2, 'Swiss', 2002, 'Switzerland', 102, 'Star', 89, '1,674$'),
             (3, 'Elal', 1948, 'Israel', 60, 'Matmid', 43, '984$'),
             (4, 'TurkishAirlines', 1933, 'Turkia', 304, 'Star', 338, '1,298$'),
             (5, 'AirCanada', 1937, 'Canada', 222, 'Star', 189, '1,167$'),
             (6, 'BritishAirways', 1974, 'UK', 183, 'OneWorld', 277, '1,535$'),
             (7, 'UnitedAirlines', 1926, 'USA', 342, 'Star', 781, '1,116$'),
             (8, 'CathayPacific', 1946, 'China', 77, 'OneWorld', 153, '1,636$')]


def main():
    host_name = input('Please enter the host name: ')
    user_name = input('Please enter the user name: ')
    password = input('Please enter the password: ')
    db_name = input('Please enter Database name: ')
    tb_name = input('Please enter Table name: ')

    connection = connect_mysql(host_name, user_name, password)
    if connection is None:
        exit(1)

    create_database(connection, db_name)

    connection_with_table = create_table(host_name, user_name, password, db_name, tb_name, cols_list)
    insert_into_tables(connection_with_table, tb_name, data_list)
    connection_with_table.close()


if __name__ == "__main__":
    main()