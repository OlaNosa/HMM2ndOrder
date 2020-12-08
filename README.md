# HMM2ndOrder
- can use python2 for all of the code (must use python2 to run pyhmm)

## ctfiles: 
- processed_data directory has individual ct files with the sequence of nucleotides and its corresponding pair or unpair (labeled as 1 or 0 respectivley)
- To generate and view the transition matrix run 2ordertransitionprob.py: the result (probmat.npy) contains a 4X4 matrix for transitions between hidden states (UU, UP, PU, PP).
- To generate and view the emission matrix run 2orderemissionprob.py: the result (emprobmat.npy) contains a 4X16 matrix of hiddens states (UU, UP, PU, PP) by (all possible pairs of nucleotides starting with AA, etc. where A = 0, C = 1, G = 2, U = 3)
  - emission probability represents P(pair of nucleotides | pair of hidden states)
## pyhmm: (use python2)
- To generate second order HMM run mytest_pyhmm2order
  - used same code as for the first order model but changed input sequence to take in pairs of nucleotides in strides of 2
