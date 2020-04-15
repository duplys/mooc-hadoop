from pyspark import SparkContext

sc = SparkContext()

fileA = sc.textFile('/user/cloudera/input/join1_FileA.txt')

print(fileA.collect())

fileB = sc.textFile('/user/cloudera/input/join1_FileB.txt')

print(fileB.collect())

def split_fileA(line):
    tokens = line.split(',')
    word = tokens[0]
    count = int(tokens[1])
    
    return (word, count)


def split_fileB(line):
    # split the input line into word, date and count_string
    tokens0 = line.split(',')
    count_string = tokens0[1]
    tokens1 = tokens0[0].split()
    date = tokens1[0]
    word = tokens1[1]
    return (word, date + " " + count_string)

test_line = "able,991"

print(split_fileA(test_line))

fileA_data = fileA.map(split_fileA)
print(fileA_data.collect())

 
fileB_data = fileB.map(split_fileB)
print(fileB_data.collect())

fileB_joined_fileA = fileB_data.join(fileA_data)

print(fileB_joined_fileA.collect())