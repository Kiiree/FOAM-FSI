#!/usr/bin/env python

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Figure dimensions
fig_width_pt = 0.5 * 345.0
inches_per_pt = 1.0/72.27
fig_width = fig_width_pt*inches_per_pt
fig_height = fig_width * 0.86
fig_size = [fig_width,fig_height]
nb_ticks = 7
params = {
    'font.size' : 7,
    'axes.labelsize' : 7,
    'font.size' : 7,
    'legend.fontsize': 7,
    'xtick.labelsize' : 7,
    'ytick.labelsize' : 7,
    'figure.figsize': fig_size
}

plt.rcParams.update(params)

markers = ["-ob", "-vg", "-<r", "-^c", "->m", "-sy", "-*k", "--ob", "--vg", "--<r", "--^c", "-->m", "--sy", "--*k", "-.db", "-ob", "-vg", "-<r", "-^c", "->m", "-sy"]
markerIndex = 0

nbComputations = 6
nbNodes = 6

timeIntegrationSchemes = ["IDC", "SDIRK"]

sdirkSchemes = ["SDIRK2", "SDIRK3", "SDIRK4", "ESDIRK3", "ESDIRK4", "ESDIRK5", "ESDIRK53PR", "ESDIRK63PR", "ESDIRK74PR"]

label_ref = "IDC_nbNodes_" + str( nbNodes )
label_ref += "_nbTimeSteps_" + str( 2 ** (nbComputations-1) )

data_u_ref = np.loadtxt( "data/" + label_ref + "_data_u.log" )
data_a_ref = np.loadtxt( "data/" + label_ref + "_data_a.log" )

velocityFig = plt.figure()
velocityPlot = velocityFig.add_subplot(111)
areaFig = plt.figure()
areaPlot = areaFig.add_subplot(111)

for timeIntegrationScheme in timeIntegrationSchemes:

    nbSchemes = nbNodes
    if timeIntegrationScheme == "SDIRK":
        nbSchemes = len( sdirkSchemes )

    for iNodes in np.arange( nbSchemes ):

        timeStepList = []
        errors_u = []
        errors_a = []

        for iComputation in np.arange( nbComputations ):

            nbNodes = iNodes + 1
            nbTimeSteps = 2 ** iComputation

            label = timeIntegrationScheme

            if timeIntegrationScheme == "SDIRK":
                label += "_" + sdirkSchemes[iNodes]

            if timeIntegrationScheme == "IDC":
                label += "_nbNodes_" + str( nbNodes )

            label += "_nbTimeSteps_" + str( nbTimeSteps )

            try:
                data_u = np.loadtxt( "data/" + label + "_data_u.log" )
                data_a = np.loadtxt( "data/" + label + "_data_a.log" )
            except:
                continue

            error_u = np.linalg.norm(data_u - data_u_ref) / np.linalg.norm( data_u_ref )
            error_a = np.linalg.norm(data_a - data_a_ref) / np.linalg.norm( data_a_ref )

            errors_u.append( error_u )
            errors_a.append( error_a )
            timeStepList.append( 1.0 / float( nbTimeSteps ) )

        if timeIntegrationScheme == "SDIRK":
            legend = sdirkSchemes[iNodes]
        if timeIntegrationScheme == "IDC":
            legend = 'IDC' + str(nbNodes)

        velocityPlot.loglog( timeStepList, errors_u, markers[markerIndex], label = legend, markersize = 3 )
        areaPlot.loglog( timeStepList, errors_a, markers[markerIndex], label = legend, markersize = 3 )

        markerIndex += 1

        try:
            print '\n' + legend
            for i in np.arange( nbComputations - 1 ):
                print ( np.log10( errors_u[i+1] ) - np.log10( errors_u[i] ) ) / ( np.log10( timeStepList[i+1] ) - np.log10( timeStepList[i] ) )

            print ''
            for i in np.arange( nbComputations - 1 ):
                print ( np.log10( errors_a[i+1] ) - np.log10( errors_a[i] ) ) / ( np.log10( timeStepList[i+1] ) - np.log10( timeStepList[i] ) )
        except:
            pass

velocityPlot.set_xlabel( 'Time step [s]' )
velocityPlot.set_ylabel( 'Error in velocity [-]' )
velocityPlot.grid( 'on' )
lgd = velocityPlot.legend( loc='upper center', bbox_to_anchor=(0.4, 1.55), ncol = 3, fancybox = True, shadow = False )
velocityFig.savefig( 'tubeflow_velocity.pdf', bbox_extra_artists=(lgd,), transparent = True, bbox_inches='tight' )

areaPlot.set_xlabel( 'Time step [s]' )
areaPlot.set_ylabel( 'Error in area [-]' )
areaPlot.grid( 'on' )
lgd = areaPlot.legend( loc='upper center', bbox_to_anchor=(0.4, 1.55), ncol = 3, fancybox = True, shadow = False )
areaFig.savefig( 'tubeflow_area.pdf', bbox_extra_artists=(lgd,), transparent = True, bbox_inches='tight' )
