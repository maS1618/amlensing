import numpy as np
import time

#sub packages
from setup import make_plots, Pair_limit
import plot_functions as pf

''' 
list of Filter functions for the combined data of lens and source 
Used in Raw Data
might be improved
'''
ff = []

def broadcast():
	global make_plots, Pair_limit
	from setup import make_plots, Pair_limit

def Filter_sim_pm(rp, limit = Pair_limit['pm_sim_1'],\
	limit_sim = Pair_limit['pm_sim_2']):
	# non similar proper motion
	F_pm_1= (rp['pmRA_x']-rp['pmra'])**2 + (rp['pmDE_x']-rp['pmdec'])**2 \
			> limit_sim**2 * (rp['pmDE_x']**2 + rp['pmRA_x']**2)
	F_pm_2 = rp['pmra']**2 + rp['pmdec']**2 \
		< limit**2 * (rp['pmDE_x']**2 + rp['pmRA_x']**2)
	# Filter is not used for bgs without 5-parameter solution
	F_pm_3 = rp['pmra'].mask 

	#print(rp['pmra'])
	# print(np.sum(rp['pmDE_x'].mask ))
	# print(np.sum(rp['pmDE_x'].mask ))
	# print(np.sum(rp['pmra'].mask ))
	# print(np.sum(rp['pmdec'].mask ))
	# print(limit_sim)

	print('F_pm_1 : ',np.sum(F_pm_1))
	print('F_pm_2 : ',np.sum(F_pm_2))
	print('F_pm_3 : ',np.sum(F_pm_3))
	
	if any(F_pm_3) == False:
		F_pm_3 = (rp['pmra'] == 1e20)
	if make_plots:
		pf.plot_delta_pm_ax1(rp,[(F_pm_1 & F_pm_2)])
	F_pm_1.fill_value = False
	F_pm_1 = F_pm_1.filled()	

	F_pm_2.fill_value = False
	F_pm_2 = F_pm_2.filled()
	return (F_pm_1 & F_pm_2) | F_pm_3

def Filter_sim_pm_DR2(rp, limit = Pair_limit['pm_sim_1'],\
	limit_sim = Pair_limit['pm_sim_2']):
	if "ob_displacement_dec_doubled" not in rp.columns:
		return np.ones(len(rp), dtype = bool)
	# non similar proper motion
	F_pm_1= (rp['pmRA_x']-rp['ob_displacement_ra_doubled'])**2 \
			+ (rp['pmdec']-rp['ob_displacement_dec_doubled'])**2 \
			> limit_sim**2 * (rp['pmdec']**2 + rp['pmRA_x']**2)
	F_pm_2 = rp['ob_displacement_ra_doubled']**2 \
		+ rp['ob_displacement_dec_doubled']**2 \
		< limit**2 * (rp['pmdec']**2 + rp['pmRA_x']**2)
	
	# Filter is not used for bgs with an 5-parameter solution 
	two_parm = (rp['pmra'].mask)
	if any(two_parm) == False:
		two_parm =  (rp['pmra'] == 1e20)
	print(any(F_pm_1[two_parm]))

	if make_plots:
		pf.plot_delta_pm_ax2(rp,two_parm,[(F_pm_1 & F_pm_2) & (two_parm)])
	return (F_pm_1 & F_pm_2) | (two_parm==False)

def Filter_pm_tot_DR2(rp, limit = Pair_limit['pm_tot']):
	# Filter on the absolut dr2 propermotion
	if "ob_displacement_dec_doubled" not in rp.columns:
		return np.ones(len(rp), dtype = bool)
	F_pmdr2_1 = (rp['ob_displacement_ra_doubled']**2 \
		+ rp['ob_displacement_dec_doubled']**2) < limit*limit
	# Filter is not used for bgs with an 5-parameter solution 
	F_pmdr2_2 = (rp['pmRA_x'].mask) | (rp['pmRA_x'] < 1e20)
	return F_pmdr2_1 | (F_pmdr2_2 == False)

def Filter_sim_px(rp, limit = Pair_limit['px']):
	# non similar parallax
	F_px_1 = rp['parallax']  < limit * rp['Plx'] 
	F_px_2 = rp['pmra'].mask 
	if any(F_px_2) == False:
		F_px_2 = (rp['pmra'] == 1e20)
	F_px_1.fill_value = False
	F_px_1=F_px_1.filled()
	if make_plots:
		pf.plot_sim_px(rp,F_px_1)
	return F_px_1 | F_px_2

All_filter = [Filter_sim_pm, Filter_sim_px]
#, Filter_sim_pm_DR2