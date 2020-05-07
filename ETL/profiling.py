import glob
files_ind = glob.glob('./GT1Datos/Encuestas_Individuales/*')
files_mul = glob.glob('./GT1Datos/Encuestas_Multiples_CRN/*')
import csv
import statistics as s
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

#print("Cantidad de Archivos individuales",len(files_ind))
#print("Cantidad de Archivos multiples",len(files_mul))

registers=[]
labels=[]

for file_path in files_ind:
    arra=file_path.split("\\")
    labels.append(arra[len(arra)-1])
    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        line_count = 0
        for row in csv_reader:
            try:
                x = int(row[0])
                line_count +=1    
            except ValueError:                
                pass
    registers.append(line_count)

print("Median: ", s.mean(registers))
print("Desvesta ", s.variance(registers))
sum = 0
for number in range(len(registers)):
    sum+=registers[number]

print("Total ", sum)

objects = labels
y_pos = np.arange(len(objects))
performance = registers

np.random.seed(19680801)

plt.rcdefaults()
fig, ax = plt.subplots()




# Example data
people = labels
y_pos = np.arange(len(labels))
performance = registers


ax.barh(y_pos, performance, align='center')
ax.set_yticks(y_pos)
ax.set_yticklabels(people)
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xlabel('Número de encuestas totales')


plt.show()