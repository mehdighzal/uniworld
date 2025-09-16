from rest_framework import serializers
from .models import University, Program, Coordinator


class UniversitySerializer(serializers.ModelSerializer):
    """Serializer for University model"""
    
    programs_count = serializers.ReadOnlyField()
    coordinators_count = serializers.ReadOnlyField()
    
    class Meta:
        model = University
        fields = (
            'id', 'name', 'country', 'city', 'website', 'description',
            'established_year', 'student_count', 'ranking_world', 'ranking_country',
            'programs_count', 'coordinators_count', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')


class ProgramSerializer(serializers.ModelSerializer):
    """Serializer for Program model"""
    
    university_name = serializers.CharField(source='university.name', read_only=True)
    university_country = serializers.CharField(source='university.country', read_only=True)
    university_city = serializers.CharField(source='university.city', read_only=True)
    coordinators_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Program
        fields = (
            'id', 'university', 'university_name', 'university_country', 'university_city',
            'name', 'field_of_study', 'degree_level', 'description',
            'duration_months', 'language', 'tuition_fee_euro',
            'application_deadline', 'start_date',
            'min_gpa', 'ielts_score', 'toefl_score', 'gre_score',
            'program_website', 'brochure_url', 'is_active',
            'coordinators_count', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')


class CoordinatorSerializer(serializers.ModelSerializer):
    """Serializer for Coordinator model"""
    
    university_name = serializers.CharField(source='university.name', read_only=True)
    university_country = serializers.CharField(source='university.country', read_only=True)
    program_name = serializers.CharField(source='program.name', read_only=True)
    
    class Meta:
        model = Coordinator
        fields = (
            'id', 'university', 'university_name', 'university_country',
            'program', 'program_name', 'name', 'public_email', 'role',
            'phone', 'office_location', 'office_hours',
            'title', 'department', 'bio', 'is_active',
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')


class UniversityDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for University with programs and coordinators"""
    
    programs = ProgramSerializer(many=True, read_only=True)
    coordinators = CoordinatorSerializer(many=True, read_only=True)
    programs_count = serializers.ReadOnlyField()
    coordinators_count = serializers.ReadOnlyField()
    
    class Meta:
        model = University
        fields = (
            'id', 'name', 'country', 'city', 'website', 'description',
            'established_year', 'student_count', 'ranking_world', 'ranking_country',
            'programs', 'coordinators', 'programs_count', 'coordinators_count',
            'created_at', 'updated_at'
        )


class ProgramDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for Program with coordinators"""
    
    university = UniversitySerializer(read_only=True)
    coordinators = CoordinatorSerializer(many=True, read_only=True)
    coordinators_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Program
        fields = (
            'id', 'university', 'name', 'field_of_study', 'degree_level', 'description',
            'duration_months', 'language', 'tuition_fee_euro',
            'application_deadline', 'start_date',
            'min_gpa', 'ielts_score', 'toefl_score', 'gre_score',
            'program_website', 'brochure_url', 'is_active',
            'coordinators', 'coordinators_count', 'created_at', 'updated_at'
        )


class SearchSerializer(serializers.Serializer):
    """Serializer for search functionality"""
    
    query = serializers.CharField(max_length=200, required=False)
    country = serializers.CharField(max_length=100, required=False)
    field_of_study = serializers.CharField(max_length=200, required=False)
    degree_level = serializers.ChoiceField(choices=Program.DEGREE_LEVEL_CHOICES, required=False)
    language = serializers.CharField(max_length=100, required=False)
    min_tuition = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    max_tuition = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    university_id = serializers.IntegerField(required=False)
    
    def validate(self, attrs):
        if attrs.get('min_tuition') and attrs.get('max_tuition'):
            if attrs['min_tuition'] > attrs['max_tuition']:
                raise serializers.ValidationError("Min tuition cannot be greater than max tuition")
        return attrs
