import csv
import getopt
import sys

def main(argv):
    # Arguments
    kofam_file = ''
    database_file = ''

    output_matched = ''

    try:
        opts, args = getopt.getopt(argv, "hk:d:o:", ["kofam=","database=","matched_output="])
    except getopt.GetoptError as e:
        print("Error:")
        print(e)
        print('\nUsage:')
        print('  python3 find.py -k <kofam result file> -d <SearchKEGG file> -o <output>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('find.py -k <kofam result file> -d <SearchKEGG file> -o <output>')
            sys.exit()
        elif opt in ('-k', '--kofam'):
            kofam_file = arg
        elif opt in ('-d', '--database'):
            database_file = arg
        elif opt in ('-o', '--output'):
            output_matched = arg

    if kofam_file == '' or database_file == '' or output_matched == '':
        print('find.py -k <kofam result file> -d <SearchKEGG file> -o <output>')
        sys.exit(2)

    # Input
    res_file = open(kofam_file)
    kofam_res = csv.reader(res_file, delimiter="\t")
    kofam = []
    for row in kofam_res:
        if len(row) < 2:
            continue
        row[1] = "".join(filter(str.isalnum, row[1]))
        kofam.append(row)

    # Database
    kegg_file = open(database_file)
    kegg_db = csv.reader(kegg_file, delimiter=",")
    kegg = []
    for row in kegg_db:
        row[1] = "".join(filter(str.isalnum, row[1]))
        kegg.append(row)

    # Filter
    result = []
    for row in kegg:
        b = [x for x in kofam if x[1] == row[1]]
        if not b:
            row.append("not found")
        else:
            row.append("found")
        result.append(row)

    # Output
    with open(output_matched, 'w', newline='\n') as f_output:
        tsv_output = csv.writer(f_output, delimiter=',')
        for row in result:
            tsv_output.writerow(row)

if __name__ == "__main__":
   main(sys.argv[1:])
