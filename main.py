import time
from grasp import *
# from prueba import *
import argparse
from tqdm import tqdm
import json

argparser = argparse.ArgumentParser()
argparser.add_argument('-r', '--random', help='mezcla de datos al incio del algoritmo', default=True)
argparser.add_argument('-i', '--iteraciones',help='numero de iteraciones que hace el algoritmo', default=5)
argparser.add_argument('-s', '--seed', help='semilla que utilizamos para el randomizado de los datos', default=None)
argparser.add_argument('-a', '--alfa', help='cojunto de valores que puede tomar alfa, cuan mas grande el valor mas divisiones de alfa, multiplos de 10', default=None)
argparser.add_argument('-g', '--save', help='Guarda la solución en un fichero llamado "solution_json.json"', default=False)
argparser.add_argument('-l', '--lcr', help='Tamaño de la lista de candidatos', default=3)
argparser.add_argument('-x', '--stock', help='Path al fichero csv de stock', default="./data/stock.csv")
argparser.add_argument('-y', '--viajes', help='Path al fichero xml de viajes', default="./data/viajes.xml",)
argparser.add_argument('-z', '--precios', help='Path al fichero csv de precios', default="./data/precios.csv")
args = argparser.parse_args()

print("Config: Inter -> {},\n \tAlfa -> {},\n \tLCR ->{},\n \tAutosave -> {}".format(args.iteraciones,args.alfa if args.alfa != None else 0.5 ,args.lcr,args.save))
start_time = time.time()
sol = {}
val = {}
sum_val = {}
for i in tqdm(range(int(args.iteraciones))):
    g = Grasp(args.random, args.seed, args.stock,args.viajes,args.precios)
    if args.alfa == None:
        x = g.GRASP_Solution()
        sol[i] = x[0]
        val[i] = x[1]
        
    else:
        for alfa in range(int(args.alfa)+1):
            x = g.GRASP_Solution(alfa/int(args.alfa),args.lcr,i)
            sum_val[str(alfa/int(args.alfa))] = sum_val[str(alfa/int(args.alfa))] + x[1] if str(alfa/int(args.alfa)) in sum_val.keys() else x[1]
            if i == 0:
                sol = x[0]
                val = x[1]
            else:
                if val >= x[1]:
                    sol = x[0]
                    val = x[1]




if args.alfa == None:
    new_val = 0
    new_sol = {}
    for i in val.keys():
        print("---> Iter {} fitness: {}".format(i,val[i]))
        if new_val == 0:
            new_val = val[i]
            new_sol = sol[i]
        elif val[i] < new_val:
            new_val = val[i]
            new_sol = sol[i]
    val = new_val
    sol = new_sol
        
else:
    for x in sum_val:
        print("---> Media fitness {}: {}".format(x,sum_val[x]/int(args.iteraciones)))


if(args.save):
    with open('solution_json.json', 'w') as outfile:
        json.dump(sol, outfile)
print("---> Mejor fitness: {}".format(val))
print("--- {} seconds ---".format(time.time() - start_time))
