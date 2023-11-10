def make_csv(filename):
    """
    Make a new copy of a file removing all spaces that are preceded by commas.
    """
    new_lines = []
    with open(filename, 'r+', encoding='latin-1') as f:
        try:
            for line in f:
                line_copy = line[0]
                for x in range(1, len(line)):
                    # If the current character is a space preceded by a comma, DON'T copy it
                    if line[x] == ' ' and line[x-1] == ',':
                        continue
                    else:
                        line_copy += line[x]
                new_lines.append(line_copy)
        except UnicodeDecodeError as err:
            print(err)
            raise

    new_filename = f"{filename[:-4]}_new.csv"
    with open(new_filename, 'a', encoding='latin-1') as f:
         f.writelines(new_lines)
    
    return

def add_url_as_id(filename):
    """
    Open sellers csv file, parse out the hyperlink, insert the unique portion
    of the hyperlink at the front of the line, and create a new file with the
    updated lines.
    """
    with open(filename, 'r', encoding='latin-1') as f:
        try:
            new_lines = []
            for line in f:
                line_parts = line.split(',')
                shop_link = line_parts[1]
                # Find the '/' preceding the unique link section and slice
                target_index = shop_link.rfind('/')
                target = shop_link[target_index + 1:]
                line_parts.insert(0, target)
                new_lines.append((',').join(line_parts))
        except Exception as err:
            print(err)
            raise

        new_filename = f"{filename[:-4]}_with_key.csv"
        with open(new_filename, 'a', encoding='latin-1') as f:
            f.writelines(new_lines)


if __name__ == '__main__':
    filename = 'data/sellers_Tue_05_Sep_2023_02_04AM_with_key.csv'
    # filename = 'data/three_sellers.txt'
    make_csv(filename)
    # add_url_as_id(filename)
    print("Done")
