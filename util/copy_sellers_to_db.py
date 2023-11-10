import psycopg2
import psycopg2.extras
from typing import List, Tuple

def connect_to_db(db_params):
    conn = None
    try:
        conn = psycopg2.connect(**db_params)
    except (Exception, psycopg2.DatabaseError) as err:
        print(err)
        exit(1)
    print("Connection successful")
    return conn

def copy_to_db(conn, source_file):
    """
    Commit CSV values to the card shops database.
    """
    # TODO, we thought we couldn't use copy_from because of the UUID column
    # and the fact that the csv file does not have UUIDs inside.
    # however, using a UUID seems overkill.
    # We can use each shop's hyperlink as a unique identifier.
    RATING_IDX = 3
    SALES_IDX = 4
    STATE_IDX = 5
    field_names = [
        'db_id', 'shop_name', 'hyperlink', 'rating', 'num_sales', 'state'
    ]
    # create list of dictionary objects for each entry in the csv file
    csv_data = []
    with open(source_file) as f:
        for line in f:
            sl = line.split(',')
            sl[RATING_IDX] = float(sl[RATING_IDX])
            sl[SALES_IDX] = int(sl[SALES_IDX])
            sl[STATE_IDX] = sl[STATE_IDX][:-1] # Remove the newline character
            csv_data.append(dict(zip(field_names, sl)))
    # Create cursor to execute queries. context manager handles committing and closing cursor
    with conn.cursor() as db_cursor:
        insert_query = """INSERT INTO card_shops (db_id, shop_name, hyperlink, rating, num_sales, state) VALUES (%(db_id)s, %(shop_name)s, %(hyperlink)s, %(rating)s, %(num_sales)s, %(state)s);"""
        psycopg2.extras.execute_batch(db_cursor, insert_query, csv_data)
        conn.commit()
    print("Exited psql context manager")

def prepare_data_for_insertion(filename) -> List[Tuple]:
    """
    """
    parsed_shop_data = []
    with open(filename) as f:
        for line in f:
            line_parts = line.split(',')
            # Find the '/' preceding the unique link section and slice
            shop_link = line_parts[1]
            target_index = shop_link.rfind('/')
            target = shop_link[target_index + 1:]
            # Remove the newline character from the shop location string
            line_parts[4] = line_parts[4][:-1]
            parsed_shop_data.append((target, *line_parts))

    return parsed_shop_data

def test_helper():
    source_file = "/Users/brandon/myprograms/web_stuff/tcg-shop-locator/data/three_sellers.txt"
    parsed_data = prepare_data_for_insertion(source_file)
    for item in parsed_data:
        print(item)
    return


def main():
    db_conn_params = {
        "host"  : "localhost",
        "dbname": "tcg_shops",
        "user"  : "postgres"
    }
    # source_file = "data/three_sellers.csv"
    source_file = "data/sellers_Tue_05_Sep_2023_02_04AM_with_key_new.csv"

    db_conn = connect_to_db(db_conn_params)
    copy_to_db(db_conn, source_file)
    db_conn.close()

if __name__ == '__main__':
    main()
    # test_helper()
