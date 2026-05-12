"""добавила в узел больше атрибутов и нужно изменить memgraph_client и views """
from rest_framework import serializers

class NodeSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=50)
    rus_word=serializers.CharField(max_lenght=50)
    eng_word=serializers.CharField(max_lenght=50)
class NodeWithNeighborsSerializer(serializers.Serializer):
    id = serializers.CharField()
    rus_word=serializers.CharField(max_lenght=50)
    eng_word=serializers.CharField(max_lenght=50)
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