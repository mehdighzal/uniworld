from django.urls import path
from . import views

urlpatterns = [
    # University endpoints
    path('universities/', views.UniversityListView.as_view(), name='university-list'),
    path('universities/<int:pk>/', views.UniversityDetailView.as_view(), name='university-detail'),
    path('universities/<int:university_id>/programs/', views.programs_by_university_view, name='programs-by-university'),
    
    # Program endpoints
    path('programs/', views.ProgramListView.as_view(), name='program-list'),
    path('programs/<int:pk>/', views.ProgramDetailView.as_view(), name='program-detail'),
    path('programs/<int:program_id>/coordinators/', views.coordinators_by_program_view, name='coordinators-by-program'),
    
    # Coordinator endpoints
    path('coordinators/', views.CoordinatorListView.as_view(), name='coordinator-list'),
    
    # Search and filter endpoints
    path('search/', views.search_view, name='search'),
    path('countries/', views.countries_list_view, name='countries-list'),
    path('fields-of-study/', views.fields_of_study_list_view, name='fields-of-study-list'),
]
