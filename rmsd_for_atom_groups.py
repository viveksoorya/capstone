# code borrowed from MDA_EROS_22Mar25.ipynb; credit for mentioned python notebook : Prof Kalyan Chakrabarti

import numpy as np
import pandas as pd
from MDAnalysis.analysis import rms

def rmsd_for_atomgroups(universe, selection1, selection2=None):
    """Calulate the RMSD for selected atom groups.

    Parameters
    ----------
    universe: MDAnalysis.core.universe.Universe
        MDAnalysis universe.
    selection1: str
        Selection string for main atom group, also used during alignment.
    selection2: list of str, optional
        Selection strings for additional atom groups.

    Returns
    -------
    rmsd_df: pandas.core.frame.DataFrame
        DataFrame containing RMSD of the selected atom groups over time.
    """
    print(len(universe.trajectory))
    universe.trajectory[0]   # what is this line doing? seems to seek to the 0th frame such that universe is in that frame; 
    # why would this happen in this function that returns rmsd of given atomgroups
    ref = universe
    rmsd_analysis = rms.RMSD(universe, ref, select=selection1, groupselections=selection2)
    rmsd_analysis.run()     # why is there a run method here? it wouldn't surprise me if it not for the method in the previous line
    columns = [selection1, *selection2] if selection2 else [selection1]
    rmsd_df = pd.DataFrame(np.round(rmsd_analysis.rmsd[:, 2:], 2), columns=columns)
    rmsd_df.index.name = "frame"
    return rmsd_df
