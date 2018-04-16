# -*- coding: latin-1 -*-
# Create a list of nodes to present the tower
# Nous prenons la géométrie décrite dans "Definition of a 5-MW Reference Wind Turbine for
# Offshore System Development"

# Auteur: Hao BAI
# Date de création: 15/04/2018

import sys, os
cwd = os.getcwd()

import salome # Initialisation SALOME
salome.salome_init()

import GEOM # Interface Python de module GEOM
from salome.geom import geomBuilder
geompy = geomBuilder.New(salome.myStudy)
gg = salome.ImportComponentGUI("GEOM")

import SMESH, SALOMEDS # Interface Python de module MESH
from salome.smesh import smeshBuilder
smesh = smeshBuilder.New(salome.myStudy)
from salome.StdMeshers import StdMeshersBuilder

from math import sin, cos, radians
#------------------------------------------------------------------------
#                              	   GEOMETRIE
#------------------------------------------------------------------------
# Repère globale
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)

# ======================== POINTS ========================
TowerHt  = 87.6 # Height of tower above ground level [onshore] or MSL [offshore] (meters)
HtFract = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
Elevation = [i * TowerHt for i in HtFract]
# Elevation = [0.00, 8.76, 17.52, 26.28, 35.04, 43.80, 52.56, 61.32, 70.08, 78.84, 87.60]

# ======================== POINTS ========================
# Tower
list_tower = []
for elem in Elevation:
    node = geompy.MakeVertex(0., 0., elem)
    list_tower.append(node)


# ======================== LIGNES ========================
# +++ Tower
tower = geompy.MakePolyline(list_tower, False) # Créer une liger fermée si 'True'
id_tower = geompy.addToStudy(tower, "Tower")
# gg.createAndDisplayGO(id_tower)


# ======================== GROUPES ========================
# +++ tower
# |-- Groupe des noeuds
vertexIDs = geompy.SubShapeAllIDs(tower, geompy.ShapeType["VERTEX"])

nodes = []
i = 0
for vertexid in vertexIDs:
    temp = geompy.CreateGroup(tower, geompy.ShapeType["VERTEX"])
    nodes.append(temp)
    geompy.UnionIDs(temp, [vertexid])
    geompy.addToStudyInFather(tower, temp, 'Node_'+str(i))
    i = i + 1
# |-- Groupe des arrêtes
edgeIDs = geompy.SubShapeAllIDs(tower, geompy.ShapeType["EDGE"])

segments = []
i = 0
for edgeid in edgeIDs:
    i = i + 1
    temp = geompy.CreateGroup(tower, geompy.ShapeType["EDGE"])
    segments.append(temp)
    geompy.UnionIDs(temp, [edgeid])
    geompy.addToStudyInFather(tower, temp, 'Seg_'+str(i))


#------------------------------------------------------------------------
#                              	    MAILLAGE
#------------------------------------------------------------------------
# ======================== CONFIGURATION ========================
# Algorithme 1D
algo_1D = smesh.CreateHypothesis('Regular_1D')
smesh.SetName(algo_1D, 'Algorithme 1D_Wire Discretisation')

# Hypothèse 1D
hyp_1D = smesh.CreateHypothesis('LocalLength')
hyp_1D.SetLength(1.0) 
hyp_1D.SetPrecision(1e-7)
smesh.SetName(hyp_1D, 'Local Length_1')

# ======================== ATTRIBUTION ========================
# Définir le maillage
maillage = smesh.Mesh(tower)

# Associer les algoritmes et les hypothèses correspondants
maillage.AddHypothesis(algo_1D)
maillage.AddHypothesis(hyp_1D)

# ======================== CALCUL ========================
maillage.Compute()
smesh.SetName(maillage, 'Maillage')

# ======================== GROUPES ========================
# Noeuds
j = 0
for node in nodes:
    maillage.GroupOnGeom(node, 'Node_'+str(j), SMESH.NODE)
    j = j + 1

# Lignes
maillage.GroupOnGeom(tower, 'Tower', SMESH.EDGE)
j = 0
for seg in segments:
    j = j + 1
    maillage.GroupOnGeom(seg, 'Seg_'+str(j), SMESH.EDGE)


# ======================== EXPORTATION ========================
maillage.ExportMED(r'./Eolien/Code_Aster/Tower/Maillage2.mmed', False, SMESH.MED_V2_2, 1, 
                   None ,1)
print ('Mesh has been exported to ./Eolien/Code_Aster/Tower/Maillage2.mmed')
