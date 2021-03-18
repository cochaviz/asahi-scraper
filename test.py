import csv

filename = "test"

list1 = list(range(0, 5))
list2 = list(range(5, 10))
list3 = list(range(10, 15))

with open(filename + ".csv", 'w', newline='') as myfile:
    print("Created " + filename + ".csv")

myfile = open(filename + ".csv", 'a', newline='')

print("Opened file: " + filename + ".csv")
file_writer = csv.writer(myfile, quoting=csv.QUOTE_ALL)

print("Appending to file...")
file_writer.writerow(list1)

print("Appending to file...")
file_writer.writerow(list2)

print("Appending to file...")
file_writer.writerow(list3)
