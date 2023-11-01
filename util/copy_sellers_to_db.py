import psycopg2
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

def copy_to_db(conn):
    source_file = "data/three_sellers.txt"
    # Create cursor to execute queries
    db_cursor = conn.cursor()
    # TODO, we thought we couldn't use copy_from because of the UUID column
    # and the fact that the csv file does not have UUIDs inside.
    # however, using a UUID seems overkill.
    # We can use each shop's hyperlink as a unique identifier.
    # We should do some file processing to insert the hyperlink at the start of
    # every line in the csv file
    with open(source_file) as f:
        for line in f:
            line_parts = line.split(',')
            shop_link = line_parts[1]
            # Find the '/' preceding the unique link section and slice
            target_index = shop_link.rfind('/')
            target = shop_link[target_index + 1:]
        
    conn.commit()
    db_cursor.close()

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
        "dbname": "mtg_info",
        "user"  : "brandon"
    }

    db_conn = connect_to_db(db_conn_params)
    copy_to_db(db_conn)
    db_conn.close()

if __name__ == '__main__':
    #main()
    test_helper()
