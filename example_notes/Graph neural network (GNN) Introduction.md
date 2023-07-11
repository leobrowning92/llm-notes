- tags: #graph #deeplearning
- source: [from twitter list](https://twitter.com/PetarV_93/status/1306689711029858304) [primary blog](https://towardsdatascience.com/simple-scalable-graph-neural-networks-7eb04f366d07) 
see [[GCN graph convolution layers]]

## Overview

Graph neural networks essentially use weighted [[message passing algorithm]] by multiplying the node features X, the normalised adjacency matrix (or some Linear Diffusion operator) A, and a learned weight matrix W.

So each layer in the simple GCN would be ReLU(AXW).  However, for a deep network that requires the Adjacency matrix stored in memory, which is prohibitive for large networks. Multiple layers allow information to be passed through the network. Additionally initial work used sampling, SGD, and mini batches, but using the nodes in a graph as samples ignores the fact that they are _not independent points from some distribution_. More sophisticated deep networks sample subgraphs or L-hop (L = layer number) graphs to reduce the computational load, and address the dependance of samples.

However, the core focus of the primary blog post was on the SIGN (Scaleable Inception-like Graph Networks), which instead of deep layers, use a shallow layer that computes many different Diffusion operators (actually powers of the norm Adj matrix to represent n-hops). [PyTorch Geometric Implementation Example](https://github.com/rusty1s/pytorch_geometric/blob/master/examples/sign.py) Shows how simple this pre-computation can be, to the extent that you are simply writing a parallel linear and concatenation followed by a MLP. This is key, as it lets you define whatever kind of output feature you want to train on, for example (n,f) for node level, or (1,f) for graph level.

## Thoughts

Im not sure at the moment how that fits for representation learning on graphs, or semi-supervised methods, which I think will be quite important for us.

Out lack of real [[Obtaining ground truth location data]] extends to a lack of ground truth data about a graph that we might like to train.

Also need to look into how transfer learning on graphs works.
