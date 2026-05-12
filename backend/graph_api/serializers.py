"""добавила в узел 2 свойства"""
from rest_framework import serializers

class NodeSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=50)
    rus_word=serializers.CharField(max_lenght=50)
    eng_word=serializers.CharField(max_lenght=50)
    node_type = serializers.CharField(max_length=30)  
    subtype = serializers.CharField(max_length=30, required=False) 
    # Семантическая роль (для анализа предложений)
    semantic_role = serializers.CharField(max_length=20, required=False)
class NodeWithNeighborsSerializer(serializers.Serializer):
    id = serializers.CharField()
    rus_word=serializers.CharField(max_lenght=50)
    eng_word=serializers.CharField(max_lenght=50)
    node_type = serializers.CharField()
    subtype = serializers.CharField(required=False)
    semantic_role = serializers.CharField(required=False)
    neighbors = serializers.ListField(
        child=serializers.DictField()
    )

class EdgeSerializer(serializers.Serializer):
    from_id = serializers.CharField()
    to_id = serializers.CharField()
    type = serializers.CharField(max_length=50)

class CreateEdgeSerializer(serializers.Serializer):
    from_id = serializers.CharField()
    to_id = serializers.CharField()
    rel_type = serializers.CharField()

class UpdateNodeSerializer(serializers.Serializer):
    new_id = serializers.CharField(required=False)
    new_rus_word=serializers.CharField(max_lenght=50)
    new_eng_word=serializers.CharField(max_lenght=50)