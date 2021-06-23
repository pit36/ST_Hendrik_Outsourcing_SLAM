import csv

# this imports the test.csv and returns testA.csv testB.csv respectively


def writetoseperatecsv(inputrow):
    targetfile= 'test'+ inputrow[0] + '.csv'
    targetrow=inputrow
    with open(targetfile,'a') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t')
        writer.writerow(targetrow)

with open('test.csv', 'r') as file:
    reader = csv.reader(file, delimiter = '\t')
    for row in reader:
        if row[0]!='Art der Messung':
            writetoseperatecsv(row)


