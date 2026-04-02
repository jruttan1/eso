import networkx as nx
from crud import get_all_edges
from sqlmodel import Session
from db import engine, Cluster, NoteCluster


def create_graph():
    G = nx.Graph()
    with Session(engine) as session:
        edges =  get_all_edges(session)

        for edge in edges: # build graph
            similarity = 1 - edge.distance # we were using cosine distance where lower = more connected but Louvain reads it the other way so invert to get cosine similarity (inverse of cosine distance)
            G.add_edge(edge.from_note_id, edge.to_note_id, similarity = similarity)
        
        clusters = nx.louvain_communities(G, weight = 'similarity',  resolution=1) # resolution: less than 1 = larger communities, greater than 1 = smaller communities

        for group in clusters: # group here is a group of similar ids that makeup a cluster respresented as a set
            cluster = Cluster() 
            session.add(cluster)
            session.commit()
            session.refresh(cluster)


            for j in group: # loop through each id in hte cluster
                cluster_record = NoteCluster(note_id = j, cluster_id = cluster.id)
                session.add(cluster_record)
                session.commit()
