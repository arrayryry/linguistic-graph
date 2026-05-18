from rest_framework import serializers

class ConceptSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    ru_name = serializers.CharField(max_length=500)  
    en_name = serializers.CharField(max_length=500)  
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