
# BioEmu Colab output:

`samples.xtc` and `topology.pdb`: Trajectory and topology files of all drawn samples.
`cluster_samples.xtc` and `cluster_topology.pdb`: Trajectory and topology files of clustered samples via
                      foldseek using the parameters specified in the notebook.
`foldseek_clusters.json`: Foldseek cluster assignment of all drawn samples
`sequence.fasta`: FASTA file containing the sequence that was sampled
`hpacker-openmm/`
    |- `hpacker-openmm_sidechain_rec.pdb` and `hpacker-openmm_sidechain_rec.xtc`: Contain sidechain
                      reconstructed samples via `hpacker`.
    |- `hpacker-openmm_md_equil.pdb` and `hpacker-openmm_md_equil.xtc`: Contain MD-equilibrated samples
                      after sidechain reconstruction.

For issues, please visit the [`bioemu` GitHub repository](https://github.com/microsoft/bioemu)

