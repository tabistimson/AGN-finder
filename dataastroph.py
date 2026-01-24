import matplotlib.pyplot as plt
import csv 

#creating usable data from WISE data 
def wisedata(): 
    w_data = []
    agns = []
    with open('astroph/wise_galaxies.csv') as wisedata:
        wisereader = csv.DictReader(wisedata)
        for row in wisereader: 
            w_data.append({"w_ra":row["ra"], "w_dec":row["dec"], "w1":row["w1mpro"], "w2":row["w2mpro"], "w3":row["w3mpro"]})
    with open('astroph/wise_quasars.csv') as wiseagns:
        wisereader = csv.DictReader(wiseagns)
        for row in wisereader: 
            agns.append({"w_ra":row["ra"], "w_dec":row["dec"], "w1":row["w1mpro"], "w2":row["w2mpro"], "w3":row["w3mpro"]})
    return w_data , agns

#creating usable SDSS data 
def SDSSdata():
    data = []
    data2 = []
    #opening QSO file (file) and normal galaxy file (file2)
    with open('astroph/quasars.csv') as file, open('astroph/galaxies.csv') as file2:
        reader = csv.DictReader(file)
        reader2 = csv.DictReader(file2)
        for row in reader: 
            if -500 < float(row["u"])- float(row["g"]) < 500 and -500 < float(row["g"])-float(row["r"]) < 500 and -100<float(row["z"])<100: #constraints are to clear out null data
                data.append({"u":row["u"], "g":row["g"], "r":row["r"], "objID":row["objID"], "ra":row["ra"], "dec":row["dec"], "z":row["z"]})
        for row in reader2: 
            if -500 < float(row["u"])- float(row["g"]) < 500 and -9 < float(row["g"])-float(row["r"]) < 500 and -100<float(row["z"])<100: #constraints are to clear out null data
                data2.append({"u":row["u"], "g":row["g"], "r":row["r"], "objID":row["objID"], "ra":row["ra"], "dec":row["dec"], "z":row["z"]})

    return data, data2

#sorting through WISE data to find if W1-W2>0.8 and making a color color diagram
def infrared(w_data, agns): 
    w12 = []
    w23 = []
    w12agn =[]
    w23agn = []
    for row in w_data: 
        w12.append(float(row["w1"]) - float(row["w2"]))
        w23.append(float(row["w2"]) - float(row["w3"]))
    for row in agns: 
        w12agn.append(float(row["w1"]) - float(row["w2"]))
        w23agn.append(float(row["w2"]) - float(row["w3"]))

    plt.scatter(w12, w23, c='red',  s=3, alpha=0.5, label="random galaxies")
    plt.scatter(w12agn, w23agn, c='blue', s=3, alpha=0.5, label="QSOs")
    plt.xlabel("w1-w2")
    plt.ylabel("w2-w3")
    plt.legend()
    plt.show()
    
#creating color color graphs using SDSS data
def colorcolor(data, data2): 
    agncand_ug = []  
    agncand_gr = []
    gal_ug = []
    gal_gr = []
    agnz = []
    galz = []
    for row in data: 
        agncand_ug.append(float(row["u"]) - float(row["g"]))
        agncand_gr.append(float(row["g"]) - float(row["r"]))
        agnz.append(float(row["z"]))
    for row in data2: 
        gal_ug.append(float(row["u"]) - float(row["g"]))
        gal_gr.append(float(row["g"]) - float(row["r"]))
        galz.append(float(row["z"]))
    
    plt.scatter(gal_gr, gal_ug, c=galz, cmap='Blues', s=3, alpha=0.5, label="random galaxies ")
    plt.colorbar(label='Redshift (z)')
    plt.scatter(agncand_gr, agncand_ug, c=agnz, cmap='Oranges', s=3, alpha=0.5, label="QSOs")
    plt.colorbar(label='Redshift of QSO (z)')
    plt.ylabel("u-g")
    plt.xlabel("g-r")
    plt.legend()
    plt.show()

#running the program
def main(): 
    w_data , agns = wisedata()
    data , data2 = SDSSdata()
    colorcolor(data, data2)
    infrared(w_data, agns)
    agns = []


if __name__ == "__main__":
    main()
