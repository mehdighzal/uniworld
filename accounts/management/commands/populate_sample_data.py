from django.core.management.base import BaseCommand
from universities.models import University, Program, Coordinator


class Command(BaseCommand):
    help = 'Populate database with sample Italian universities and programs'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create Italian universities
        universities_data = [
            {
                'name': 'Università di Bologna',
                'country': 'Italy',
                'city': 'Bologna',
                'website': 'https://www.unibo.it',
                'description': 'The oldest university in the Western world, founded in 1088.',
                'established_year': 1088,
                'student_count': 85000,
                'ranking_world': 160,
                'ranking_country': 1
            },
            {
                'name': 'Sapienza Università di Roma',
                'country': 'Italy',
                'city': 'Rome',
                'website': 'https://www.uniroma1.it',
                'description': 'One of the largest universities in Europe.',
                'established_year': 1303,
                'student_count': 120000,
                'ranking_world': 171,
                'ranking_country': 2
            },
            {
                'name': 'Università degli Studi di Milano',
                'country': 'Italy',
                'city': 'Milan',
                'website': 'https://www.unimi.it',
                'description': 'Leading research university in Northern Italy.',
                'established_year': 1924,
                'student_count': 60000,
                'ranking_world': 301,
                'ranking_country': 3
            },
            {
                'name': 'Università di Padova',
                'country': 'Italy',
                'city': 'Padua',
                'website': 'https://www.unipd.it',
                'description': 'One of the oldest universities in Italy.',
                'established_year': 1222,
                'student_count': 65000,
                'ranking_world': 201,
                'ranking_country': 4
            },
            {
                'name': 'Politecnico di Milano',
                'country': 'Italy',
                'city': 'Milan',
                'website': 'https://www.polimi.it',
                'description': 'Leading technical university in Italy.',
                'established_year': 1863,
                'student_count': 45000,
                'ranking_world': 149,
                'ranking_country': 5
            }
        ]
        
        universities = []
        for uni_data in universities_data:
            university, created = University.objects.get_or_create(
                name=uni_data['name'],
                defaults=uni_data
            )
            universities.append(university)
            if created:
                self.stdout.write(f'Created university: {university.name}')
        
        # Create programs
        programs_data = [
            # University of Bologna programs
            {
                'university': universities[0],
                'name': 'Master in Computer Science',
                'field_of_study': 'Computer Science',
                'degree_level': 'master',
                'description': 'Advanced computer science program focusing on AI and machine learning.',
                'duration_months': 24,
                'language': 'English',
                'tuition_fee_euro': 2000.00,
                'min_gpa': 3.0,
                'ielts_score': 6.5
            },
            {
                'university': universities[0],
                'name': 'Master in Economics',
                'field_of_study': 'Economics',
                'degree_level': 'master',
                'description': 'Comprehensive economics program with focus on European markets.',
                'duration_months': 24,
                'language': 'English',
                'tuition_fee_euro': 1500.00,
                'min_gpa': 3.2,
                'ielts_score': 6.0
            },
            # Sapienza programs
            {
                'university': universities[1],
                'name': 'Master in Architecture',
                'field_of_study': 'Architecture',
                'degree_level': 'master',
                'description': 'Renowned architecture program with focus on sustainable design.',
                'duration_months': 24,
                'language': 'Italian',
                'tuition_fee_euro': 1000.00,
                'min_gpa': 3.0,
                'ielts_score': 5.5
            },
            {
                'university': universities[1],
                'name': 'Master in International Relations',
                'field_of_study': 'Political Science',
                'degree_level': 'master',
                'description': 'Global perspective on international politics and diplomacy.',
                'duration_months': 24,
                'language': 'English',
                'tuition_fee_euro': 1200.00,
                'min_gpa': 3.1,
                'ielts_score': 6.5
            },
            # University of Milan programs
            {
                'university': universities[2],
                'name': 'Master in Business Administration',
                'field_of_study': 'Business Administration',
                'degree_level': 'master',
                'description': 'Comprehensive MBA program with focus on European business.',
                'duration_months': 18,
                'language': 'English',
                'tuition_fee_euro': 15000.00,
                'min_gpa': 3.5,
                'ielts_score': 7.0
            },
            {
                'university': universities[2],
                'name': 'Master in Medicine',
                'field_of_study': 'Medicine',
                'degree_level': 'master',
                'description': 'Advanced medical program with clinical rotations.',
                'duration_months': 36,
                'language': 'Italian',
                'tuition_fee_euro': 3000.00,
                'min_gpa': 3.7,
                'ielts_score': 6.0
            },
            # University of Padua programs
            {
                'university': universities[3],
                'name': 'Master in Engineering',
                'field_of_study': 'Engineering',
                'degree_level': 'master',
                'description': 'Advanced engineering program with focus on innovation.',
                'duration_months': 24,
                'language': 'English',
                'tuition_fee_euro': 2500.00,
                'min_gpa': 3.3,
                'ielts_score': 6.5
            },
            {
                'university': universities[3],
                'name': 'Master in Psychology',
                'field_of_study': 'Psychology',
                'degree_level': 'master',
                'description': 'Comprehensive psychology program with clinical focus.',
                'duration_months': 24,
                'language': 'Italian',
                'tuition_fee_euro': 1800.00,
                'min_gpa': 3.2,
                'ielts_score': 6.0
            },
            # Politecnico di Milano programs
            {
                'university': universities[4],
                'name': 'Master in Mechanical Engineering',
                'field_of_study': 'Mechanical Engineering',
                'degree_level': 'master',
                'description': 'Advanced mechanical engineering with focus on automotive industry.',
                'duration_months': 24,
                'language': 'English',
                'tuition_fee_euro': 4000.00,
                'min_gpa': 3.4,
                'ielts_score': 6.5
            },
            {
                'university': universities[4],
                'name': 'Master in Design',
                'field_of_study': 'Design',
                'degree_level': 'master',
                'description': 'Innovative design program with focus on product and industrial design.',
                'duration_months': 24,
                'language': 'English',
                'tuition_fee_euro': 3500.00,
                'min_gpa': 3.0,
                'ielts_score': 6.0
            }
        ]
        
        programs = []
        for prog_data in programs_data:
            program, created = Program.objects.get_or_create(
                university=prog_data['university'],
                name=prog_data['name'],
                defaults=prog_data
            )
            programs.append(program)
            if created:
                self.stdout.write(f'Created program: {program.name}')
        
        # Create coordinators
        coordinators_data = [
            # Computer Science coordinators
            {
                'university': universities[0],
                'program': programs[0],
                'name': 'Prof. Marco Rossi',
                'public_email': 'marco.rossi@unibo.it',
                'role': 'head',
                'title': 'Professor',
                'department': 'Computer Science',
                'phone': '+39 051 209 1000',
                'office_location': 'Building A, Room 201'
            },
            {
                'university': universities[0],
                'program': programs[0],
                'name': 'Dr. Anna Bianchi',
                'public_email': 'anna.bianchi@unibo.it',
                'role': 'coordinator',
                'title': 'Assistant Professor',
                'department': 'Computer Science',
                'phone': '+39 051 209 1001',
                'office_location': 'Building A, Room 202'
            },
            # Economics coordinators
            {
                'university': universities[0],
                'program': programs[1],
                'name': 'Prof. Giuseppe Verdi',
                'public_email': 'giuseppe.verdi@unibo.it',
                'role': 'head',
                'title': 'Professor',
                'department': 'Economics',
                'phone': '+39 051 209 2000',
                'office_location': 'Building B, Room 301'
            },
            # Architecture coordinators
            {
                'university': universities[1],
                'program': programs[2],
                'name': 'Prof. Francesca Romano',
                'public_email': 'francesca.romano@uniroma1.it',
                'role': 'director',
                'title': 'Professor',
                'department': 'Architecture',
                'phone': '+39 06 4991 0000',
                'office_location': 'Faculty Building, Room 101'
            },
            # International Relations coordinators
            {
                'university': universities[1],
                'program': programs[3],
                'name': 'Dr. Alessandro Conti',
                'public_email': 'alessandro.conti@uniroma1.it',
                'role': 'coordinator',
                'title': 'Associate Professor',
                'department': 'Political Science',
                'phone': '+39 06 4991 1000',
                'office_location': 'Faculty Building, Room 201'
            },
            # MBA coordinators
            {
                'university': universities[2],
                'program': programs[4],
                'name': 'Prof. Maria Ferrari',
                'public_email': 'maria.ferrari@unimi.it',
                'role': 'director',
                'title': 'Professor',
                'department': 'Business School',
                'phone': '+39 02 503 25000',
                'office_location': 'Business School, Room 501'
            },
            # Medicine coordinators
            {
                'university': universities[2],
                'program': programs[5],
                'name': 'Prof. Roberto Lombardi',
                'public_email': 'roberto.lombardi@unimi.it',
                'role': 'head',
                'title': 'Professor',
                'department': 'Medicine',
                'phone': '+39 02 503 30000',
                'office_location': 'Medical Faculty, Room 301'
            },
            # Engineering coordinators
            {
                'university': universities[3],
                'program': programs[6],
                'name': 'Prof. Elena Moretti',
                'public_email': 'elena.moretti@unipd.it',
                'role': 'head',
                'title': 'Professor',
                'department': 'Engineering',
                'phone': '+39 049 827 5000',
                'office_location': 'Engineering Building, Room 401'
            },
            # Psychology coordinators
            {
                'university': universities[3],
                'program': programs[7],
                'name': 'Dr. Paolo Gentile',
                'public_email': 'paolo.gentile@unipd.it',
                'role': 'coordinator',
                'title': 'Assistant Professor',
                'department': 'Psychology',
                'phone': '+39 049 827 6000',
                'office_location': 'Psychology Building, Room 201'
            },
            # Mechanical Engineering coordinators
            {
                'university': universities[4],
                'program': programs[8],
                'name': 'Prof. Stefano Russo',
                'public_email': 'stefano.russo@polimi.it',
                'role': 'head',
                'title': 'Professor',
                'department': 'Mechanical Engineering',
                'phone': '+39 02 2399 0000',
                'office_location': 'Engineering Campus, Building 1'
            },
            # Design coordinators
            {
                'university': universities[4],
                'program': programs[9],
                'name': 'Prof. Laura Santoro',
                'public_email': 'laura.santoro@polimi.it',
                'role': 'director',
                'title': 'Professor',
                'department': 'Design',
                'phone': '+39 02 2399 1000',
                'office_location': 'Design Campus, Building 2'
            }
        ]
        
        for coord_data in coordinators_data:
            coordinator, created = Coordinator.objects.get_or_create(
                program=coord_data['program'],
                public_email=coord_data['public_email'],
                defaults=coord_data
            )
            if created:
                self.stdout.write(f'Created coordinator: {coordinator.name}')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {len(universities)} universities, '
                f'{len(programs)} programs, and {len(coordinators_data)} coordinators'
            )
        )
