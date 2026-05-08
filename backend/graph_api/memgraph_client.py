# api/memgraph_client.py
from gqlalchemy import Memgraph
from typing import List, Dict, Optional

class MemgraphClient:
    def __init__(self):
        self.mg = Memgraph(host='localhost', port=7687)
    
    def get_node_with_neighbors(self, node_id: str) -> Optional[dict]:
        """Получить узел со всеми соседями"""
        query = """
        MATCH (n:Word {id: $id})
        OPTIONAL MATCH (n)-[r]-(neighbor:Word)
        RETURN {
            id: n.id,
            neighbors: COLLECT(DISTINCT {
                id: neighbor.id,
                label: TYPE(r)
            })
        } as result
        """
        results = list(self.mg.execute_and_fetch(query, {'id': node_id}))
        if results and results[0].get('result'):
            return results[0]['result']
        return None
    
    def add_node(self, node_id: str) -> bool:
        """Создать узел"""
        query = "CREATE (n:Word {id: $id}) RETURN n"
        self.mg.execute(query, {'id': node_id})
        return True
    
    def add_edge(self, from_id: str, to_id: str, relation: str) -> bool:
        """Создать связь"""
        query = f"""
        MATCH (from:Word {{id: $from_id}})
        MATCH (to:Word {{id: $to_id}})
        CREATE (from)-[:{relation}]->(to)
        RETURN from, to
        """
        self.mg.execute(query, {'from_id': from_id, 'to_id': to_id})
        return True
    
    def delete_node(self, node_id: str) -> bool:
        """Удалить узел"""
        query = "MATCH (n:Word {id: $id}) DETACH DELETE n RETURN count(n) as deleted"
        results = list(self.mg.execute_and_fetch(query, {'id': node_id}))
        return results[0]['deleted'] > 0 if results else False
    
    def delete_edge(self, from_id: str, to_id: str) -> bool:
        """Удалить связь"""
        query = """
        MATCH (from:Word {id: $from_id})-[r]-(to:Word {id: $to_id})
        DELETE r
        RETURN count(r) as deleted
        """
        results = list(self.mg.execute_and_fetch(query, {'from_id': from_id, 'to_id': to_id}))
        return results[0]['deleted'] > 0 if results else False
    
   
    def update_node(self, old_id: str, new_id: str) -> bool:
        """Обновить ID узла"""
        query = "MATCH (n:Word {id: $old_id}) SET n.id = $new_id RETURN n"
        self.mg.execute(query, {'old_id': old_id, 'new_id': new_id})
        return True