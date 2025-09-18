"""
AI-powered email suggestion service for UniWorld platform.
This module provides intelligent email subject and content generation using OpenAI.
"""

import openai
from django.conf import settings
from typing import Dict, List, Optional
import logging
import json

logger = logging.getLogger(__name__)

class EmailSuggestionService:
    """Service for generating AI-powered email suggestions"""
    
    def __init__(self):
        """Initialize the OpenAI client"""
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = getattr(settings, 'OPENAI_MODEL', 'gpt-3.5-turbo')
    
    def generate_email_subject(self, 
                             program_name: str, 
                             university_name: str, 
                             coordinator_name: str,
                             email_type: str = 'inquiry',
                             student_profile: Optional[Dict] = None,
                             language: str = 'en') -> str:
        """
        Generate an AI-powered email subject line
        
        Args:
            program_name: Name of the master's program
            university_name: Name of the university
            coordinator_name: Name of the coordinator
            email_type: Type of email (inquiry, admission, scholarship, etc.)
            student_profile: Optional student profile information
            language: Language code (en, it, fr, es, de, pt, nl, ru, zh, ja, ko, ar)
            
        Returns:
            Generated subject line
        """
        try:
            prompt = self._build_subject_prompt(
                program_name, university_name, coordinator_name, 
                email_type, student_profile, language
            )
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": f"You are an expert academic communication assistant. Generate professional, concise email subject lines for students contacting university coordinators. Respond in {language}."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except openai.RateLimitError as e:
            logger.warning(f"OpenAI rate limit exceeded, using fallback: {str(e)}")
            return self._fallback_subject(program_name, university_name, email_type)
        except openai.APIError as e:
            logger.warning(f"OpenAI API error, using fallback: {str(e)}")
            return self._fallback_subject(program_name, university_name, email_type)
        except Exception as e:
            logger.error(f"Error generating email subject: {str(e)}")
            return self._fallback_subject(program_name, university_name, email_type)
    
    def generate_email_content(self,
                              program_name: str,
                              university_name: str,
                              coordinator_name: str,
                              coordinator_role: str,
                              email_type: str = 'inquiry',
                              student_profile: Optional[Dict] = None,
                              custom_requirements: Optional[List[str]] = None,
                              language: str = 'en') -> str:
        """
        Generate AI-powered email content
        
        Args:
            program_name: Name of the master's program
            university_name: Name of the university
            coordinator_name: Name of the coordinator
            coordinator_role: Role of the coordinator
            email_type: Type of email (inquiry, admission, scholarship, etc.)
            student_profile: Optional student profile information
            custom_requirements: Optional list of specific requirements/questions
            language: Language code (en, it, fr, es, de, pt, nl, ru, zh, ja, ko, ar)
            
        Returns:
            Generated email content
        """
        try:
            prompt = self._build_content_prompt(
                program_name, university_name, coordinator_name, 
                coordinator_role, email_type, student_profile, custom_requirements, language
            )
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": f"You are an expert academic communication assistant. Generate professional, personalized email content for students contacting university coordinators. Be respectful, specific, and demonstrate genuine interest in the program. Respond in {language}."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except openai.RateLimitError as e:
            logger.warning(f"OpenAI rate limit exceeded, using fallback: {str(e)}")
            return self._fallback_content(program_name, university_name, coordinator_name, email_type)
        except openai.APIError as e:
            logger.warning(f"OpenAI API error, using fallback: {str(e)}")
            return self._fallback_content(program_name, university_name, coordinator_name, email_type)
        except Exception as e:
            logger.error(f"Error generating email content: {str(e)}")
            return self._fallback_content(program_name, university_name, coordinator_name, email_type)
    
    def generate_multiple_subjects(self,
                                  program_name: str,
                                  university_name: str,
                                  coordinator_name: str,
                                  email_type: str = 'inquiry',
                                  count: int = 3) -> List[str]:
        """
        Generate multiple subject line options
        
        Args:
            program_name: Name of the master's program
            university_name: Name of the university
            coordinator_name: Name of the coordinator
            email_type: Type of email (inquiry, admission, scholarship, etc.)
            count: Number of subject options to generate
            
        Returns:
            List of generated subject lines
        """
        try:
            prompt = f"""Generate {count} different professional email subject lines for a student contacting {coordinator_name} at {university_name} about the {program_name} program.

Email type: {email_type}
Program: {program_name}
University: {university_name}
Coordinator: {coordinator_name}

Requirements:
- Each subject should be unique and professional
- Keep them concise (under 60 characters)
- Make them specific to the program and university
- Vary the tone and approach
- One subject per line

Return only the subject lines, one per line."""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert academic communication assistant. Generate multiple professional email subject line options."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.8
            )
            
            subjects = response.choices[0].message.content.strip().split('\n')
            return [subject.strip() for subject in subjects if subject.strip()]
            
        except openai.RateLimitError as e:
            logger.warning(f"OpenAI rate limit exceeded, using fallback: {str(e)}")
            return [self._fallback_subject(program_name, university_name, email_type)]
        except openai.APIError as e:
            logger.warning(f"OpenAI API error, using fallback: {str(e)}")
            return [self._fallback_subject(program_name, university_name, email_type)]
        except Exception as e:
            logger.error(f"Error generating multiple subjects: {str(e)}")
            return [self._fallback_subject(program_name, university_name, email_type)]
    
    def enhance_email_content(self,
                            current_content: str,
                            program_name: str,
                            university_name: str,
                            coordinator_name: str,
                            coordinator_role: str,
                            enhancement_type: str = 'improve') -> str:
        """
        Enhance existing email content with AI suggestions
        
        Args:
            current_content: The current email content
            program_name: Name of the master's program
            university_name: Name of the university
            coordinator_name: Name of the coordinator
            coordinator_role: Role of the coordinator
            enhancement_type: Type of enhancement (improve, personalize, shorten, expand)
            
        Returns:
            Enhanced email content
        """
        try:
            prompt = f"""Please {enhancement_type} the following email content for a student contacting {coordinator_name} ({coordinator_role}) at {university_name} about the {program_name} program.

Current content:
{current_content}

Email type: inquiry
Program: {program_name}
University: {university_name}
Coordinator: {coordinator_name} ({coordinator_role})

Requirements:
- Maintain the original intent and key points
- Keep it professional and respectful
- Make it more engaging and personalized
- Ensure proper academic email format
- Keep the same tone but improve clarity and impact

Return only the enhanced email content."""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert academic communication assistant. Enhance email content while maintaining professionalism and the original intent."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except openai.RateLimitError as e:
            logger.warning(f"OpenAI rate limit exceeded, using fallback: {str(e)}")
            return self._fallback_content(program_name, university_name, coordinator_name, 'inquiry')
        except openai.APIError as e:
            logger.warning(f"OpenAI API error, using fallback: {str(e)}")
            return self._fallback_content(program_name, university_name, coordinator_name, 'inquiry')
        except Exception as e:
            logger.error(f"Error enhancing email content: {str(e)}")
            return self._fallback_content(program_name, university_name, coordinator_name, 'inquiry')
    
    def _build_subject_prompt(self, program_name, university_name, coordinator_name, email_type, student_profile, language='en'):
        """Build the prompt for subject generation"""
        # Language-specific prompts
        language_prompts = {
            'en': f"""Generate a professional email subject line for a student contacting {coordinator_name} at {university_name} about the {program_name} program.

Email type: {email_type}
Program: {program_name}
University: {university_name}
Coordinator: {coordinator_name}""",
            'it': f"""Genera un oggetto email professionale per uno studente che contatta {coordinator_name} presso {university_name} riguardo al programma {program_name}.

Tipo email: {email_type}
Programma: {program_name}
Università: {university_name}
Coordinatore: {coordinator_name}""",
            'fr': f"""Générez un objet d'email professionnel pour un étudiant contactant {coordinator_name} à {university_name} concernant le programme {program_name}.

Type d'email: {email_type}
Programme: {program_name}
Université: {university_name}
Coordinateur: {coordinator_name}""",
            'es': f"""Genera un asunto de email profesional para un estudiante que contacta a {coordinator_name} en {university_name} sobre el programa {program_name}.

Tipo de email: {email_type}
Programa: {program_name}
Universidad: {university_name}
Coordinador: {coordinator_name}""",
            'de': f"""Generieren Sie einen professionellen E-Mail-Betreff für einen Studenten, der {coordinator_name} an der {university_name} bezüglich des Programms {program_name} kontaktiert.

E-Mail-Typ: {email_type}
Programm: {program_name}
Universität: {university_name}
Koordinator: {coordinator_name}""",
            'pt': f"""Gere um assunto de email profissional para um estudante entrando em contato com {coordinator_name} na {university_name} sobre o programa {program_name}.

Tipo de email: {email_type}
Programa: {program_name}
Universidade: {university_name}
Coordenador: {coordinator_name}""",
            'nl': f"""Genereer een professioneel email-onderwerp voor een student die {coordinator_name} bij {university_name} contacteert over het programma {program_name}.

Email type: {email_type}
Programma: {program_name}
Universiteit: {university_name}
Coördinator: {coordinator_name}""",
            'ru': f"""Создайте профессиональную тему письма для студента, обращающегося к {coordinator_name} в {university_name} по поводу программы {program_name}.

Тип письма: {email_type}
Программа: {program_name}
Университет: {university_name}
Координатор: {coordinator_name}""",
            'zh': f"""为联系{university_name}的{coordinator_name}询问{program_name}项目的学生生成专业的邮件主题。

邮件类型: {email_type}
项目: {program_name}
大学: {university_name}
协调员: {coordinator_name}""",
            'ja': f"""{university_name}の{coordinator_name}に{program_name}プログラムについて連絡する学生のためのプロフェッショナルなメール件名を生成してください。

メールタイプ: {email_type}
プログラム: {program_name}
大学: {university_name}
コーディネーター: {coordinator_name}""",
            'ko': f"""{university_name}의 {coordinator_name}에게 {program_name} 프로그램에 대해 연락하는 학생을 위한 전문적인 이메일 제목을 생성하세요.

이메일 유형: {email_type}
프로그램: {program_name}
대학교: {university_name}
코디네이터: {coordinator_name}""",
            'ar': f"""قم بإنشاء موضوع بريد إلكتروني مهني لطالب يتصل بـ {coordinator_name} في {university_name} بخصوص برنامج {program_name}.

نوع البريد الإلكتروني: {email_type}
البرنامج: {program_name}
الجامعة: {university_name}
المنسق: {coordinator_name}"""
        }
        
        prompt = language_prompts.get(language, language_prompts['en'])

        if student_profile:
            prompt += f"\nStudent background: {student_profile.get('background', 'Not specified')}"
            if student_profile.get('interests'):
                prompt += f"\nStudent interests: {student_profile.get('interests')}"

        # Language-specific requirements
        requirements = {
            'en': "\n\nRequirements:\n- Professional and concise (under 60 characters)\n- Specific to the program and university\n- Appropriate for academic communication\n- Clear and direct",
            'it': "\n\nRequisiti:\n- Professionale e conciso (sotto i 60 caratteri)\n- Specifico per il programma e l'università\n- Appropriato per la comunicazione accademica\n- Chiaro e diretto",
            'fr': "\n\nExigences:\n- Professionnel et concis (moins de 60 caractères)\n- Spécifique au programme et à l'université\n- Approprié pour la communication académique\n- Clair et direct",
            'es': "\n\nRequisitos:\n- Profesional y conciso (menos de 60 caracteres)\n- Específico para el programa y la universidad\n- Apropiado para comunicación académica\n- Claro y directo",
            'de': "\n\nAnforderungen:\n- Professionell und prägnant (unter 60 Zeichen)\n- Spezifisch für Programm und Universität\n- Angemessen für akademische Kommunikation\n- Klar und direkt",
            'pt': "\n\nRequisitos:\n- Profissional e conciso (menos de 60 caracteres)\n- Específico para o programa e universidade\n- Apropriado para comunicação acadêmica\n- Claro e direto",
            'nl': "\n\nVereisten:\n- Professioneel en beknopt (onder 60 tekens)\n- Specifiek voor programma en universiteit\n- Geschikt voor academische communicatie\n- Helder en direct",
            'ru': "\n\nТребования:\n- Профессионально и кратко (менее 60 символов)\n- Специфично для программы и университета\n- Подходяще для академического общения\n- Ясно и прямо",
            'zh': "\n\n要求:\n- 专业简洁（少于60个字符）\n- 针对项目和大学\n- 适合学术交流\n- 清晰直接",
            'ja': "\n\n要件:\n- プロフェッショナルで簡潔（60文字未満）\n- プログラムと大学に特化\n- 学術コミュニケーションに適切\n- 明確で直接的",
            'ko': "\n\n요구사항:\n- 전문적이고 간결함 (60자 미만)\n- 프로그램과 대학교에 특화\n- 학술 커뮤니케이션에 적합\n- 명확하고 직접적",
            'ar': "\n\nالمتطلبات:\n- مهني ومختصر (أقل من 60 حرف)\n- محدد للبرنامج والجامعة\n- مناسب للتواصل الأكاديمي\n- واضح ومباشر"
        }
        
        prompt += requirements.get(language, requirements['en'])

        return prompt
    
    def _build_content_prompt(self, program_name, university_name, coordinator_name, coordinator_role, email_type, student_profile, custom_requirements, language='en'):
        """Build the prompt for content generation"""
        # Language-specific prompts
        language_prompts = {
            'en': f"""Write a professional email for a student contacting {coordinator_name} ({coordinator_role}) at {university_name} about the {program_name} program.

Email type: {email_type}
Program: {program_name}
University: {university_name}
Coordinator: {coordinator_name} ({coordinator_role})""",
            'it': f"""Scrivi un'email professionale per uno studente che contatta {coordinator_name} ({coordinator_role}) presso {university_name} riguardo al programma {program_name}.

Tipo email: {email_type}
Programma: {program_name}
Università: {university_name}
Coordinatore: {coordinator_name} ({coordinator_role})""",
            'fr': f"""Écrivez un email professionnel pour un étudiant contactant {coordinator_name} ({coordinator_role}) à {university_name} concernant le programme {program_name}.

Type d'email: {email_type}
Programme: {program_name}
Université: {university_name}
Coordinateur: {coordinator_name} ({coordinator_role})""",
            'es': f"""Escribe un email profesional para un estudiante que contacta a {coordinator_name} ({coordinator_role}) en {university_name} sobre el programa {program_name}.

Tipo de email: {email_type}
Programa: {program_name}
Universidad: {university_name}
Coordinador: {coordinator_name} ({coordinator_role})""",
            'de': f"""Schreiben Sie eine professionelle E-Mail für einen Studenten, der {coordinator_name} ({coordinator_role}) an der {university_name} bezüglich des Programms {program_name} kontaktiert.

E-Mail-Typ: {email_type}
Programm: {program_name}
Universität: {university_name}
Koordinator: {coordinator_name} ({coordinator_role})""",
            'pt': f"""Escreva um email profissional para um estudante entrando em contato com {coordinator_name} ({coordinator_role}) na {university_name} sobre o programa {program_name}.

Tipo de email: {email_type}
Programa: {program_name}
Universidade: {university_name}
Coordenador: {coordinator_name} ({coordinator_role})""",
            'nl': f"""Schrijf een professionele email voor een student die {coordinator_name} ({coordinator_role}) bij {university_name} contacteert over het programma {program_name}.

Email type: {email_type}
Programma: {program_name}
Universiteit: {university_name}
Coördinator: {coordinator_name} ({coordinator_role})""",
            'ru': f"""Напишите профессиональное письмо для студента, обращающегося к {coordinator_name} ({coordinator_role}) в {university_name} по поводу программы {program_name}.

Тип письма: {email_type}
Программа: {program_name}
Университет: {university_name}
Координатор: {coordinator_name} ({coordinator_role})""",
            'zh': f"""为联系{university_name}的{coordinator_name}（{coordinator_role}）询问{program_name}项目的学生写一封专业邮件。

邮件类型: {email_type}
项目: {program_name}
大学: {university_name}
协调员: {coordinator_name} ({coordinator_role})""",
            'ja': f"""{university_name}の{coordinator_name}（{coordinator_role}）に{program_name}プログラムについて連絡する学生のためのプロフェッショナルなメールを書いてください。

メールタイプ: {email_type}
プログラム: {program_name}
大学: {university_name}
コーディネーター: {coordinator_name} ({coordinator_role})""",
            'ko': f"""{university_name}의 {coordinator_name}（{coordinator_role}）에게 {program_name} 프로그램에 대해 연락하는 학생을 위한 전문적인 이메일을 작성하세요.

이메일 유형: {email_type}
프로그램: {program_name}
대학교: {university_name}
코디네이터: {coordinator_name} ({coordinator_role})""",
            'ar': f"""اكتب بريد إلكتروني مهني لطالب يتصل بـ {coordinator_name} ({coordinator_role}) في {university_name} بخصوص برنامج {program_name}.

نوع البريد الإلكتروني: {email_type}
البرنامج: {program_name}
الجامعة: {university_name}
المنسق: {coordinator_name} ({coordinator_role})"""
        }
        
        prompt = language_prompts.get(language, language_prompts['en'])

        if student_profile:
            prompt += f"\nStudent background: {student_profile.get('background', 'Not specified')}"
            if student_profile.get('interests'):
                prompt += f"\nStudent interests: {student_profile.get('interests')}"
            if student_profile.get('experience'):
                prompt += f"\nStudent experience: {student_profile.get('experience')}"

        if custom_requirements:
            prompt += f"\nSpecific questions/requirements: {', '.join(custom_requirements)}"

        prompt += f"""

Requirements:
- Professional and respectful tone
- Demonstrate genuine interest in the program
- Be specific about what information you're seeking
- Mention relevant background/experience
- Keep it concise but informative
- Use proper academic email format
- Include greeting and closing
- Personalize based on the coordinator's role"""

        return prompt
    
    def _fallback_subject(self, program_name, university_name, email_type):
        """Fallback subject when AI generation fails"""
        return f"Inquiry about {program_name} at {university_name}"
    
    def _fallback_content(self, program_name, university_name, coordinator_name, email_type):
        """Fallback content when AI generation fails"""
        return f"""Dear {coordinator_name},

I hope this email finds you well. I am writing to inquire about the {program_name} program at {university_name}.

I am very interested in pursuing my master's degree in this field and would like to learn more about the program requirements, application process, and opportunities available.

I would greatly appreciate any information you could provide about the program.

Thank you for your time and consideration.

Best regards,
[Your Name]"""


# Convenience functions for easy integration
def get_email_suggestions(program_name: str, 
                          university_name: str, 
                          coordinator_name: str,
                          coordinator_role: str = 'coordinator',
                          email_type: str = 'inquiry',
                          student_profile: Optional[Dict] = None,
                          language: str = 'en') -> Dict[str, str]:
    """
    Get complete email suggestions (subject + content)
    
    Returns:
        Dictionary with 'subject' and 'content' keys
    """
    service = EmailSuggestionService()
    
    subject = service.generate_email_subject(
        program_name, university_name, coordinator_name, email_type, student_profile, language
    )
    
    content = service.generate_email_content(
        program_name, university_name, coordinator_name, coordinator_role, 
        email_type, student_profile, language
    )
    
    return {
        'subject': subject,
        'content': content
    }

def get_multiple_subject_options(program_name: str,
                                 university_name: str,
                                 coordinator_name: str,
                                 email_type: str = 'inquiry',
                                 count: int = 3) -> List[str]:
    """
    Get multiple subject line options
    
    Returns:
        List of subject line options
    """
    service = EmailSuggestionService()
    return service.generate_multiple_subjects(
        program_name, university_name, coordinator_name, email_type, count
    )