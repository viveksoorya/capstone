# code borrowed from MDA_EROS_22Mar25.ipynb and slightly modified for use; credit for mentioned python notebook : Prof Kalyan Chakrabarti
def visualize_mda_universe(u, output_dir='bioemu-samples',
    sel_string='not ((resname WAT) or (resname HOH))', 
    style={"cartoon": {'color': 'spectrum'}}):
  
  """
  Inputs: 
  u : mdanalysis universe
  sel_string : mdanalysis selection string for visible atoms
  style : py3Dmol style
  """

  stride_animation = 1

  import warnings
  warnings.filterwarnings('ignore')
  

  # TODO: do i need to assert that the line has no more than 80 characters?
    # Helper classes to read and get PDB fields
  class Atom(dict):
    def __init__(self, line):
      self["type"] = line[0:6].strip()
      self["idx"] = line[6:11].strip()
      self["name"] = line[12:16].strip()      # TODO : what is this
      self["resname"] = line[17:20].strip()   # TODO: there is something between residue name and residue id what is it, in the file
      self["resid"] = int(int(line[22:26]))
      #print(type(self["resid"]))
      #print(self["resid"])  
      self["x"] = float(line[30:38])
      self["y"] = float(line[38:46])
      self["z"] = float(line[46:54])          
      # there are two thing after x y and z coordinates, and before symbol of atom; 
      # The second one is B-factor or temperature factor (as explained in one of the papers in the literature)
      # The first one is a quantity describing the amount of time spent 
      # in that position described by x y and z; it's called occupancy 
      # # Occupancy comes in handy to note if the molecule is flexible in that region
      self["sym"] = line[76:78].strip()

    def __str__(self):
      line = list(" " * 80)                   # initializes a line with 80 characters
      line[0:6] = self["type"].ljust(6)       
      line[6:11] = self["idx"].ljust(5)
      line[12:16] = self["name"].ljust(4)
      line[17:20] = self["resname"].ljust(3)
      line[22:26] = str(self["resid"]).ljust(4)
      line[30:38] = str(self["x"]).rjust(8)
      line[38:46] = str(self["y"]).rjust(8)
      line[46:54] = str(self["z"]).rjust(8)
      line[76:78] = self["sym"].rjust(2)
      return "".join(line) + "\n"             # returns the line after updating the characters to reflect atom attributes
          
  class Molecule(list):
    def __init__(self, file):                 # collects all lines labelled ATOM
      for line in file:
        if "ATOM  " in line or "HETATM" in line:      # TODO: what is HETATM; heterogeneous atom is an atom in a small molecule
          self.append(Atom(line))
              
      def __str__(self):
        outstr = ""
        for at in self:
          outstr += str(at)
        return outstr


  import os
  if not os.path.exists(output_dir):
      os.makedirs(output_dir)  # create the directory if it does not exist
  write_to_file = os.path.join(output_dir, 'sample_')
  u.trajectory[0]  
  import MDAnalysis as mda
  # Write out frames for animation
  protein = u.select_atoms(sel_string) 
  i = 0
  for ts in u.trajectory[0:len(u.trajectory):int(stride_animation)]:  # TODO: why unused variable ts
      if i > -1:
          with mda.Writer(write_to_file + str(i) + '.pdb', protein.n_atoms) as W:  
              W.write(protein)
      i = i + 1

  # TODO: why write to files at all if all you are going to do with the files is to  put them all in the string models later

  
  # Load frames as molecules (py3Dmol let us visualize a single "molecule" per frame)
  molecules = []
  for i in range(int(len(u.trajectory)/int(stride_animation))):
      with open(write_to_file + str(i) + '.pdb') as ifile:
          molecules.append(Molecule(ifile))
  models = ""
  for i in range(len(molecules)):
    models += "MODEL " + str(i) + "\n"
    for j,atom in enumerate(molecules[i]):  # TODO: shouldn't the variable here be atom instead of mol?
      # i think it should be atom;
      # TODO: figure out a way to get rid of the useless j variable
      models += str(atom)
    models += "ENDMDL\n"


  # Animation
  import py3Dmol
  view = py3Dmol.view(width=800, height=600)
  view.addModelsAsFrames(models)
  for i, at in enumerate(molecules[0]):
      view.setStyle({'model': -1, 'serial': i+1}, at.get("pymol", style))
  view.zoomTo()
  
  view.animate({'loop': "forward", 'reps': 0}) #, 'interval': 1000}) # TODO: explain this line; value as 0 for reps actually stands for infinite
  return view

