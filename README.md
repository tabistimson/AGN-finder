# AGN Identification Using SDSS and WISE Data

## Project Summary

This project focuses on identifying Active Galactic Nuclei (AGN) around a specified sky coordinate using Sloan Digital Sky Survey (SDSS) photometric data and Wide-field Infrared Survey Explorer (WISE) infrared data. The pipeline queries all objects within a 500 arcsecond cone centered on a given coordinate, applies a set of optical and infrared selection criteria, and outputs:

* A color–color diagram in optical bands
* A sky map in Cartesian coordinates
* A text file containing candidate AGN coordinates

The goal is to identify likely AGN (with an emphasis on quasars) based on their infrared and optical properties.

---

## Introduction

Active Galactic Nuclei (AGN) are extremely luminous galaxies powered by accretion onto supermassive black holes (SMBHs) at their centers. Prominent subclasses include quasars and Seyfert galaxies. As matter accretes onto the SMBH, large amounts of energy are emitted across the electromagnetic spectrum.

Studying AGN properties helps constrain models of SMBH growth and provides insight into galaxy evolution and the early universe. This project focuses on identifying AGN using a combination of infrared and optical photometry, leveraging the characteristic signatures AGN exhibit in these wavelength regimes.

---

## Physical Motivation

### Infrared Properties (WISE)

Quasars and other AGN are typically bright in the mid-infrared due to thermal emission from dust in the torus surrounding the SMBH. WISE observes the sky in four mid-infrared bands:

* **W1**: 3.4 μm
* **W2**: 4.6 μm
* **W3**: 12 μm
* **W4**: 22 μm

A common AGN selection technique uses infrared color cuts such as:

* **W1 − W2 > 0.8**
* **W2 − W3 > 2**

Large values of these colors indicate enhanced mid-infrared emission, which is a strong indicator of AGN activity. This project narrows down possibilities of AGN

### Optical Properties (SDSS)

AGN also tend to appear bluer in optical bands due to the high temperatures of their accretion disks. SDSS observes the sky in five optical bands:

* **u** (354 nm, near-UV)
* **g** (477 nm, blue-green)
* **r** (623 nm, red)
* **i** (753 nm, infrared)
* **z** (880 nm, near-infrared)

For this project, the most useful optical colors are:

* **u − g**: measures UV excess
* **g − r**: measures optical blueness

Lower values of these colors correspond to bluer objects, which is typical of quasars and other AGN.

---

## Project Structure

The project consists of two main programs:

### 1. Finding Constraints

This program is used to establish selection criteria for quasars.

* Inputs:

  * A dataset of ~1000 confirmed quasars from SDSS
  * A dataset of ~1000 random galaxies from SDSS
* Output:

  * A color–color diagram (u − g vs. g − r)

The diagram highlights how quasars cluster in color space relative to normal galaxies. Redshift information is included to illustrate how quasar colors evolve with redshift.

These plots are used to define reasonable color boundaries for AGN candidate selection.

---

### 2. Finding Possible AGN Candidates

This program identifies AGN candidates around a specific coordinate.

* Input:

  * Right ascension and declination (degrees)
* Search radius:

  * **500 arcseconds**

All objects within the cone are filtered using the following criteria:

* **Magnitude (z-band)**: ~17 to 21
* **Optical colors**:

  * 0 to 4 in u − g
  * −0.3 to 0.4 in g − r
* **Infrared color**:

  * W1 − W2 > 0.8

The final list of AGN/QSO candidates is written to an output text file.

---

## Outputs

### Optical Color–Color Diagram

Displays u − g vs. g − r for all objects in the cone:

* **Green points**: objects that satisfy the AGN selection criteria
* **Red points**: all other stars and galaxies

### Candidate Output File

A text file containing the coordinates (RA, Dec) of all objects that satisfy both the optical and infrared AGN criteria.

### Sky Map

A Cartesian sky map showing the spatial distribution of all objects within the cone. Different colors indicate which selection criteria were satisfied by each object.


---

## Applications and Extensions

* Identification of AGN candidates in arbitrary sky regions
* Cross-matching AGN candidates with spectroscopic catalogs
* Studying AGN environments and clustering
* Refining selection cuts using machine learning or additional photometric bands

---

## Data Sources

* **Sloan Digital Sky Survey (SDSS)** – Optical photometry
* **WISE (Wide-field Infrared Survey Explorer)** – Mid-infrared photometry

---

## Author

Physics student project focused on AGN identification using multiwavelength survey data.

