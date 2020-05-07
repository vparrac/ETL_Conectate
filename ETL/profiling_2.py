import csv
import glob
from datetime import datetime


f= open("guru99.txt","w+")
listaClases=[]
listaCursos=[]
codigoPorCurso={}
retirosPorCurso={}
inscritosCurso={}
notaPorEstudiante={}
estudiantesCurso={}
profesorPorCurso={}

path='./GT1Datos/Out20190404092503CTE19GES-CursosConectaTEInscritosRetirados2013A2017.csv'
path_2='./GT1Datos/Out2019040409284320190403-EA-CursosConectaTEEstNotaPrmSemPrmAca2013A2017.csv'

with open(path_2) as csv_file:  
    csv_reader = csv.reader(csv_file, delimiter=';')        
    for row in csv_reader:
        crn=row[3]
        if(row[4].__contains__('profesor')):
            profesorPorCurso.update({row[3]:row[4]})
        else:
            if crn in notaPorEstudiante:
                listaEstudiantes=notaPorEstudiante[crn]
                login=row[4]
                nota='null'
                if row[5]!='':
                    nota=float(row[5].replace(',','.',1))
                listaEstudiantes.update({login:nota})
            else:
                estudiantes={}
                login=row[4]
                nota='null'
                if row[5]!='':
                    nota=float(row[5].replace(',','.',1))
                estudiantes.update({login:nota})
                notaPorEstudiante.update({row[3]:estudiantes})


with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')        
        for row in csv_reader:     
            retirosPorCurso.update({row[2]:row[3]})
            inscritosCurso.update({row[2]:row[4]})
            if not listaClases.__contains__(row[2]):
                listaClases.append(row[2])
            if not listaCursos.__contains__(row[1]):
                listaCursos.append(row[1])
            codigoPorCurso.update({row[2]:row[1]})


listA=['./GT1Datos/Encuestas_Individuales/Categorizados/*']
files_ind = glob.glob(listA[0])
categorias_i=["HT","AC","O","C","A","I","E"]
diccionario = {}

def processStudent(row, categorias, numeroElementosCategorias, sumaTotalCategorias):
    for index in range(len(categorias)):
        valorFila= categorias[index]     
        for value in valorFila:  
            if row[value]!='':
                numeroElementosCategorias[index]+=1               
                sumaTotalCategorias[index]+=int(row[value])

for file_path in files_ind:
    print(file_path)
    previousRow=[]
    findFirstStudent=True
    categorias=[[],[],[],[],[],[],[]]
    sumaTotalCategorias=[0]*len(categorias_i)
    numeroElementosCategorias=[0]*len(categorias_i)
    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')           
        for row in csv_reader:            
            if findFirstStudent:                
                try:
                    x = int(row[0])
                    findFirstStudent=False                          
                    for index in range(len(previousRow)):  
                        # if(index==len(previousRow)-1):
                        #     pdb.set_trace()  
                        if "_" not in previousRow[index]: 
                            continue                             
                        categoria=previousRow[index].split("_")                        
                        categoriaEncuesta=categoria[0]
                        #Mirar los casos de las categorías de dos carácteres primero
                        initial = categoriaEncuesta[:2]
                        if(initial==categorias_i[0]):
                            categorias[0].append(index)
                        elif initial==categorias_i[1]:
                            categorias[1].append(index)
                        else:
                            initial = categoriaEncuesta[:1]
                            if categorias_i.__contains__(initial):
                                valor=categorias_i.index(initial)
                                categorias[valor].append(index)    
                            elif initial=='0':
                                continue
                            else:
                                import pdb; pdb.set_trace()
                                raise Exception('Categoria no encontrada',categoriaEncuesta[:1] )                         
                    processStudent(row=row,categorias=categorias,numeroElementosCategorias=numeroElementosCategorias,sumaTotalCategorias=sumaTotalCategorias)
                    #Una vez aquí se procesa al estudiante                    
                except ValueError:                         
                    previousRow=row                    
                    pass
            else:                
                processStudent(row=row,categorias=categorias,numeroElementosCategorias=numeroElementosCategorias,sumaTotalCategorias=sumaTotalCategorias)
    nombreCSV=file_path.split('\\')
    crn=nombreCSV[len(nombreCSV)-1].split(".")[0]   
    

    if not crn in retirosPorCurso:
        print('crn no está')
    else:
        print('crn está')

    print(categorias)
    print(sumaTotalCategorias)
    print(numeroElementosCategorias)    

f.close()