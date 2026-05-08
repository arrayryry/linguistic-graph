# api/serializers.py
from rest_framework import serializers

class NodeSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=50)
    
class NodeWithNeighborsSerializer(serializers.Serializer):
    id = serializers.CharField()
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