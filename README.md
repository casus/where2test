# where2test
EUvsVirus project repository

# Status

1. Can read a GeoJSON file *(Currently testing with the geojson file provided here : https://npgeo-corona-npgeo-de.hub.arcgis.com/datasets/917fc37a709542548cc3be077a786c17_0)*

2. Runs an optimizer *(Need to correctly define the objective function and constraints)*

3. Output a GeoJSON file with the optimized quantity as an attribute *(Overwrites all other properties, only one of the available solutions is printed out)*

# Usage 

`python test.py <inputfile> <outputfile>`

# Dependencies

* PyGeoj 1.0.0 (https://pypi.org/project/PyGeoj/)
* PyGMO 2 (https://github.com/esa/pygmo2)

