#!/usr/bin/env python
# coding: utf-8

# In[79]:


"""Solve standard RBA problem."""
# python 2/3 compatibility
from __future__ import division, print_function

# package imports
import rba
import re
import copy
import numpy as np
import pandas as pd
import sys


# In[80]:


def set_flux_boundary(model, reaction, value):
    
    # construct target from input reaction ID and flux boundary
    boundary_id = reaction + '_flux_boundary'
    new_target = rba.xml.targets.TargetReaction(reaction)
    new_target.value = boundary_id
    
    # add target to model
    mp = model.targets.target_groups.get_by_id('metabolite_production')
    if reaction not in [i.reaction for i in mp.reaction_fluxes]:
        mp.reaction_fluxes.append(new_target)
        
        # add a new parameter with the actual value to model
        model.parameters.functions.append(
            rba.xml.Function(boundary_id, 'constant', {'CONSTANT': value})
        )
    else:
        # or update existing parameter
        fn = model.parameters.functions.get_by_id(boundary_id)
        fn.parameters.get_by_id('CONSTANT').value = value


# In[81]:


def report_results(
    result, output_dir, output_suffix,
    substrate_TR = None, substrate_MW = None):
    
    # calculate yield
    # flux in mmol g_bm^-1 h^-1 needs to be converted to g substrate
    # using transporter TR and molecular weight MW
    if substrate_TR:
        yield_subs = result.mu_opt / (result.reaction_fluxes()[substrate_TR] * substrate_MW)
    
    # calculate compartment occupancy ('density status')
    ds_mem = result.density_status("Cell_membrane")
    ds_cyt = result.density_status("Cytoplasm")
    
    # export summary fluxes per reaction
    result.write_fluxes(
        output_dir + 'fluxes' + output_suffix,
        file_type = 'csv',
        remove_prefix = True)
    
    # optionally re-export fluxes to comma separated values as well
    fluxes = pd.read_csv(output_dir + 'fluxes' + output_suffix, 
        sep = '\t', 
        index_col = 0, 
        header = None)
    fluxes.to_csv(output_dir + 'fluxes' + re.sub('tsv', 'csv', output_suffix))
    
    # export enzyme concentrations
    result.write_proteins(
        output_dir + 'proteins' + output_suffix,
        file_type = 'csv')
    
    # export growth rate, yield, and process machinery concentrations
    ma = result.process_machinery_concentrations()
    ma['P_ENZ'] = sum(result.enzyme_concentrations().values())
    ma['mu'] = result.mu_opt
    if substrate_TR:
        ma['yield'] = yield_subs
        ma['qS'] = result.reaction_fluxes()[substrate_TR]
    with open(output_dir + 'macroprocesses' + output_suffix, 'w') as fout:
        fout.write('\n'.join(['{}\t{}'.format(k, v) for k, v in ma.items()]))
    
    # print µ_max and yield to terminal
    print('\n----- SUMMARY -----\n')
    print('Optimal growth rate is {}.'.format(result.mu_opt))
    #print('Yield on substrate is {}.'.format(yield_subs))
    print('Cell membrane occupancy is {} %.'.format(round(100*ds_mem[1]/ds_mem[0], 3)))
    print('Cytoplasm occupancy is {} %.'.format(round(100*ds_cyt[1]/ds_cyt[0], 3)))
    print('\n----- BOUNDARY FLUXES -----\n')
    for r in result.sorted_boundary_fluxes():
        print(r)


# In[82]:


xml_dir = sys.argv[1] 
output_dir = 'test'
model = rba.RbaModel.from_xml(xml_dir)


# In[83]:


#change medium
model.medium["M_fru"]=0
model.medium["M_c160"]=10


# In[84]:


#set flux constraints
#set_flux_boundary(model, 'R_ETOHt2r', 0.0)
#set_flux_boundary(model, 'R_ACt2r', 0.0)
#set_flux_boundary(model, 'R_CITt', 0)

#set_flux_boundary(model, 'R_EX_c160_e', 1.0)
set_flux_boundary(model, 'R_FAMC160', 1.0)
#set_flux_boundary(model, 'R_ICDHx', 0.0)
#R_EX_o2_e O2

cbb=sys.argv[2]
set_flux_boundary(model, 'R_RBPC', float(cbb) )
set_flux_boundary(model, 'R_RBPC_duplicate_2', float(0) )
#set_flux_boundary(model, 'R_SUCCt2_2', 0.0)
#set_flux_boundary(model, 'R_SUCCt_3', 0.0)
#set_flux_boundary(model, 'R_SUCCtr', 0.0)
#set_flux_boundary(model, 'R_GLUDy', 0.0)


#knockdown= ["ALRTa","G3PD2","TRSARr","3HBCD","ALCD19","AACOAR","THRA","THRD","MGSA","MDH2","POX","AACOAR","FORTF"]
#for k in knockdown:
#    kill="R_" + k;
#    set_flux_boundary(model, kill, float(0))

#set_flux_boundary(model, 'R_NADHNADPH', float(0) )
#O2=sys.argv[3]
#set_flux_boundary(model, 'R_O2t', float(O2) )
# In[87]:

#output_dir= sys.argv[3] 

try:
    result = model.solve(lp_solver="cplex")
            # report results; for yield calculation supply transport
            # reaction and MW of substrate
    report_results(result,
            output_dir = output_dir,
            output_suffix = "oil"
    )
    a=result.reaction_fluxes()
    b=result.reactions
    for i in b.keys():
        print(i,a[i],b[i],sep="\t")
    print("biomass","\t",result.mu_opt,end="\t")
    print(a["R_RBPC"],end="\t")
    print(a["R_HDCAt2"],end="\t")
    print(a["R_O2t"])
    #result.write_fluxes(sys.argv[3])
except TypeError:
            print('model not solvable due to matrix inconsistency')


