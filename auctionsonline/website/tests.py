import psycopg2

try:
    connection = psycopg2.connection(user="admin",
                                  password="admin2023",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="leilao")
    cursor = connection.cursor()

    postgres_insert_query = "CALL inserir_user('username', 'password', 'email@example.com', 'Primeiro Nome', 'Último Nome', 100.00, '123456789','Rua Principal', 'Cidade', '12345', 'País','2023-08-13');"
    cursor.execute(postgres_insert_query)

    connection.commit()
    count = cursor.rowcount
    print(count, "Record inserted successfully into mobile table")

except (Exception, psycopg2.Error) as error:
    print("Failed to insert record into mobile table", error)

finally:
    # closing database connection.
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")