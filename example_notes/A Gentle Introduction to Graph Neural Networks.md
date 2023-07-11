- tags: #graph #deeplearning

from [[distil - pub]].

An excellent resource for a technically skilled, but not necessarily knowledgeable, practitioner. This assumes some understanding of deep learning more broadly, and a cursory understanding of graphs, but quickly ramps up to an overview suitable for an ML practitioner.

and relates to [[Graph neural network (GNN) Introduction]] which tends to focus on the GCN layers specifically and sampling from a graph, which is also discussed here.

They emphasise how a [[message passing algorithm]] is used to pass embeddings via the connectivity of the graph to give nodes and edges near it, k-hops away, where the number of layers is the number of hops. these messages are then aggregated together, and then passed through a learned update function to update the node or edge.

message passing can occur from edges to edges via node connections and nodes to nodes via edge connections.

There can also be a learned linear mapping from nodes to edges, where you want that information to flow from node to edge or edge to node. This is especially important if your dataset includes node information, and you want to predict on edges or vise versa.

A cool insight is to have a master node which is connected to all nodes and allows passing of global context.

They also stress that much of the work is in structuring the graphs sensibly, for example multi-partite graphs with different structures between different node or edge types, or nested graphs.

