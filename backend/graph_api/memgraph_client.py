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
            rus_word: n.rus_word,
            eng_word: n.eng_word,
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
    
    def add_node(self, node_id: str, rus_word: str = "", eng_word: str = "") -> bool:
        """Создать узел с русским и английским словом"""
        query = """
        CREATE (n:Word {id: $id, rus_word: $rus_word, eng_word: $eng_word})
        RETURN n
        """
        self.mg.execute(query, {'id': node_id, 'rus_word': rus_word, 'eng_word': eng_word})
        return True
    
    def get_all_nodes(self) -> List[dict]:
        """Получить все узлы"""
        query = """
        MATCH (n:Word) 
        RETURN {
            id: n.id, 
            rus_word: n.rus_word, 
            eng_word: n.eng_word
        } as node
        """
        results = list(self.mg.execute_and_fetch(query))
        return [r['node'] for r in results if r['node']]
    
    def update_node(self, old_id: str, new_id: str = None, new_rus_word: str = None, new_eng_word: str = None) -> bool:
        """Обновить ID и/или слова узла"""
        updates = []
        params = {'old_id': old_id}
        
        if new_id:
            updates.append("n.id = $new_id")
            params['new_id'] = new_id
        if new_rus_word:
            updates.append("n.rus_word = $new_rus_word")
            params['new_rus_word'] = new_rus_word
        if new_eng_word:
            updates.append("n.eng_word = $new_eng_word")
            params['new_eng_word'] = new_eng_word
        
        if not updates:
            return True
        
        query = f"""
        MATCH (n:Word {{id: $old_id}})
        SET {', '.join(updates)}
        RETURN n
        """
        self.mg.execute(query, params)
        return True
    
    def delete_node(self, node_id: str) -> bool:
        """Удалить узел"""
        query = "MATCH (n:Word {id: $id}) DETACH DELETE n RETURN count(n) as deleted"
        results = list(self.mg.execute_and_fetch(query, {'id': node_id}))
        return results[0]['deleted'] > 0 if results else False
    
    
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
    
    def delete_edge(self, from_id: str, to_id: str, relation: str = None) -> bool:
        """Удалить связь"""
        type_filter = f":{relation}" if relation else ""
        query = f"""
        MATCH (from:Word {{id: $from_id}})-[r{type_filter}]->(to:Word {{id: $to_id}})
        DELETE r
        RETURN count(r) as deleted
        """
        results = list(self.mg.execute(query, {'from_id': from_id, 'to_id': to_id}))
        return True
    
    def init_mock_data(self, mock_data: dict):
        """Загрузить тестовые данные"""
        self.mg.execute("MATCH (n) DETACH DELETE n")
        
        for node_id, node_info in mock_data.items():
            rus = node_info.get('rus_word', '')
            eng = node_info.get('eng_word', '')
            self.mg.execute(
                "CREATE (n:Word {id: $id, rus_word: $rus, eng_word: $eng})",
                {'id': node_id, 'rus': rus, 'eng': eng}
            )
        
        for node_id, node_info in mock_data.items():
            for neighbor in node_info.get('neighbors', []):
                query = f"""
                MATCH (from:Word {{id: $from_id}})
                MATCH (to:Word {{id: $to_id}})
                CREATE (from)-[:{neighbor['label']}]->(to)
                """
                self.mg.execute(query, {
                    'from_id': node_id,
                    'to_id': neighbor['id']
                })
        
        return True