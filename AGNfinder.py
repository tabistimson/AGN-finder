from astroquery.ipac.irsa import Irsa
from astropy.coordinates import SkyCoord
import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np
import csv 
from astroquery.sdss import SDSS

#querying WISE data 
def WISEquery(righta, declin):
    #base coordinates used for test = ra=348.9563679, dec=1.2869483
    coord = SkyCoord(ra=righta, dec=declin, unit='deg', frame='icrs')
    #querying the region 500 arcsec around the coordinate
    wise = Irsa.query_region(coordinates=coord, catalog="allwise_p3as_psd", radius=500*u.arcsec, columns='ra, dec, w1mpro, w2mpro')
    wise.write('astroph/wisedata.csv', overwrite=True)
       
#creating usable data from WISE data 
def wisedata(): 
    w_data = []
    with open('astroph/wisedata.csv') as wisedata:
        wisereader = csv.DictReader(wisedata)
        for row in wisereader: 
            w_data.append({"w_ra":row["ra"], "w_dec":row["dec"], "w1":row["w1mpro"], "w2":row["w2mpro"]})
    return w_data
    
#creates a list of coordinates collected in WISE data
def coords(w_data): 
    coords = []
    for row in w_data: 
        ra = row["w_ra"]
        dec = row["w_dec"]
        coord = SkyCoord(ra=ra, dec=dec, unit='deg', frame='icrs')
        coords.append(coord)
    return coords

#querying SDSS data based off the coordinates from WISE 
def query_SDSS(coord):
    sdss = SDSS.query_region(coord, radius=1*u.arcsec, fields=['ra', 'dec', 'u', 'g', 'r', 'z'])
    sdss.write('astroph/output2.csv', overwrite=True)

#creating usable SDSS data 
def SDSSdata():
    data = []
    with open('astroph/output2.csv') as file:
        reader = csv.DictReader(file)
        for row in reader: 
            if -500 < float(row["u"])- float(row["g"]) < 500 and -500 < float(row["g"])-float(row["r"]) < 500 and -100<float(row["z"])<100: #constraints are to clear out null data
                data.append({"u":row["u"], "g":row["g"], "r":row["r"], "objID":row["objID"], "ra":row["ra"], "dec":row["dec"], "z":row["z"]})
    return data

#sorting through WISE data to find if W1-W2>0.8
def infrared(w_data): 
    agnra = []
    agndec = []
    for row in w_data: 
        w12= float(row["w1"]) - float(row["w2"])
        if w12 > 0.8: 
            agnra.append(float(row["w_ra"]))
            agndec.append(float(row["w_dec"]))
    return agnra, agndec

#creating color color graphs using SDSS data
def colorcolor(data): 
    agncand_ug = []  
    agncand_gr = []
    agncandra = []
    agncanddec = []
    agnradec = []
    ug= []
    gr= []
    for row in data: 
        if -0.1 < (float(row["g"])-float(row["r"])) < 0.6 and (float(row["u"])-float(row["g"])) < 4 and 14 < float(row['z']) < 23:
            agncand_ug.append(float(row["u"]) - float(row["g"]))
            agncand_gr.append(float(row["g"]) - float(row["r"]))
            agncandra.append(float(row["ra"]))
            agncanddec.append(float(row["dec"]))
            agnradec.append({"ra":row["ra"], "dec":(row["dec"])})
        else:
            ug.append((float(row["u"]) - float(row["g"])))
            gr.append(float(row["g"]) - float(row["r"]))

    plt.scatter(gr, ug, c='red', s=3, label="all objects")
    plt.scatter(agncand_gr, agncand_ug, c='green', s=3, alpha=0.5, label="AGN candidates")
    plt.ylabel("u-g")
    plt.xlabel("g-r")
    plt.legend()
    plt.show()
    return agncandra, agncanddec , agnradec


    #plotting 
    cra = [float(x) / 180 * np.pi for x in cra]
    cdec = [float(x) for x in cdec]
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    theta = [x / 180.0 * np.pi for x in ra]
    ax.set_ylim(dec[0]-(300/3600), dec[0]+(300/3600))
    ax.set_xlim(theta[0]-(100/3600), theta[0]+(100/3600))
    ax.scatter(cra, cdec, c='blue', s=6, label="color")
    ax.scatter(theta, dec, c='red', s=6, label="candidates")
    plt.legend()
    plt.show()

#making a cartesian graph of all infrared candidates, color-color candidates, and candidates that fulfill both requirements
def cartesian(ra, dec,cra, cdec, ira, idec):
    plt.scatter(cra, cdec, c='blue', s=6, label="color")
    plt.scatter(ira, idec, c='green', s=6, label="infrared")
    plt.scatter(ra, dec, c='red', s=6, label="both color and infrared")
    plt.gca().invert_xaxis()
    plt.ylabel("dec")
    plt.xlabel("ra")
    plt.legend()
    plt.show()
    
def make_file(agns):
    with open('astroph/finaltext.txt', 'w', newline='') as final:
        final.write("ra,dec\n")
        for row in agns: 
            final.write(f"{row["ra"]},{row["dec"]}\n")

#running the program
def main(): 
    ra = input("RA: ")
    dec = input("DEC: ")
    WISEquery(ra, dec)
    w_data = wisedata()
    coord = coords(w_data)
    query_SDSS(coord)
    data = SDSSdata()
    agn_ra_color, agn_dec_color, agnradec= colorcolor(data)
    agn_ra_inf, agn_dec_inf = infrared(w_data)
    agns = []

    #cross matching coordinates
    for row in agnradec: 
        ra , dec = float(row["ra"]), float(row["dec"])
        for dec_i in agn_dec_inf:
            #assuming a maximum difference of 6 arcseconds in declination 
            coord = {"ra":f"{ra:.5f}", "dec":f"{dec:.5f}"}
            if (-6/3600) < (dec_i - dec) < (6/3600) and coord not in agns:
                agns.append(coord)
    fullra = [float(row["ra"]) for row in agns]
    fulldec = [float(row["dec"]) for row in agns]
    cartesian(fullra, fulldec, agn_ra_color, agn_dec_color, agn_ra_inf, agn_dec_inf)
    make_file(agns)
    
    
if __name__ == "__main__":
    main()
