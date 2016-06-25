# Read a file and convert each line to set items
def file_to_set(filename):
    results = set()
    with open(filename, 'rt') as f:
        for line in f:
            results.add(line.replace('\n', ''))
    return results


# Iterate through a set, each item will be a line in a file
def set_to_file(links, filename):
    with open(filename, "w") as f:
        for l in sorted(links):
            f.write(l+"\n")
