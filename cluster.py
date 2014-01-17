import argparse
import os
import sys
import ewave
import h5py
from birdwerdz.dtw import find_matches
from scipy.cluster.vq import kmeans
import numpy as np


def main():
        p = argparse.ArgumentParser(prog="classify", 
                               description="""Finds potential instances of given motif and clusters them into groups for further analysis.""")
        p.add_argument("file", help="""Either an arf(hdf5) file containing motif matches generated by classify.py""",nargs='+')
        p.add_argument("-c", "--clusters", help="""Number of clusters to use""", default = 10, type = int)

        options = p.parse_args()


        with h5py.File(options.file, 'r+') as arf:

            n_motifs=sum(e['motifs'].shape[0] for e in arf.values() 
                         if isinstance(e,h5py.Group) and 'motifs' in e.keys())

            amp_vectors = np.zeros((n_motifs, spec_shape[1]))
            k=0
            for entry in arf.values():
                if not isinstance(entry,h5py.Group) or 'motifs' not in entry.keys(): continue
                for m in entry['motifs']:
                    amp_vectors[k,:] = m['spectrograms'].sum(0)
                    k+=1

            nclusters=10

            centroids,_ = kmeans(amp_vectors, options.clusters)
            arf.create_dataset('centroids', data = centroids)


if __name__=='__main__':
    main()
