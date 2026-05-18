from rest_framework import serializers


class ConceptSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    ru_name = serializers.CharField(max_length=500)  
    en_name = serializers.CharField(max_length=500)  

class NodeSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=50)
    rus_word = serializers.CharField(max_length=50)  
    eng_word = serializers.CharField(max_length=50) 
    node_type = serializers.CharField(max_length=30)  
    subtype = serializers.CharField(max_length=30, required=False) 
    # Семантическая роль (для анализа предложений)
    semantic_role = serializers.CharField(max_length=20, required=False)

class NodeWithNeighborsSerializer(serializers.Serializer):
    id = serializers.CharField()
    rus_word = serializers.CharField(max_length=50)  
    eng_word = serializers.CharField(max_length=50)  
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
    hypernym = serializers.IntegerField(allow_null=True, required=False)

class ConceptWithNeighborsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    ru_name = serializers.CharField(max_length=500)  
    en_name = serializers.CharField(max_length=500)  
    type = serializers.CharField()
    hypernym = serializers.IntegerField(allow_null=True)
    children = serializers.ListField(child=serializers.DictField())
    semantic_neighbors = serializers.ListField(child=serializers.DictField())

class CreateEdgeSerializer(serializers.Serializer):
    from_id = serializers.IntegerField()
    to_id = serializers.IntegerField()
    rel_type = serializers.CharField()

class UpdateConceptSerializer(serializers.Serializer):
    new_ru_name = serializers.CharField(max_length=500, required=False)
    new_en_name = serializers.CharField(max_length=500, required=False)
    new_type = serializers.CharField(max_length=50, required=False)
    new_hypernym = serializers.IntegerField(allow_null=True, required=False)
class UpdateNodeSerializer(serializers.Serializer):
    new_id = serializers.CharField(required=False)
    new_rus_word = serializers.CharField(max_length=50, required=False)  
    new_eng_word = serializers.CharField(max_length=50, required=False)  
    new_node_type = serializers.CharField(max_length=30, required=False) 
    new_subtype = serializers.CharField(max_length=30, required=False)  
    new_semantic_role = serializers.CharField(max_length=20, required=False) 

