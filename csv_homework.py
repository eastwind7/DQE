import argparse
import csv
import locale

locale.setlocale(locale.LC_ALL, 'en_US.utf8')
'en_US.utf8'


def parse_arguments():
    parser = argparse.ArgumentParser(description='BED HRR')
    parser.add_argument('-bed', type=int, help='bed argument')
    parser.add_argument('-path', type=str, help='path to csv')
    return parser.parse_args()


args = parse_arguments()
# args
with open(args.path) as f:
    d = csv.DictReader(f)
    extracted_data = []
    for row in d:
        extracted_data.append((row['HRR'], row['Available Hospital Beds'], row['Total Hospital Beds']))
    if extracted_data[0][1] == '':
        extracted_data = extracted_data[1:]
    result = map(lambda x: (x[0], locale.atof(x[1]) * 100 / locale.atof(x[2])), extracted_data)
    result = sorted(result, key=lambda x: x[1], reverse=True)
if args.bed > len(result):
    n = 3
else:
    n = args.bed
for i in range(args.bed):
    print("{0} {1:.2f} %".format(result[i][0], result[i][1]))
