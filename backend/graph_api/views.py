# api/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .memgraph_client import MemgraphClient

client = MemgraphClient()

@api_view(['GET'])
def get_node(request, node_id):
    """GET /api/node/k1 - получить узел с соседями"""
    result = client.get_node_with_neighbors(node_id)
    if result and result.get('id'):
        return Response(result)
    return Response({"error": "Node not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def add_node(request):
    """POST /api/node - создать узел
    Body: {"id": "k1"}"""
    node_id = request.data.get('id')
    if node_id:
        client.add_node(node_id)
        return Response({"status": "ok", "id": node_id}, status=status.HTTP_201_CREATED)
    return Response({"error": "No id provided"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def add_edge(request):
    """POST /api/edge - создать связь
    Body: {"from": "k1", "to": "k2", "relation": "гипоним"}"""
    from_id = request.data.get('from')
    to_id = request.data.get('to')
    relation = request.data.get('relation')
    
    if not from_id:
        return Response({"error": "Missing 'from' parameter"}, status=status.HTTP_400_BAD_REQUEST)
    if not to_id:
        return Response({"error": "Missing 'to' parameter"}, status=status.HTTP_400_BAD_REQUEST)
    if not relation:
        return Response({"error": "Missing 'relation' parameter"}, status=status.HTTP_400_BAD_REQUEST)
    
    success = client.add_edge(from_id, to_id, relation)
    if success:
        return Response({"status": "ok", "from": from_id, "to": to_id, "relation": relation})
    return Response({"error": "Failed to create edge"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Добавь эти методы для полноценной работы:

@api_view(['DELETE'])
def delete_node(request, node_id):
    """DELETE /api/node/k1 - удалить узел"""
    success = client.delete_node(node_id)
    if success:
        return Response({"status": "deleted", "id": node_id})
    return Response({"error": "Node not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_edge(request):
    """DELETE /api/edge - удалить связь
    Body: {"from": "k1", "to": "k2"}"""
    from_id = request.data.get('from')
    to_id = request.data.get('to')
    
    if not from_id or not to_id:
        return Response({"error": "Missing 'from' or 'to' parameters"}, status=status.HTTP_400_BAD_REQUEST)
    
    success = client.delete_edge(from_id, to_id)
    if success:
        return Response({"status": "deleted", "from": from_id, "to": to_id})
    return Response({"error": "Edge not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_all_nodes(request):
    """GET /api/nodes - получить все узлы"""
    nodes = client.get_all_nodes()
    return Response({"nodes": nodes})

@api_view(['PUT'])
def update_node(request, node_id):
    """PUT /api/node/k1 - обновить узел
    Body: {"new_id": "k1_new"}"""
    new_id = request.data.get('new_id')
    if new_id:
        success = client.update_node(node_id, new_id)
        if success:
            return Response({"status": "updated", "old_id": node_id, "new_id": new_id})
        return Response({"error": "Node not found"}, status=status.HTTP_404_NOT_FOUND)
    return Response({"error": "Missing 'new_id' parameter"}, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
def init_mock_data(request):
    """POST /api/init-mock/ - загрузить мок-данные в Memgraph"""
    
    # Твои мок-данные
    mock_data = {
        "k1": {"id": "k1", "neighbors": [{"id": "k2", "label": "гипоним"}, {"id": "k3", "label": "синоним"}, {"id": "k4", "label": "антоним"}, {"id": "k15", "label": "мероним"}, {"id": "k16", "label": "голоним"}]},
        "k2": {"id": "k2", "neighbors": [{"id": "k5", "label": "пример"}, {"id": "k6", "label": "часть"}, {"id": "k1", "label": "гипероним"}]},
        "k3": {"id": "k3", "neighbors": [{"id": "k7", "label": "родственный"}, {"id": "k8", "label": "ассоциация"}, {"id": "k1", "label": "синоним"}]},
        "k4": {"id": "k4", "neighbors": [{"id": "k9", "label": "противоположность"}, {"id": "k1", "label": "антоним"}]},
        "k5": {"id": "k5", "neighbors": [{"id": "k10", "label": "конкретизация"}, {"id": "k11", "label": "иллюстрация"}, {"id": "k17", "label": "типичный_случай"}]},
        "k6": {"id": "k6", "neighbors": [{"id": "k2", "label": "целое"}, {"id": "k18", "label": "компонент"}]},
        "k7": {"id": "k7", "neighbors": [{"id": "k12", "label": "коллокация"}, {"id": "k19", "label": "идиома"}]},
        "k8": {"id": "k8", "neighbors": [{"id": "k20", "label": "контекст"}]},
        "k9": {"id": "k9", "neighbors": []},
        "k10": {"id": "k10", "neighbors": [{"id": "k21", "label": "специализация"}, {"id": "k22", "label": "уточнение"}]},
        "k11": {"id": "k11", "neighbors": [{"id": "k23", "label": "метафора"}]},
        "k12": {"id": "k12", "neighbors": [{"id": "k24", "label": "фразеологизм"}, {"id": "k25", "label": "пословица"}]},
        "k13": {"id": "k13", "neighbors": [{"id": "k26", "label": "термин"}, {"id": "k27", "label": "неологизм"}]},
        "k14": {"id": "k14", "neighbors": [{"id": "k28", "label": "архаизм"}, {"id": "k29", "label": "историзм"}]},
        "k15": {"id": "k15", "neighbors": [{"id": "k30", "label": "элемент"}, {"id": "k1", "label": "холоним"}]},
        "k16": {"id": "k16", "neighbors": [{"id": "k1", "label": "мероним"}]},
        "k17": {"id": "k17", "neighbors": []},
        "k18": {"id": "k18", "neighbors": []},
        "k19": {"id": "k19", "neighbors": []},
        "k20": {"id": "k20", "neighbors": []},
        "k21": {"id": "k21", "neighbors": []},
        "k22": {"id": "k22", "neighbors": []},
        "k23": {"id": "k23", "neighbors": []},
        "k24": {"id": "k24", "neighbors": []},
        "k25": {"id": "k25", "neighbors": []},
        "k26": {"id": "k26", "neighbors": []},
        "k27": {"id": "k27", "neighbors": []},
        "k28": {"id": "k28", "neighbors": []},
        "k29": {"id": "k29", "neighbors": []},
        "k30": {"id": "k30", "neighbors": []},
    }
    
    try:
        # 1. Очищаем БД
        client.mg.execute("MATCH (n) DETACH DELETE n")
        
        # 2. Создаем все узлы
        for node_id in mock_data.keys():
            client.mg.execute("CREATE (n:Word {id: $id})", {'id': node_id})
        
        # 3. Создаем все связи
        for node_id, node_info in mock_data.items():
            for neighbor in node_info['neighbors']:
                query = f"""
                MATCH (from:Word {{id: $from_id}})
                MATCH (to:Word {{id: $to_id}})
                CREATE (from)-[:{neighbor['label']}]->(to)
                """
                client.mg.execute(query, {
                    'from_id': node_id,
                    'to_id': neighbor['id']
                })
        
        # 4. Проверяем результат
        result = list(client.mg.execute_and_fetch("MATCH (n:Word) RETURN count(n) as count"))[0]
        
        return Response({
            "status": "success",
            "message": "Mock data loaded successfully",
            "nodes_created": result['count']
        })
        
    except Exception as e:
        return Response({
            "status": "error",
            "message": str(e)
        }, status=500)