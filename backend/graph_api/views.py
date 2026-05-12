from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .memgraph_client import MemgraphClient
from .serializers import NodeSerializer, CreateEdgeSerializer, UpdateNodeSerializer

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
    Body: {
        "id": "k1", 
        "rus_word": "слово", 
        "eng_word": "word",
        "node_type": "OBJECT",
        "subtype": "PERSON",
        "semantic_role": "AGENT"
    }"""
    serializer = NodeSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data
    client.add_node(
        node_id=data['id'],
        rus_word=data.get('rus_word', ''),
        eng_word=data.get('eng_word', ''),
        node_type=data.get('node_type', 'OBJECT'),
        subtype=data.get('subtype', ''),
        semantic_role=data.get('semantic_role', '')
    )
    return Response({"status": "ok", "id": data['id']}, status=status.HTTP_201_CREATED)

@api_view(['PUT'])
def update_node(request, node_id):
    """PUT /api/node/k1/update - обновить узел
    Body: {
        "new_id": "new_id",
        "new_rus_word": "новое",
        "new_eng_word": "new",
        "new_node_type": "ACTION",
        "new_subtype": "MENTAL",
        "new_semantic_role": "AGENT"
    }"""
    serializer = UpdateNodeSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data
    success = client.update_node(
        old_id=node_id,
        new_id=data.get('new_id'),
        new_rus_word=data.get('new_rus_word'),
        new_eng_word=data.get('new_eng_word'),
        new_node_type=data.get('new_node_type'),
        new_subtype=data.get('new_subtype'),
        new_semantic_role=data.get('new_semantic_role')
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
    Body: {"from": "k1", "to": "k2", "relation": "синоним"}"""
    serializer = CreateEdgeSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data
    client.add_edge(data['from_id'], data['to_id'], data['rel_type'])
    return Response({"status": "ok"})

@api_view(['DELETE'])
def delete_edge(request):
    """DELETE /api/edge/delete - удалить связь
    Body: {"from": "k1", "to": "k2"}"""
    from_id = request.data.get('from')
    to_id = request.data.get('to')
    relation = request.data.get('relation')
    
    if not from_id or not to_id:
        return Response({"error": "Missing 'from' or 'to'"}, status=status.HTTP_400_BAD_REQUEST)
    
    client.delete_edge(from_id, to_id, relation)
    return Response({"status": "deleted"})

@api_view(['POST'])
def init_mock_data(request):
    """POST /api/init-mock/ - загрузить тестовые данные"""
    mock_data = {
    "joy_1": {
        "id": "joy_1",
        "rus_word": "радость",
        "eng_word": "joy",
        "node_type": "OBJECT",
        "subtype": "ABSTRACT",
        "semantic_role": "",
        "neighbors": [{"id": "happiness_1", "label": "синоним"}]
    },
    "happiness_1": {
        "id": "happiness_1",
        "rus_word": "счастье",
        "eng_word": "happiness",
        "node_type": "OBJECT",
        "subtype": "ABSTRACT",
        "semantic_role": "",
        "neighbors": [{"id": "joy_1", "label": "синоним"}]
    },
    "good_1": {
        "id": "good_1",
        "rus_word": "хороший",
        "eng_word": "good",
        "node_type": "ATTRIBUTE",
        "subtype": "QUALITY",
        "semantic_role": "",
        "neighbors": [{"id": "bad_1", "label": "антоним"}]
    },
    "bad_1": {
        "id": "bad_1",
        "rus_word": "плохой",
        "eng_word": "bad",
        "node_type": "ATTRIBUTE",
        "subtype": "QUALITY",
        "semantic_role": "",
        "neighbors": [{"id": "good_1", "label": "антоним"}]
    },
    "dog_1": {
        "id": "dog_1",
        "rus_word": "собака",
        "eng_word": "dog",
        "node_type": "OBJECT",
        "subtype": "ANIMAL",
        "semantic_role": "",
        "neighbors": [{"id": "animal_1", "label": "гипоним"}]
    },
    "animal_1": {
        "id": "animal_1",
        "rus_word": "животное",
        "eng_word": "animal",
        "node_type": "OBJECT",
        "subtype": "ANIMAL",
        "semantic_role": "",
        "neighbors": [{"id": "dog_1", "label": "гипероним"}]
    },
    "wheel_1": {
        "id": "wheel_1",
        "rus_word": "колесо",
        "eng_word": "wheel",
        "node_type": "OBJECT",
        "subtype": "PHYSICAL",
        "semantic_role": "",
        "neighbors": [{"id": "car_1", "label": "мероним"}]
    },
    "car_1": {
        "id": "car_1",
        "rus_word": "машина",
        "eng_word": "car",
        "node_type": "OBJECT",
        "subtype": "PHYSICAL",
        "semantic_role": "",
        "neighbors": [{"id": "wheel_1", "label": "голоним"}]
    },
    "doctor_1": {
        "id": "doctor_1",
        "rus_word": "врач",
        "eng_word": "doctor",
        "node_type": "OBJECT",
        "subtype": "PERSON",
        "semantic_role": "",
        "neighbors": [{"id": "hospital_1", "label": "ассоциация"}]
    },
    "hospital_1": {
        "id": "hospital_1",
        "rus_word": "больница",
        "eng_word": "hospital",
        "node_type": "OBJECT",
        "subtype": "LOCATION",
        "semantic_role": "",
        "neighbors": [{"id": "doctor_1", "label": "ассоциация"}]
    },
    "rain_1": {
        "id": "rain_1",
        "rus_word": "дождь",
        "eng_word": "rain",
        "node_type": "OBJECT",
        "subtype": "PHENOMENON",
        "semantic_role": "",
        "neighbors": [{"id": "wet_1", "label": "причина"}]
    },
    "wet_1": {
        "id": "wet_1",
        "rus_word": "мокрый",
        "eng_word": "wet",
        "node_type": "ATTRIBUTE",
        "subtype": "STATE",
        "semantic_role": "",
        "neighbors": [{"id": "rain_1", "label": "следствие"}]
    },
    "knife_1": {
        "id": "knife_1",
        "rus_word": "нож",
        "eng_word": "knife",
        "node_type": "OBJECT",
        "subtype": "TOOL",
        "semantic_role": "INSTRUMENT",
        "neighbors": [{"id": "cut_1", "label": "инструмент"}]
    },
    "cut_1": {
        "id": "cut_1",
        "rus_word": "резать",
        "eng_word": "cut",
        "node_type": "ACTION",
        "subtype": "PHYSICAL",
        "semantic_role": "",
        "neighbors": [{"id": "knife_1", "label": "инструмент"}]
    },
    "school_1": {
        "id": "school_1",
        "rus_word": "школа",
        "eng_word": "school",
        "node_type": "OBJECT",
        "subtype": "LOCATION",
        "semantic_role": "LOCATION",
        "neighbors": [{"id": "study_1", "label": "локация"}]
    },
    "study_1": {
        "id": "study_1",
        "rus_word": "учиться",
        "eng_word": "study",
        "node_type": "ACTION",
        "subtype": "MENTAL",
        "semantic_role": "",
        "neighbors": [{"id": "school_1", "label": "локация"}]
    },
    "teacher_1": {
        "id": "teacher_1",
        "rus_word": "учитель",
        "eng_word": "teacher",
        "node_type": "OBJECT",
        "subtype": "PERSON",
        "semantic_role": "",
        "neighbors": [{"id": "pupil_1", "label": "коним"}]
    },
    "pupil_1": {
        "id": "pupil_1",
        "rus_word": "ученик",
        "eng_word": "pupil",
        "node_type": "OBJECT",
        "subtype": "PERSON",
        "semantic_role": "",
        "neighbors": [{"id": "teacher_1", "label": "коним"}]
    },
    "read_1": {
        "id": "read_1",
        "rus_word": "читать",
        "eng_word": "read",
        "node_type": "ACTION",
        "subtype": "MENTAL",
        "semantic_role": "",
        "neighbors": [{"id": "book_1", "label": "действие_на"}]
    },
    "book_1": {
        "id": "book_1",
        "rus_word": "книга",
        "eng_word": "book",
        "node_type": "OBJECT",
        "subtype": "ABSTRACT",
        "semantic_role": "PATIENT",
        "neighbors": [{"id": "read_1", "label": "объект_действия"}]
    }
}
    try:
        client.init_mock_data(mock_data)
        return Response({"status": "success", "message": "Mock data loaded"})
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
