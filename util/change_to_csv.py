def make_csv(filename):
    new_lines = []
    with open(filename, 'r', encoding='latin-1') as f:
        try:
            for line in f:
                line_copy = line[0]
                for x in range(1, len(line)):
                    if line[x] == ' ' and line[x-1] == ',':
                        continue
                    else:
                        line_copy += line[x]
                new_lines.append(line_copy)
        except UnicodeDecodeError as err:
            print(err)
            raise

    new_filename = f"{filename[:-3]}csv"
    with open(new_filename, 'a', encoding='latin-1') as f:
         f.writelines(new_lines)
    
    return

def add_url_as_id(filename):
    """
    Open sellers csv file, parse out the hyperlink, insert the unique portion
    of the hyperlink at the front of the line
    """
    with open(filename, 'r', encoding='latin-1') as f:
        try:
            for line in f:
                line_parts = line.split(',')
                shop_link = line_parts[1]
                # Find the '/' preceding the unique link section and slice
                target_index = shop_link.rfind('/')
                target = shop_link[target_index + 1:]
        except Exception as err:
            print(err)
            raise


if __name__ == '__main__':
    filename = 'data/sellers_Tue_05_Sep_2023_02_04AM.txt'
    make_csv(filename)
    print("Done")
