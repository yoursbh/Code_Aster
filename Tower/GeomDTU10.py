# -*- coding: latin-1 -*-
# Générer la géométrie pour un modèle RDM
# DTU 10MW Reference Wind Turbine

# Auteur: Hao BAI
# Date de création: 18/04/2018

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
import math


#------------------------------------------------------------------------
#                              	   GEOMETRIE
#------------------------------------------------------------------------
# Repère globale
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)

# ======================== POINTS ========================
TowerHt  = 115.63 # Height of tower above ground level [onshore] or MSL [offshore] (meters)
# HtFract = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
# Elevation = [i * TowerHt for i in HtFract]
Elevation = [0.00, 11.500, 11.501, 23.000, 23.001, 34.500, 34.501, 46.000, 46.001, 57.500,
             57.501, 69.000, 69.001, 80.500, 80.501, 92.000, 92.001, 103.500, 103.501,
             115.630]

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

Groupe_TwrRoot = geompy.CreateGroup(tower, geompy.ShapeType["VERTEX"])
geompy.UnionIDs(Groupe_TwrRoot, [vertexIDs[0]])
geompy.addToStudyInFather(tower, Groupe_TwrRoot, 'Groupe_TwrRoot')

Groupe_TwrTip = geompy.CreateGroup(tower, geompy.ShapeType["VERTEX"])
geompy.UnionIDs(Groupe_TwrTip, [vertexIDs[-1]])
geompy.addToStudyInFather(tower, Groupe_TwrTip, 'Groupe_TwrTip')
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
# |- Local length
hyp_1D_LL = smesh.CreateHypothesis('LocalLength')
hyp_1D_LL.SetLength(1.0) 
hyp_1D_LL.SetPrecision(1e-7)
smesh.SetName(hyp_1D_LL, 'Local Length_1')
# |- Number of segments
hyp_1D_NS = smesh.CreateHypothesis('NumberOfSegments')
hyp_1D_NS.SetNumberOfSegments(1)
smesh.SetName(hyp_1D_NS, 'Nb. Segments_1')


# ======================== ATTRIBUTION ========================
# Définir le maillage
maillage1 = smesh.Mesh(tower)
maillage2 = smesh.Mesh(tower)

# Associer les algoritmes et les hypothèses correspondants
maillage1.AddHypothesis(algo_1D)
maillage1.AddHypothesis(hyp_1D_LL)
maillage2.AddHypothesis(algo_1D)
maillage2.AddHypothesis(hyp_1D_NS)

# ======================== CALCUL ========================
maillage1.Compute()
smesh.SetName(maillage1, 'Maillage_Local_Length')

maillage2.Compute()
smesh.SetName(maillage2, 'Maillage_Number_Of_Segment')

# ======================== GROUPES ========================
# Noeuds
maillage1.GroupOnGeom(Groupe_TwrRoot, 'Groupe_TwrRoot', SMESH.NODE)
maillage1.GroupOnGeom(Groupe_TwrTip, 'Groupe_TwrTip', SMESH.NODE)

# Lignes
maillage1.GroupOnGeom(tower, 'Tower', SMESH.EDGE)
j = 0
for seg in segments:
    j = j + 1
    maillage1.GroupOnGeom(seg, 'Seg_'+str(j), SMESH.EDGE)


# Noeuds
maillage2.GroupOnGeom(Groupe_TwrRoot, 'Groupe_TwrRoot', SMESH.NODE)
maillage2.GroupOnGeom(Groupe_TwrTip, 'Groupe_TwrTip', SMESH.NODE)

# Lignes
maillage2.GroupOnGeom(tower, 'Tower', SMESH.EDGE)
j = 0
for seg in segments:
    j = j + 1
    maillage2.GroupOnGeom(seg, 'Seg_'+str(j), SMESH.EDGE)


# ======================== EXPORTATION ========================
maillage1.ExportMED(r'./Eolien/Code_Aster/Tower/MailDTU10_POU.mmed', False, SMESH.MED_V2_2, 1, 
                   None ,1)
print ('Mesh has been exported to ./Eolien/Code_Aster/Tower/MailDTU10_POU.mmed')
maillage2.ExportMED(r'./Eolien/Code_Aster/Tower/MailDTU10_DIS.mmed', False, SMESH.MED_V2_2, 1, 
                   None ,1)
print ('Mesh has been exported to ./Eolien/Code_Aster/Tower/MailDTU10_DIS.mmed')
