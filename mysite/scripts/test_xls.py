import csv
import xlwt
import os
# csv to xls
def run():
    resultexcel = xlwt.Workbook()
    resultsheet = resultexcel.add_sheet("result")
    csvfile = open(os.path.join("/home/lsl/InitData/Output", "Result.csv"), 'r')
    reader = csv.reader(csvfile)
    l = 0
    for line in reader:
        r = 0
        for i in line:
            resultsheet.write(l, r, i)
            r = r + 1
        l = l + 1
    resultexcel.save(os.path.join("/home/lsl/InitData/Output", "Result.xls"))
    print("OK")