# api/serializers.py
from rest_framework import serializers

class NodeSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=50)
    rus_word = serializers.CharField(max_length=50)
    eng_word = serializers.CharField(max_length=50)
    node_type = serializers.CharField(max_length=30)

class NodeWithNeighborsSerializer(serializers.Serializer):
    id = serializers.CharField()
    rus_word = serializers.CharField(max_length=50)
    eng_word = serializers.CharField(max_length=50)
    node_type = serializers.CharField()
    neighbors = serializers.ListField(child=serializers.DictField())

class CreateEdgeSerializer(serializers.Serializer):
    from_id = serializers.CharField()
    to_id = serializers.CharField()
    rel_type = serializers.CharField()

class UpdateNodeSerializer(serializers.Serializer):
    new_id = serializers.CharField(required=False)
    new_rus_word = serializers.CharField(max_length=50, required=False)
    new_eng_word = serializers.CharField(max_length=50, required=False)
    new_node_type = serializers.CharField(max_length=30, required=False)