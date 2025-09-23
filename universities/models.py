from django.db import models
import uuid


class University(models.Model):
    """Model representing a university"""
    
    university_id = models.CharField(max_length=20, unique=True, help_text="Unique identifier for the university")
    name = models.CharField(max_length=200, unique=True)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    website = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='university_logos/', blank=True, null=True)
    
    # Additional fields for future expansion
    established_year = models.IntegerField(blank=True, null=True)
    student_count = models.IntegerField(blank=True, null=True)
    ranking_world = models.IntegerField(blank=True, null=True)
    ranking_country = models.IntegerField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'universities'
        ordering = ['name']
        verbose_name_plural = 'Universities'
    
    def save(self, *args, **kwargs):
        if not self.university_id:
            # Generate a unique university_id based on name and country
            name_slug = ''.join(c.upper() for c in self.name if c.isalnum())[:6]
            country_slug = ''.join(c.upper() for c in self.country if c.isalnum())[:3]
            base_id = f"{name_slug}_{country_slug}"
            
            # Ensure uniqueness
            counter = 1
            self.university_id = f"{base_id}_{counter:02d}"
            while University.objects.filter(university_id=self.university_id).exists():
                counter += 1
                self.university_id = f"{base_id}_{counter:02d}"
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} - {self.city}, {self.country}"
    
    @property
    def programs_count(self):
        """Get the number of programs offered by this university"""
        return self.programs.count()
    
    @property
    def coordinators_count(self):
        """Get the number of coordinators for this university"""
        return self.coordinators.count()


class Program(models.Model):
    """Model representing a master's program"""
    
    DEGREE_LEVEL_CHOICES = [
        ('master', 'Master'),
        ('phd', 'PhD'),
        ('bachelor', 'Bachelor'),
        ('diploma', 'Diploma'),
    ]
    
    program_id = models.CharField(max_length=20, unique=True, help_text="Unique identifier for the program")
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='programs')
    name = models.CharField(max_length=300)
    field_of_study = models.CharField(max_length=200)
    degree_level = models.CharField(max_length=20, choices=DEGREE_LEVEL_CHOICES, default='master')
    description = models.TextField(blank=True, null=True)
    
    # Program details
    duration_months = models.IntegerField(blank=True, null=True, help_text="Duration in months")
    language = models.CharField(max_length=100, default='English')
    tuition_fee_euro = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    application_deadline = models.DateField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    
    # Requirements
    min_gpa = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    ielts_score = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    toefl_score = models.IntegerField(blank=True, null=True)
    gre_score = models.IntegerField(blank=True, null=True)
    
    # Additional information
    program_website = models.URLField(blank=True, null=True)
    brochure_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'programs'
        ordering = ['university__name', 'name']
        unique_together = ['university', 'name']
    
    def save(self, *args, **kwargs):
        if not self.program_id:
            # Generate a unique program_id based on university and program name
            university_prefix = self.university.university_id[:6] if self.university.university_id != 'TEMP_ID' else 'UNI'
            program_slug = ''.join(c.upper() for c in self.name if c.isalnum())[:6]
            base_id = f"{university_prefix}_{program_slug}"
            
            # Ensure uniqueness
            counter = 1
            self.program_id = f"{base_id}_{counter:02d}"
            while Program.objects.filter(program_id=self.program_id).exists():
                counter += 1
                self.program_id = f"{base_id}_{counter:02d}"
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} - {self.university.name}"
    
    @property
    def coordinators_count(self):
        """Get the number of coordinators for this program"""
        return self.coordinators.count()


class Coordinator(models.Model):
    """Model representing a program coordinator"""
    
    ROLE_CHOICES = [
        ('head', 'Head of Department'),
        ('coordinator', 'Program Coordinator'),
        ('advisor', 'Academic Advisor'),
        ('director', 'Program Director'),
        ('professor', 'Professor'),
    ]
    
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='coordinators')
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='coordinators')
    name = models.CharField(max_length=200)
    public_email = models.EmailField()
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='coordinator')
    
    # Additional contact information
    phone = models.CharField(max_length=20, blank=True, null=True)
    office_location = models.CharField(max_length=200, blank=True, null=True)
    office_hours = models.CharField(max_length=200, blank=True, null=True)
    
    # Professional information
    title = models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=200, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'coordinators'
        ordering = ['university__name', 'program__name', 'name']
        unique_together = ['program', 'public_email']
    
    def __str__(self):
        return f"{self.name} - {self.program.name}"