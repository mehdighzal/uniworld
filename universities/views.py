from rest_framework import generics, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import University, Program, Coordinator
from .serializers import (
    UniversitySerializer, ProgramSerializer, CoordinatorSerializer,
    UniversityDetailSerializer, ProgramDetailSerializer, SearchSerializer
)


class UniversityListView(generics.ListAPIView):
    """View for listing universities"""
    
    queryset = University.objects.all()
    serializer_class = UniversitySerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['country', 'city']
    search_fields = ['name', 'city', 'country', 'description']
    ordering_fields = ['name', 'created_at', 'ranking_world']
    ordering = ['name']


class UniversityDetailView(generics.RetrieveAPIView):
    """View for university details"""
    
    queryset = University.objects.all()
    serializer_class = UniversityDetailSerializer
    permission_classes = [permissions.AllowAny]


class ProgramListView(generics.ListAPIView):
    """View for listing programs"""
    
    queryset = Program.objects.filter(is_active=True).select_related('university')
    serializer_class = ProgramSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['university__country', 'field_of_study', 'degree_level', 'language']
    search_fields = ['name', 'field_of_study', 'description', 'university__name']
    ordering_fields = ['name', 'tuition_fee_euro', 'created_at']
    ordering = ['university__name', 'name']


class ProgramDetailView(generics.RetrieveAPIView):
    """View for program details"""
    
    queryset = Program.objects.filter(is_active=True).select_related('university')
    serializer_class = ProgramDetailSerializer
    permission_classes = [permissions.AllowAny]


class CoordinatorListView(generics.ListAPIView):
    """View for listing coordinators"""
    
    queryset = Coordinator.objects.filter(is_active=True).select_related('university', 'program')
    serializer_class = CoordinatorSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['university__country', 'role', 'program__field_of_study']
    search_fields = ['name', 'public_email', 'university__name', 'program__name']
    ordering_fields = ['name', 'created_at']
    ordering = ['university__name', 'program__name', 'name']


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def search_view(request):
    """Advanced search view for universities and programs"""
    
    serializer = SearchSerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)
    
    data = serializer.validated_data
    
    # Build query for programs
    programs_query = Program.objects.filter(is_active=True).select_related('university')
    
    if data.get('query'):
        programs_query = programs_query.filter(
            Q(name__icontains=data['query']) |
            Q(field_of_study__icontains=data['query']) |
            Q(description__icontains=data['query']) |
            Q(university__name__icontains=data['query'])
        )
    
    if data.get('country'):
        programs_query = programs_query.filter(university__country__icontains=data['country'])
    
    if data.get('field_of_study'):
        programs_query = programs_query.filter(field_of_study__icontains=data['field_of_study'])
    
    if data.get('degree_level'):
        programs_query = programs_query.filter(degree_level=data['degree_level'])
    
    if data.get('language'):
        programs_query = programs_query.filter(language__icontains=data['language'])
    
    if data.get('university_id'):
        programs_query = programs_query.filter(university_id=data['university_id'])
    
    if data.get('min_tuition'):
        programs_query = programs_query.filter(tuition_fee_euro__gte=data['min_tuition'])
    
    if data.get('max_tuition'):
        programs_query = programs_query.filter(tuition_fee_euro__lte=data['max_tuition'])
    
    # Get unique universities from filtered programs
    universities = University.objects.filter(
        programs__in=programs_query
    ).distinct()
    
    return Response({
        'programs': ProgramSerializer(programs_query[:50], many=True).data,
        'universities': UniversitySerializer(universities[:20], many=True).data,
        'total_programs': programs_query.count(),
        'total_universities': universities.count()
    })


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def countries_list_view(request):
    """View for getting list of countries"""
    
    countries = University.objects.values_list('country', flat=True).distinct().order_by('country')
    return Response({'countries': list(countries)})


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def fields_of_study_list_view(request):
    """View for getting list of fields of study"""
    
    fields = Program.objects.values_list('field_of_study', flat=True).distinct().order_by('field_of_study')
    return Response({'fields_of_study': list(fields)})


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def programs_by_university_view(request, university_id):
    """View for getting programs by university"""
    
    try:
        university = University.objects.get(id=university_id)
        programs = Program.objects.filter(university=university, is_active=True)
        
        return Response({
            'university': UniversitySerializer(university).data,
            'programs': ProgramSerializer(programs, many=True).data
        })
    except University.DoesNotExist:
        return Response({'error': 'University not found'}, status=404)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def coordinators_by_program_view(request, program_id):
    """View for getting coordinators by program"""
    
    try:
        program = Program.objects.get(id=program_id, is_active=True)
        coordinators = Coordinator.objects.filter(program=program, is_active=True)
        
        return Response({
            'program': ProgramSerializer(program).data,
            'coordinators': CoordinatorSerializer(coordinators, many=True).data
        })
    except Program.DoesNotExist:
        return Response({'error': 'Program not found'}, status=404)