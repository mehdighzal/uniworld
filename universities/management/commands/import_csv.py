from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from universities.models import University, Program, Coordinator
from payments.models import Subscription, Payment, EmailLog
import csv
import os
from datetime import datetime


class Command(BaseCommand):
    help = 'Import data from CSV files'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, help='CSV file to import')
        parser.add_argument('--model', type=str, help='Model to import to')

    def handle(self, *args, **options):
        file_path = options.get('file')
        model_name = options.get('model')

        if not file_path or not model_name:
            self.stdout.write(
                self.style.ERROR('Please provide --file and --model arguments')
            )
            return

        if not os.path.exists(file_path):
            self.stdout.write(
                self.style.ERROR(f'File {file_path} does not exist')
            )
            return

        try:
            if model_name == 'universities':
                self.import_universities(file_path)
            elif model_name == 'programs':
                self.import_programs(file_path)
            elif model_name == 'coordinators':
                self.import_coordinators(file_path)
            elif model_name == 'subscriptions':
                self.import_subscriptions(file_path)
            elif model_name == 'payments':
                self.import_payments(file_path)
            elif model_name == 'email_logs':
                self.import_email_logs(file_path)
            else:
                self.stdout.write(
                    self.style.ERROR(f'Unknown model: {model_name}')
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error importing data: {str(e)}')
            )

    def import_universities(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            count = 0
            for row in reader:
                university, created = University.objects.get_or_create(
                    university_id=row['university_id'],
                    defaults={
                        'name': row['name'],
                        'country': row['country'],
                        'city': row['city'],
                        'website': row['website'] if row['website'] else None,
                        'description': row['description'] if row['description'] else None,
                        'established_year': int(row['established_year']) if row['established_year'] else None,
                        'student_count': int(row['student_count']) if row['student_count'] else None,
                        'ranking_world': int(row['ranking_world']) if row['ranking_world'] else None,
                        'ranking_country': int(row['ranking_country']) if row['ranking_country'] else None,
                    }
                )
                if created:
                    count += 1
                    self.stdout.write(f'Created university: {university.name} ({university.university_id})')
                else:
                    self.stdout.write(f'University already exists: {university.name} ({university.university_id})')
            self.stdout.write(
                self.style.SUCCESS(f'Successfully imported {count} universities')
            )

    def import_programs(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            count = 0
            for row in reader:
                try:
                    university = University.objects.get(university_id=row['university_id'])
                    program, created = Program.objects.get_or_create(
                        program_id=row['program_id'],
                        defaults={
                            'university': university,
                            'name': row['name'],
                            'field_of_study': row['field_of_study'],
                            'degree_level': row['degree_level'],
                            'description': row['description'] if row['description'] else None,
                            'duration_months': int(row['duration_months']) if row['duration_months'] else None,
                            'language': row['language'],
                            'tuition_fee_euro': float(row['tuition_fee_euro']) if row['tuition_fee_euro'] else None,
                            'application_deadline': datetime.strptime(row['application_deadline'], '%Y-%m-%d').date() if row['application_deadline'] else None,
                            'start_date': datetime.strptime(row['start_date'], '%Y-%m-%d').date() if row['start_date'] else None,
                            'min_gpa': float(row['min_gpa']) if row['min_gpa'] else None,
                            'ielts_score': float(row['ielts_score']) if row['ielts_score'] else None,
                            'toefl_score': int(row['toefl_score']) if row['toefl_score'] else None,
                            'gre_score': int(row['gre_score']) if row['gre_score'] else None,
                            'program_website': row['program_website'] if row['program_website'] else None,
                            'brochure_url': row['brochure_url'] if row['brochure_url'] else None,
                            'is_active': row['is_active'].lower() == 'true',
                        }
                    )
                    if created:
                        count += 1
                        self.stdout.write(f'Created program: {program.name} ({program.program_id})')
                    else:
                        self.stdout.write(f'Program already exists: {program.name} ({program.program_id})')
                except University.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(f'University with ID {row["university_id"]} does not exist')
                    )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully imported {count} programs')
            )

    def import_coordinators(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            count = 0
            for row in reader:
                try:
                    program = Program.objects.get(program_id=row['program_id'])
                    # Get university from the program
                    university = program.university
                    
                    # Create full name from first_name and last_name
                    full_name = f"{row['first_name']} {row['last_name']}"
                    
                    coordinator, created = Coordinator.objects.get_or_create(
                        program=program,
                        public_email=row['email'],
                        defaults={
                            'university': university,
                            'name': full_name,
                            'role': row['role'],
                            'is_active': True,  # Default to active
                        }
                    )
                    if created:
                        count += 1
                        self.stdout.write(f'Created coordinator: {coordinator.name}')
                    else:
                        self.stdout.write(f'Coordinator already exists: {coordinator.name}')
                except Program.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(f'Program with ID {row["program_id"]} does not exist')
                    )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully imported {count} coordinators')
            )

    def import_subscriptions(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            count = 0
            for row in reader:
                try:
                    user = User.objects.get(id=row['user_id'])
                    subscription, created = Subscription.objects.get_or_create(
                        user=user,
                        stripe_subscription_id=row['stripe_subscription_id'] if row['stripe_subscription_id'] else None,
                        defaults={
                            'plan_type': row['plan_type'],
                            'status': row['status'],
                            'start_date': datetime.strptime(row['start_date'], '%Y-%m-%d %H:%M:%S'),
                            'end_date': datetime.strptime(row['end_date'], '%Y-%m-%d %H:%M:%S'),
                            'amount': float(row['amount']),
                            'currency': row['currency'],
                            'stripe_customer_id': row['stripe_customer_id'] if row['stripe_customer_id'] else None,
                        }
                    )
                    if created:
                        count += 1
                        self.stdout.write(f'Created subscription for user: {user.username}')
                    else:
                        self.stdout.write(f'Subscription already exists for user: {user.username}')
                except User.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(f'User with ID {row["user_id"]} does not exist')
                    )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully imported {count} subscriptions')
            )

    def import_payments(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            count = 0
            for row in reader:
                try:
                    user = User.objects.get(id=row['user_id'])
                    subscription = Subscription.objects.get(id=row['subscription_id'])
                    payment, created = Payment.objects.get_or_create(
                        user=user,
                        subscription=subscription,
                        stripe_payment_intent_id=row['stripe_payment_intent_id'] if row['stripe_payment_intent_id'] else None,
                        defaults={
                            'amount': float(row['amount']),
                            'currency': row['currency'],
                            'payment_method': row['payment_method'],
                            'status': row['status'],
                            'stripe_charge_id': row['stripe_charge_id'] if row['stripe_charge_id'] else None,
                            'payment_date': datetime.strptime(row['payment_date'], '%Y-%m-%d %H:%M:%S'),
                            'description': row['description'] if row['description'] else None,
                            'failure_reason': row['failure_reason'] if row['failure_reason'] else None,
                        }
                    )
                    if created:
                        count += 1
                        self.stdout.write(f'Created payment for user: {user.username}')
                    else:
                        self.stdout.write(f'Payment already exists for user: {user.username}')
                except (User.DoesNotExist, Subscription.DoesNotExist) as e:
                    self.stdout.write(
                        self.style.ERROR(f'User or Subscription does not exist: {str(e)}')
                    )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully imported {count} payments')
            )

    def import_email_logs(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            count = 0
            for row in reader:
                try:
                    user = User.objects.get(id=row['user_id'])
                    coordinator = Coordinator.objects.get(id=row['coordinator_id'])
                    email_log, created = EmailLog.objects.get_or_create(
                        user=user,
                        coordinator=coordinator,
                        subject=row['subject'],
                        defaults={
                            'body': row['body'],
                            'email_provider': row['email_provider'],
                            'status': row['status'],
                            'sent_at': datetime.strptime(row['sent_at'], '%Y-%m-%d %H:%M:%S') if row['sent_at'] else None,
                            'error_message': row['error_message'] if row['error_message'] else None,
                            'message_id': row['message_id'] if row['message_id'] else None,
                        }
                    )
                    if created:
                        count += 1
                        self.stdout.write(f'Created email log for user: {user.username}')
                    else:
                        self.stdout.write(f'Email log already exists for user: {user.username}')
                except (User.DoesNotExist, Coordinator.DoesNotExist) as e:
                    self.stdout.write(
                        self.style.ERROR(f'User or Coordinator does not exist: {str(e)}')
                    )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully imported {count} email logs')
            )
