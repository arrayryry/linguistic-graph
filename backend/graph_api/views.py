from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .memgraph_client import MemgraphClient
from .serializers import (
    NodeSerializer, 
    CreateEdgeSerializer, 
    UpdateNodeSerializer
)

client = MemgraphClient()

@api_view(['GET'])
def get_node(request, node_id):
    """GET /api/node/k1 - получить узел с соседями"""
    result = client.get_node_with_neighbors(node_id)
    if result and result.get('id'):
        return Response(result)
    return Response({"error": "Node not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_all_nodes(request):
    """GET /api/nodes - получить все узлы"""
    nodes = client.get_all_nodes()
    return Response({"nodes": nodes})

@api_view(['POST'])
def add_node(request):
    """POST /api/node - создать узел
    Body: {"id": "k1", "rus_word": "слово", "eng_word": "word"}"""
    serializer = NodeSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data
    client.add_node(
        node_id=data['id'],
        rus_word=data.get('rus_word', ''),
        eng_word=data.get('eng_word', '')
    )
    return Response({"status": "ok", "id": data['id']}, status=status.HTTP_201_CREATED)

@api_view(['PUT'])
def update_node(request, node_id):
    """PUT /api/node/k1/update - обновить узел
    Body: {"new_id": "new_id", "new_rus_word": "новое", "new_eng_word": "new"}"""
    serializer = UpdateNodeSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data
    success = client.update_node(
        old_id=node_id,
        new_id=data.get('new_id'),
        new_rus_word=data.get('new_rus_word'),
        new_eng_word=data.get('new_eng_word')
    )
    if success:
        return Response({"status": "updated"})
    return Response({"error": "Node not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_node(request, node_id):
    """DELETE /api/node/k1/delete - удалить узел"""
    success = client.delete_node(node_id)
    if success:
        return Response({"status": "deleted", "id": node_id})
    return Response({"error": "Node not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def add_edge(request):
    """POST /api/edge - создать связь
    Body: {"from": "k1", "to": "k2", "relation": "гипоним"}"""
    serializer = CreateEdgeSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data
    success = client.add_edge(data['from_id'], data['to_id'], data['rel_type'])
    if success:
        return Response({"status": "ok"})
    return Response({"error": "Failed to create edge"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def delete_edge(request):
    """DELETE /api/edge/delete - удалить связь
    Body: {"from": "k1", "to": "k2"}"""
    from_id = request.data.get('from')
    to_id = request.data.get('to')
    relation = request.data.get('relation')
    
    if not from_id or not to_id:
        return Response({"error": "Missing 'from' or 'to'"}, status=status.HTTP_400_BAD_REQUEST)
    
    success = client.delete_edge(from_id, to_id, relation)
    if success:
        return Response({"status": "deleted"})
    return Response({"error": "Edge not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def init_mock_data(request):
    """POST /api/init-mock/ - загрузить тестовые данные"""
    mock_data = {
    "k1": {"id": "k1", "rus_word": "радость", "eng_word": "joy", "neighbors": [{"id": "k2", "label": "синоним"}, {"id": "k3", "label": "антоним"}, {"id": "k4", "label": "ассоциация"}]},
    "k2": {"id": "k2", "rus_word": "счастье", "eng_word": "happiness", "neighbors": [{"id": "k1", "label": "синоним"}, {"id": "k5", "label": "гипоним"}, {"id": "k6", "label": "ассоциация"}]},
    "k3": {"id": "k3", "rus_word": "грусть", "eng_word": "sadness", "neighbors": [{"id": "k1", "label": "антоним"}, {"id": "k7", "label": "синоним"}]},
    "k4": {"id": "k4", "rus_word": "смех", "eng_word": "laughter", "neighbors": [{"id": "k1", "label": "ассоциация"}, {"id": "k8", "label": "мероним"}]},
    "k5": {"id": "k5", "rus_word": "восторг", "eng_word": "delight", "neighbors": [{"id": "k2", "label": "гипероним"}, {"id": "k9", "label": "синоним"}]},
    "k6": {"id": "k6", "rus_word": "улыбка", "eng_word": "smile", "neighbors": [{"id": "k2", "label": "ассоциация"}, {"id": "k10", "label": "пример"}]},
    "k7": {"id": "k7", "rus_word": "печаль", "eng_word": "sorrow", "neighbors": [{"id": "k3", "label": "синоним"}, {"id": "k11", "label": "гипоним"}]},
    "k8": {"id": "k8", "rus_word": "голос", "eng_word": "voice", "neighbors": [{"id": "k4", "label": "холоним"}, {"id": "k12", "label": "часть"}]},
    "k9": {"id": "k9", "rus_word": "экстаз", "eng_word": "ecstasy", "neighbors": [{"id": "k5", "label": "синоним"}]},
    "k10": {"id": "k10", "rus_word": "широкая_улыбка", "eng_word": "wide_smile", "neighbors": [{"id": "k6", "label": "гипоним"}]},
    "k11": {"id": "k11", "rus_word": "тоска", "eng_word": "yearning", "neighbors": [{"id": "k7", "label": "гипоним"}, {"id": "k13", "label": "синоним"}]},
    "k12": {"id": "k12", "rus_word": "связки", "eng_word": "ligaments", "neighbors": [{"id": "k8", "label": "мероним"}]},
    "k13": {"id": "k13", "rus_word": "меланхолия", "eng_word": "melancholy", "neighbors": [{"id": "k11", "label": "синоним"}]},
    "k14": {"id": "k14", "rus_word": "любовь", "eng_word": "love", "neighbors": [{"id": "k15", "label": "гипоним"}, {"id": "k16", "label": "антоним"}, {"id": "k17", "label": "ассоциация"}]},
    "k15": {"id": "k15", "rus_word": "романтика", "eng_word": "romance", "neighbors": [{"id": "k14", "label": "гипероним"}, {"id": "k18", "label": "синоним"}]},
    "k16": {"id": "k16", "rus_word": "ненависть", "eng_word": "hatred", "neighbors": [{"id": "k14", "label": "антоним"}, {"id": "k19", "label": "синоним"}]},
    "k17": {"id": "k17", "rus_word": "сердце", "eng_word": "heart", "neighbors": [{"id": "k14", "label": "ассоциация"}, {"id": "k20", "label": "мероним"}]},
    "k18": {"id": "k18", "rus_word": "флирт", "eng_word": "flirt", "neighbors": [{"id": "k15", "label": "гипоним"}]},
    "k19": {"id": "k19", "rus_word": "злоба", "eng_word": "malice", "neighbors": [{"id": "k16", "label": "синоним"}]},
    "k20": {"id": "k20", "rus_word": "аорта", "eng_word": "aorta", "neighbors": [{"id": "k17", "label": "холоним"}]},
    "k21": {"id": "k21", "rus_word": "мысль", "eng_word": "thought", "neighbors": [{"id": "k22", "label": "синоним"}, {"id": "k23", "label": "ассоциация"}]},
    "k22": {"id": "k22", "rus_word": "идея", "eng_word": "idea", "neighbors": [{"id": "k21", "label": "синоним"}, {"id": "k24", "label": "гипоним"}]},
    "k23": {"id": "k23", "rus_word": "мозг", "eng_word": "brain", "neighbors": [{"id": "k21", "label": "ассоциация"}, {"id": "k25", "label": "мероним"}]},
    "k24": {"id": "k24", "rus_word": "концепция", "eng_word": "concept", "neighbors": [{"id": "k22", "label": "гипероним"}]},
    "k25": {"id": "k25", "rus_word": "нейрон", "eng_word": "neuron", "neighbors": [{"id": "k23", "label": "холоним"}, {"id": "k26", "label": "часть"}]},
    "k26": {"id": "k26", "rus_word": "аксон", "eng_word": "axon", "neighbors": [{"id": "k25", "label": "мероним"}]},
    "k27": {"id": "k27", "rus_word": "красота", "eng_word": "beauty", "neighbors": [{"id": "k28", "label": "синоним"}, {"id": "k29", "label": "антоним"}]},
    "k28": {"id": "k28", "rus_word": "прелесть", "eng_word": "charm", "neighbors": [{"id": "k27", "label": "синоним"}]},
    "k29": {"id": "k29", "rus_word": "уродство", "eng_word": "ugliness", "neighbors": [{"id": "k27", "label": "антоним"}]},
    "k30": {"id": "k30", "rus_word": "эстетика", "eng_word": "aesthetics", "neighbors": [{"id": "k27", "label": "ассоциация"}, {"id": "k28", "label": "родственный"}]}
    }
    try:
        client.init_mock_data(mock_data)
        return Response({"status": "success", "message": "Mock data loaded"})
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)