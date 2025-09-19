"""
AI-powered email suggestion service for UniWorld platform.
This module provides intelligent email subject and content generation using Google Gemini.
"""

import google.generativeai as genai
from django.conf import settings
from typing import Dict, List, Optional
import logging
import json

logger = logging.getLogger(__name__)

class EmailSuggestionService:
    """Service for generating AI-powered email suggestions"""
    
    def __init__(self):
        """Initialize the Gemini client"""
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model_name = getattr(settings, 'GEMINI_MODEL', 'gemini-1.5-flash')
        self.model = genai.GenerativeModel(self.model_name)
        logger.info(f"Gemini client initialized with model: {self.model_name}")
        logger.info(f"Gemini API key configured: {bool(settings.GEMINI_API_KEY)}")
    
    def test_gemini_connection(self):
        """Test Gemini API connection"""
        try:
            logger.info("Testing Gemini API connection...")
            response = self.model.generate_content("Say hello in Italian.")
            result = response.text.strip()
            logger.info(f"Gemini test successful: {result}")
            return True
        except Exception as e:
            logger.error(f"Gemini test failed: {str(e)}")
            return False
    
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
            logger.info(f"Generating email subject in language: {language}")
            prompt = self._build_subject_prompt(
                program_name, university_name, coordinator_name, 
                email_type, student_profile, language
            )
            
            # Create a system message for Gemini
            full_prompt = f"You are an expert academic communication assistant. Generate professional, concise email subject lines for students contacting university coordinators. Respond in {language}.\n\n{prompt}"
            
            response = self.model.generate_content(full_prompt)
            return response.text.strip()
            
        except Exception as e:
            logger.error(f"Error generating email subject: {str(e)}")
            return self._fallback_subject(program_name, university_name, email_type, language)
    
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
            logger.info(f"Generating email content in language: {language}")
            
            prompt = self._build_content_prompt(
                program_name, university_name, coordinator_name, 
                coordinator_role, email_type, student_profile, custom_requirements, language
            )
            
            logger.info(f"Content prompt built, calling Gemini with language: {language}")
            logger.info(f"Prompt preview: {prompt[:200]}...")
            
            # Create a system message for Gemini
            full_prompt = f"You are an expert academic communication assistant. Generate professional, personalized email content for students contacting university coordinators. Be respectful, specific, and demonstrate genuine interest in the program. Respond in {language}.\n\n{prompt}"
            
            response = self.model.generate_content(full_prompt)
            content = response.text.strip()
            logger.info(f"Generated content (first 100 chars): {content[:100]}...")
            return content
            
        except Exception as e:
            logger.error(f"Error generating email content: {str(e)}")
            logger.error(f"Error type: {type(e).__name__}")
            logger.error(f"Error details: {str(e)}")
            return self._fallback_content(program_name, university_name, coordinator_name, email_type, language)
    
    def generate_multiple_subjects(self,
                                  program_name: str,
                                  university_name: str,
                                  coordinator_name: str,
                                  email_type: str = 'inquiry',
                                  count: int = 3,
                                  language: str = 'en') -> List[str]:
        """
        Generate multiple subject line options
        
        Args:
            program_name: Name of the master's program
            university_name: Name of the university
            coordinator_name: Name of the coordinator
            email_type: Type of email (inquiry, admission, scholarship, etc.)
            count: Number of subject options to generate
            language: Language code (en, it, fr, es, de, pt, nl, ru, zh, ja, ko, ar)
            
        Returns:
            List of generated subject lines
        """
        try:
            # Language-specific prompts
            language_prompts = {
                'en': f"""Generate {count} different professional email subject lines for a student contacting {coordinator_name} at {university_name} about the {program_name} program.

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

Return only the subject lines, one per line.""",
                'it': f"""Genera {count} diverse righe oggetto email professionali per uno studente che contatta {coordinator_name} presso {university_name} riguardo al programma {program_name}.

Tipo email: {email_type}
Programma: {program_name}
Università: {university_name}
Coordinatore: {coordinator_name}

Requisiti:
- Ogni oggetto deve essere unico e professionale
- Mantienili concisi (sotto i 60 caratteri)
- Rendili specifici per il programma e l'università
- Varia tono e approccio
- Un oggetto per riga

Restituisci solo le righe oggetto, una per riga.""",
                'fr': f"""Générez {count} différents objets d'email professionnels pour un étudiant contactant {coordinator_name} à {university_name} concernant le programme {program_name}.

Type d'email: {email_type}
Programme: {program_name}
Université: {university_name}
Coordinateur: {coordinator_name}

Exigences:
- Chaque objet doit être unique et professionnel
- Gardez-les concis (moins de 60 caractères)
- Rendez-les spécifiques au programme et à l'université
- Variez le ton et l'approche
- Un objet par ligne

Retournez seulement les objets, un par ligne.""",
                'es': f"""Genera {count} diferentes asuntos de email profesionales para un estudiante que contacta a {coordinator_name} en {university_name} sobre el programa {program_name}.

Tipo de email: {email_type}
Programa: {program_name}
Universidad: {university_name}
Coordinador: {coordinator_name}

Requisitos:
- Cada asunto debe ser único y profesional
- Manténlos concisos (menos de 60 caracteres)
- Hazlos específicos para el programa y la universidad
- Varía el tono y el enfoque
- Un asunto por línea

Devuelve solo los asuntos, uno por línea.""",
                'de': f"""Generieren Sie {count} verschiedene professionelle E-Mail-Betreffzeilen für einen Studenten, der {coordinator_name} an der {university_name} bezüglich des Programms {program_name} kontaktiert.

E-Mail-Typ: {email_type}
Programm: {program_name}
Universität: {university_name}
Koordinator: {coordinator_name}

Anforderungen:
- Jeder Betreff sollte einzigartig und professionell sein
- Halten Sie sie prägnant (unter 60 Zeichen)
- Machen Sie sie spezifisch für Programm und Universität
- Variieren Sie Ton und Ansatz
- Ein Betreff pro Zeile

Geben Sie nur die Betreffzeilen zurück, eine pro Zeile.""",
                'pt': f"""Gere {count} diferentes assuntos de email profissionais para um estudante entrando em contato com {coordinator_name} na {university_name} sobre o programa {program_name}.

Tipo de email: {email_type}
Programa: {program_name}
Universidade: {university_name}
Coordenador: {coordinator_name}

Requisitos:
- Cada assunto deve ser único e profissional
- Mantenha-os concisos (menos de 60 caracteres)
- Torne-os específicos para o programa e universidade
- Varie o tom e a abordagem
- Um assunto por linha

Retorne apenas os assuntos, um por linha.""",
                'nl': f"""Genereer {count} verschillende professionele email-onderwerpen voor een student die {coordinator_name} bij {university_name} contacteert over het programma {program_name}.

Email type: {email_type}
Programma: {program_name}
Universiteit: {university_name}
Coördinator: {coordinator_name}

Vereisten:
- Elk onderwerp moet uniek en professioneel zijn
- Houd ze beknopt (onder 60 tekens)
- Maak ze specifiek voor programma en universiteit
- Varieer toon en aanpak
- Eén onderwerp per regel

Geef alleen de onderwerpen terug, één per regel.""",
                'ru': f"""Создайте {count} различных профессиональных тем письма для студента, обращающегося к {coordinator_name} в {university_name} по поводу программы {program_name}.

Тип письма: {email_type}
Программа: {program_name}
Университет: {university_name}
Координатор: {coordinator_name}

Требования:
- Каждая тема должна быть уникальной и профессиональной
- Держите их краткими (менее 60 символов)
- Сделайте их специфичными для программы и университета
- Варьируйте тон и подход
- Одна тема на строку

Верните только темы, по одной на строку.""",
                'zh': f"""为联系{university_name}的{coordinator_name}询问{program_name}项目的学生生成{count}个不同的专业邮件主题。

邮件类型: {email_type}
项目: {program_name}
大学: {university_name}
协调员: {coordinator_name}

要求:
- 每个主题都应该独特且专业
- 保持简洁（少于60个字符）
- 针对项目和大学
- 变化语调和方式
- 每行一个主题

只返回主题，每行一个。""",
                'ja': f"""{university_name}の{coordinator_name}に{program_name}プログラムについて連絡する学生のための{count}個の異なるプロフェッショナルなメール件名を生成してください。

メールタイプ: {email_type}
プログラム: {program_name}
大学: {university_name}
コーディネーター: {coordinator_name}

要件:
- 各件名はユニークでプロフェッショナルである必要があります
- 簡潔に保つ（60文字未満）
- プログラムと大学に特化させる
- トーンとアプローチを変える
- 1行に1つの件名

件名のみを返し、1行に1つずつ。""",
                'ko': f"""{university_name}의 {coordinator_name}에게 {program_name} 프로그램에 대해 연락하는 학생을 위한 {count}개의 서로 다른 전문적인 이메일 제목을 생성하세요.

이메일 유형: {email_type}
프로그램: {program_name}
대학교: {university_name}
코디네이터: {coordinator_name}

요구사항:
- 각 제목은 고유하고 전문적이어야 합니다
- 간결하게 유지하세요 (60자 미만)
- 프로그램과 대학교에 특화시키세요
- 톤과 접근 방식을 다양화하세요
- 한 줄에 하나의 제목

제목만 반환하고, 한 줄에 하나씩.""",
                'ar': f"""قم بإنشاء {count} موضوعات بريد إلكتروني مهنية مختلفة لطالب يتصل بـ {coordinator_name} في {university_name} بخصوص برنامج {program_name}.

نوع البريد الإلكتروني: {email_type}
البرنامج: {program_name}
الجامعة: {university_name}
المنسق: {coordinator_name}

المتطلبات:
- يجب أن يكون كل موضوع فريداً ومهنياً
- اجعلها مختصرة (أقل من 60 حرف)
- اجعلها محددة للبرنامج والجامعة
- تنويع النبرة والنهج
- موضوع واحد في كل سطر

أرجع المواضيع فقط، واحد في كل سطر."""
            }
            
            prompt = language_prompts.get(language, language_prompts['en'])
            
            # Create a system message for Gemini
            full_prompt = f"You are an expert academic communication assistant. Generate multiple professional email subject line options. Respond in {language}.\n\n{prompt}"
            
            response = self.model.generate_content(full_prompt)
            subjects = response.text.strip().split('\n')
            return [subject.strip() for subject in subjects if subject.strip()]
            
        except Exception as e:
            logger.error(f"Error generating multiple subjects: {str(e)}")
            return [self._fallback_subject(program_name, university_name, email_type, language)]
    
    def enhance_email_content(self,
                            current_content: str,
                            program_name: str,
                            university_name: str,
                            coordinator_name: str,
                            coordinator_role: str,
                            enhancement_type: str = 'improve',
                            language: str = 'en') -> str:
        """
        Enhance existing email content with AI suggestions
        
        Args:
            current_content: The current email content
            program_name: Name of the master's program
            university_name: Name of the university
            coordinator_name: Name of the coordinator
            coordinator_role: Role of the coordinator
            enhancement_type: Type of enhancement (improve, personalize, shorten, expand)
            language: Language code (en, it, fr, es, de, pt, nl, ru, zh, ja, ko, ar)
            
        Returns:
            Enhanced email content
        """
        try:
            # Language-specific enhancement prompts
            enhancement_actions = {
                'en': {'improve': 'improve', 'personalize': 'personalize', 'shorten': 'shorten', 'expand': 'expand'},
                'it': {'improve': 'migliora', 'personalize': 'personalizza', 'shorten': 'accorcia', 'expand': 'espandi'},
                'fr': {'improve': 'améliore', 'personalize': 'personnalise', 'shorten': 'raccourcis', 'expand': 'étends'},
                'es': {'improve': 'mejora', 'personalize': 'personaliza', 'shorten': 'acorta', 'expand': 'expande'},
                'de': {'improve': 'verbessere', 'personalize': 'personalisieren', 'shorten': 'kürzen', 'expand': 'erweitern'},
                'pt': {'improve': 'melhore', 'personalize': 'personalize', 'shorten': 'encurte', 'expand': 'expanda'},
                'nl': {'improve': 'verbeter', 'personalize': 'personaliseer', 'shorten': 'verkort', 'expand': 'breid uit'},
                'ru': {'improve': 'улучши', 'personalize': 'персонализируй', 'shorten': 'сократи', 'expand': 'расширь'},
                'zh': {'improve': '改进', 'personalize': '个性化', 'shorten': '缩短', 'expand': '扩展'},
                'ja': {'improve': '改善', 'personalize': '個別化', 'shorten': '短縮', 'expand': '拡張'},
                'ko': {'improve': '개선', 'personalize': '개인화', 'shorten': '단축', 'expand': '확장'},
                'ar': {'improve': 'حسن', 'personalize': 'خصص', 'shorten': 'اقصر', 'expand': 'وسع'}
            }
            
            action = enhancement_actions.get(language, enhancement_actions['en']).get(enhancement_type, enhancement_type)
            
            language_prompts = {
                'en': f"""Please {action} the following email content for a student contacting {coordinator_name} ({coordinator_role}) at {university_name} about the {program_name} program.

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

Return only the enhanced email content.""",
                'it': f"""Per favore {action} il seguente contenuto email per uno studente che contatta {coordinator_name} ({coordinator_role}) presso {university_name} riguardo al programma {program_name}.

Contenuto attuale:
{current_content}

Tipo email: inquiry
Programma: {program_name}
Università: {university_name}
Coordinatore: {coordinator_name} ({coordinator_role})

Requisiti:
- Mantieni l'intento originale e i punti chiave
- Mantienilo professionale e rispettoso
- Rendilo più coinvolgente e personalizzato
- Assicura il formato email accademico corretto
- Mantieni lo stesso tono ma migliora chiarezza e impatto

Restituisci solo il contenuto email migliorato.""",
                'fr': f"""Veuillez {action} le contenu email suivant pour un étudiant contactant {coordinator_name} ({coordinator_role}) à {university_name} concernant le programme {program_name}.

Contenu actuel:
{current_content}

Type d'email: inquiry
Programme: {program_name}
Université: {university_name}
Coordinateur: {coordinator_name} ({coordinator_role})

Exigences:
- Maintenez l'intention originale et les points clés
- Gardez-le professionnel et respectueux
- Rendez-le plus engageant et personnalisé
- Assurez le format email académique approprié
- Gardez le même ton mais améliorez la clarté et l'impact

Retournez seulement le contenu email amélioré.""",
                'es': f"""Por favor {action} el siguiente contenido de email para un estudiante que contacta a {coordinator_name} ({coordinator_role}) en {university_name} sobre el programa {program_name}.

Contenido actual:
{current_content}

Tipo de email: inquiry
Programa: {program_name}
Universidad: {university_name}
Coordinador: {coordinator_name} ({coordinator_role})

Requisitos:
- Mantén la intención original y los puntos clave
- Manténlo profesional y respetuoso
- Hazlo más atractivo y personalizado
- Asegura el formato email académico apropiado
- Mantén el mismo tono pero mejora claridad e impacto

Devuelve solo el contenido email mejorado.""",
                'de': f"""Bitte {action} den folgenden E-Mail-Inhalt für einen Studenten, der {coordinator_name} ({coordinator_role}) an der {university_name} bezüglich des Programms {program_name} kontaktiert.

Aktueller Inhalt:
{current_content}

E-Mail-Typ: inquiry
Programm: {program_name}
Universität: {university_name}
Koordinator: {coordinator_name} ({coordinator_role})

Anforderungen:
- Behalten Sie die ursprüngliche Absicht und Schlüsselpunkte bei
- Halten Sie es professionell und respektvoll
- Machen Sie es ansprechender und personalisierter
- Stellen Sie das angemessene akademische E-Mail-Format sicher
- Behalten Sie den gleichen Ton bei, aber verbessern Sie Klarheit und Wirkung

Geben Sie nur den verbesserten E-Mail-Inhalt zurück.""",
                'pt': f"""Por favor {action} o seguinte conteúdo de email para um estudante entrando em contato com {coordinator_name} ({coordinator_role}) na {university_name} sobre o programa {program_name}.

Conteúdo atual:
{current_content}

Tipo de email: inquiry
Programa: {program_name}
Universidade: {university_name}
Coordenador: {coordinator_name} ({coordinator_role})

Requisitos:
- Mantenha a intenção original e pontos-chave
- Mantenha profissional e respeitoso
- Torne mais envolvente e personalizado
- Assegure o formato email acadêmico apropriado
- Mantenha o mesmo tom mas melhore clareza e impacto

Retorne apenas o conteúdo email melhorado.""",
                'nl': f"""Gelieve de volgende email-inhoud te {action} voor een student die {coordinator_name} ({coordinator_role}) bij {university_name} contacteert over het programma {program_name}.

Huidige inhoud:
{current_content}

Email type: inquiry
Programma: {program_name}
Universiteit: {university_name}
Coördinator: {coordinator_name} ({coordinator_role})

Vereisten:
- Behoud de oorspronkelijke bedoeling en kernpunten
- Houd het professioneel en respectvol
- Maak het boeiender en gepersonaliseerd
- Zorg voor het juiste academische email-formaat
- Behoud dezelfde toon maar verbeter duidelijkheid en impact

Geef alleen de verbeterde email-inhoud terug.""",
                'ru': f"""Пожалуйста, {action} следующее содержимое письма для студента, обращающегося к {coordinator_name} ({coordinator_role}) в {university_name} по поводу программы {program_name}.

Текущее содержимое:
{current_content}

Тип письма: inquiry
Программа: {program_name}
Университет: {university_name}
Координатор: {coordinator_name} ({coordinator_role})

Требования:
- Сохраните первоначальное намерение и ключевые моменты
- Сохраните профессиональность и уважение
- Сделайте более увлекательным и персонализированным
- Обеспечьте правильный академический формат письма
- Сохраните тот же тон, но улучшите ясность и воздействие

Верните только улучшенное содержимое письма.""",
                'zh': f"""请{action}以下学生联系{university_name}的{coordinator_name}（{coordinator_role}）关于{program_name}项目的邮件内容。

当前内容：
{current_content}

邮件类型: inquiry
项目: {program_name}
大学: {university_name}
协调员: {coordinator_name} ({coordinator_role})

要求:
- 保持原始意图和关键点
- 保持专业和尊重
- 使其更具吸引力和个性化
- 确保适当的学术邮件格式
- 保持相同的语调但提高清晰度和影响力

只返回改进的邮件内容。""",
                'ja': f"""{university_name}の{coordinator_name}（{coordinator_role}）に{program_name}プログラムについて連絡する学生の以下のメール内容を{action}してください。

現在の内容：
{current_content}

メールタイプ: inquiry
プログラム: {program_name}
大学: {university_name}
コーディネーター: {coordinator_name} ({coordinator_role})

要件:
- 元の意図とキーポイントを維持する
- プロフェッショナルで敬意を払う
- より魅力的で個人的にする
- 適切な学術メール形式を確保する
- 同じトーンを保つが、明確さと影響力を向上させる

改善されたメール内容のみを返してください。""",
                'ko': f"""{university_name}의 {coordinator_name}（{coordinator_role}）에게 {program_name} 프로그램에 대해 연락하는 학생의 다음 이메일 내용을 {action}해 주세요.

현재 내용:
{current_content}

이메일 유형: inquiry
프로그램: {program_name}
대학교: {university_name}
코디네이터: {coordinator_name} ({coordinator_role})

요구사항:
- 원래 의도와 핵심 포인트를 유지하세요
- 전문적이고 존중하는 태도를 유지하세요
- 더 매력적이고 개인화하세요
- 적절한 학술 이메일 형식을 보장하세요
- 같은 톤을 유지하되 명확성과 영향력을 개선하세요

개선된 이메일 내용만 반환하세요.""",
                'ar': f"""يرجى {action} محتوى البريد الإلكتروني التالي لطالب يتصل بـ {coordinator_name} ({coordinator_role}) في {university_name} بخصوص برنامج {program_name}.

المحتوى الحالي:
{current_content}

نوع البريد الإلكتروني: inquiry
البرنامج: {program_name}
الجامعة: {university_name}
المنسق: {coordinator_name} ({coordinator_role})

المتطلبات:
- احتفظ بالنية الأصلية والنقاط الرئيسية
- احتفظ بالمهنية والاحترام
- اجعله أكثر جاذبية وشخصية
- تأكد من تنسيق البريد الإلكتروني الأكاديمي المناسب
- احتفظ بنفس النبرة لكن حسّن الوضوح والتأثير

أرجع فقط المحتوى المحسن للبريد الإلكتروني."""
            }
            
            prompt = language_prompts.get(language, language_prompts['en'])
            
            # Create a system message for Gemini
            full_prompt = f"You are an expert academic communication assistant. Enhance email content while maintaining professionalism and the original intent. Respond in {language}.\n\n{prompt}"
            
            response = self.model.generate_content(full_prompt)
            return response.text.strip()
            
        except Exception as e:
            logger.error(f"Error enhancing email content: {str(e)}")
            return self._fallback_content(program_name, university_name, coordinator_name, 'inquiry', language)
    
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
        logger.info(f"Building content prompt for language: {language}")
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

        # Language-specific requirements
        requirements = {
            'en': """

Requirements:
- Professional and respectful tone
- Demonstrate genuine interest in the program
- Be specific about what information you're seeking
- Mention relevant background/experience
- Keep it concise but informative
- Use proper academic email format
- Include greeting and closing
- Personalize based on the coordinator's role""",
            'it': """

Requisiti:
- Tono professionale e rispettoso
- Dimostra genuino interesse per il programma
- Sii specifico su quali informazioni stai cercando
- Menziona background/esperienza rilevanti
- Mantienilo conciso ma informativo
- Usa il formato email accademico appropriato
- Includi saluto e chiusura
- Personalizza in base al ruolo del coordinatore""",
            'fr': """

Exigences:
- Ton professionnel et respectueux
- Démontrer un intérêt sincère pour le programme
- Être spécifique sur les informations recherchées
- Mentionner le background/expérience pertinents
- Garder concis mais informatif
- Utiliser le format email académique approprié
- Inclure salutation et fermeture
- Personnaliser selon le rôle du coordinateur""",
            'es': """

Requisitos:
- Tono profesional y respetuoso
- Demostrar interés genuino en el programa
- Ser específico sobre qué información buscas
- Mencionar background/experiencia relevante
- Mantener conciso pero informativo
- Usar formato email académico apropiado
- Incluir saludo y cierre
- Personalizar según el rol del coordinador""",
            'de': """

Anforderungen:
- Professioneller und respektvoller Ton
- Echtes Interesse am Programm demonstrieren
- Spezifisch sein über gesuchte Informationen
- Relevante Hintergrund/Erfahrung erwähnen
- Prägnant aber informativ halten
- Angemessenes akademisches E-Mail-Format verwenden
- Gruß und Abschluss einschließen
- Basierend auf der Rolle des Koordinators personalisieren""",
            'pt': """

Requisitos:
- Tom profissional e respeitoso
- Demonstrar interesse genuíno no programa
- Ser específico sobre que informações está buscando
- Mencionar background/experiência relevante
- Manter conciso mas informativo
- Usar formato email acadêmico apropriado
- Incluir saudação e fechamento
- Personalizar baseado no papel do coordenador""",
            'nl': """

Vereisten:
- Professionele en respectvolle toon
- Oprecht belangstelling voor het programma tonen
- Specifiek zijn over welke informatie je zoekt
- Relevante achtergrond/ervaring vermelden
- Beknopt maar informatief houden
- Geschikt academisch email-formaat gebruiken
- Begroeting en afsluiting opnemen
- Personaliseren op basis van de rol van de coördinator""",
            'ru': """

Требования:
- Профессиональный и уважительный тон
- Продемонстрировать искренний интерес к программе
- Быть конкретным в том, какую информацию вы ищете
- Упомянуть релевантный фон/опыт
- Держать кратким, но информативным
- Использовать подходящий академический формат письма
- Включить приветствие и закрытие
- Персонализировать на основе роли координатора""",
            'zh': """

要求:
- 专业和尊重的语调
- 表现出对项目的真正兴趣
- 具体说明你寻求的信息
- 提及相关的背景/经验
- 保持简洁但信息丰富
- 使用适当的学术邮件格式
- 包括问候和结尾
- 根据协调员的角色个性化""",
            'ja': """

要件:
- プロフェッショナルで敬意を払うトーン
- プログラムへの真の関心を示す
- 求めている情報について具体的に
- 関連する背景/経験に言及
- 簡潔だが情報豊富に保つ
- 適切な学術メール形式を使用
- 挨拶と結びを含める
- コーディネーターの役割に基づいて個人化""",
            'ko': """

요구사항:
- 전문적이고 존중하는 톤
- 프로그램에 대한 진정한 관심을 보여주세요
- 찾고 있는 정보에 대해 구체적으로
- 관련 배경/경험을 언급하세요
- 간결하지만 정보가 풍부하게 유지하세요
- 적절한 학술 이메일 형식을 사용하세요
- 인사와 마무리를 포함하세요
- 코디네이터의 역할에 따라 개인화하세요""",
            'ar': """

المتطلبات:
- نبرة مهنية ومحترمة
- أظهر اهتماماً حقيقياً بالبرنامج
- كن محدداً حول المعلومات التي تبحث عنها
- اذكر الخلفية/التجربة ذات الصلة
- اجعلها مختصرة ولكن مفيدة
- استخدم تنسيق البريد الإلكتروني الأكاديمي المناسب
- أدرج التحية والختام
- خصص بناءً على دور المنسق"""
        }

        prompt += requirements.get(language, requirements['en'])

        return prompt
    
    def _fallback_subject(self, program_name, university_name, email_type, language='en'):
        """Fallback subject when AI generation fails"""
        fallback_subjects = {
            'en': f"Inquiry about {program_name} at {university_name}",
            'it': f"Richiesta informazioni sul programma {program_name} presso {university_name}",
            'fr': f"Demande d'informations sur le programme {program_name} à {university_name}",
            'es': f"Consulta sobre el programa {program_name} en {university_name}",
            'de': f"Anfrage zum Programm {program_name} an der {university_name}",
            'pt': f"Consulta sobre o programa {program_name} na {university_name}",
            'nl': f"Vraag over het programma {program_name} aan {university_name}",
            'ru': f"Запрос о программе {program_name} в {university_name}",
            'zh': f"关于{university_name}的{program_name}项目咨询",
            'ja': f"{university_name}の{program_name}プログラムについての問い合わせ",
            'ko': f"{university_name}의 {program_name} 프로그램 문의",
            'ar': f"استفسار حول برنامج {program_name} في {university_name}"
        }
        return fallback_subjects.get(language, fallback_subjects['en'])
    
    def _fallback_content(self, program_name, university_name, coordinator_name, email_type, language='en'):
        """Fallback content when AI generation fails"""
        fallback_contents = {
            'en': f"""Dear {coordinator_name},

I hope this email finds you well. I am writing to inquire about the {program_name} program at {university_name}.

I am very interested in pursuing my master's degree in this field and would like to learn more about the program requirements, application process, and opportunities available.

I would greatly appreciate any information you could provide about the program.

Thank you for your time and consideration.

Best regards,
[Your Name]""",
            'it': f"""Gentile {coordinator_name},

Spero che questa email la trovi bene. Le scrivo per chiedere informazioni sul programma {program_name} presso {university_name}.

Sono molto interessato a perseguire il mio master in questo campo e vorrei saperne di più sui requisiti del programma, il processo di ammissione e le opportunità disponibili.

Apprezzerei molto qualsiasi informazione che potesse fornirmi sul programma.

Grazie per il suo tempo e la sua considerazione.

Cordiali saluti,
[Il Suo Nome]""",
            'fr': f"""Cher {coordinator_name},

J'espère que cet email vous trouve en bonne santé. Je vous écris pour demander des informations sur le programme {program_name} à {university_name}.

Je suis très intéressé par la poursuite de mon master dans ce domaine et j'aimerais en savoir plus sur les exigences du programme, le processus d'admission et les opportunités disponibles.

J'apprécierais grandement toute information que vous pourriez me fournir sur le programme.

Merci pour votre temps et votre considération.

Cordialement,
[Votre Nom]""",
            'es': f"""Estimado {coordinator_name},

Espero que este correo le encuentre bien. Le escribo para solicitar información sobre el programa {program_name} en {university_name}.

Estoy muy interesado en cursar mi maestría en este campo y me gustaría saber más sobre los requisitos del programa, el proceso de admisión y las oportunidades disponibles.

Agradecería mucho cualquier información que pudiera proporcionarme sobre el programa.

Gracias por su tiempo y consideración.

Atentamente,
[Su Nombre]""",
            'de': f"""Lieber {coordinator_name},

Ich hoffe, diese E-Mail erreicht Sie gut. Ich schreibe Ihnen, um mich über das Programm {program_name} an der {university_name} zu erkundigen.

Ich bin sehr interessiert daran, meinen Master in diesem Bereich zu verfolgen und würde gerne mehr über die Programmvoraussetzungen, den Bewerbungsprozess und die verfügbaren Möglichkeiten erfahren.

Ich würde mich sehr über alle Informationen freuen, die Sie mir über das Programm geben könnten.

Vielen Dank für Ihre Zeit und Ihr Interesse.

Mit freundlichen Grüßen,
[Ihr Name]""",
            'pt': f"""Caro {coordinator_name},

Espero que este email o encontre bem. Escrevo-lhe para solicitar informações sobre o programa {program_name} na {university_name}.

Estou muito interessado em prosseguir o meu mestrado nesta área e gostaria de saber mais sobre os requisitos do programa, processo de admissão e oportunidades disponíveis.

Agradeceria muito qualquer informação que pudesse fornecer sobre o programa.

Obrigado pelo seu tempo e consideração.

Atenciosamente,
[Seu Nome]""",
            'nl': f"""Beste {coordinator_name},

Ik hoop dat deze email u goed bereikt. Ik schrijf u om informatie te vragen over het programma {program_name} aan {university_name}.

Ik ben zeer geïnteresseerd in het volgen van mijn master in dit veld en zou graag meer willen weten over de programmavoorschriften, het toelatingsproces en de beschikbare mogelijkheden.

Ik zou het zeer op prijs stellen als u mij informatie over het programma zou kunnen verstrekken.

Bedankt voor uw tijd en aandacht.

Met vriendelijke groet,
[Uw Naam]""",
            'ru': f"""Уважаемый {coordinator_name},

Надеюсь, это письмо застанет Вас в добром здравии. Пишу Вам, чтобы узнать информацию о программе {program_name} в {university_name}.

Я очень заинтересован в получении степени магистра в этой области и хотел бы узнать больше о требованиях программы, процессе поступления и доступных возможностях.

Я был бы очень благодарен за любую информацию, которую Вы могли бы предоставить о программе.

Спасибо за Ваше время и внимание.

С уважением,
[Ваше Имя]""",
            'zh': f"""尊敬的{coordinator_name}，

希望这封邮件能够顺利送达。我写信是想咨询{university_name}的{program_name}项目。

我对在这个领域攻读硕士学位非常感兴趣，希望了解更多关于项目要求、申请流程和可用机会的信息。

如果您能提供任何关于该项目的信息，我将非常感激。

感谢您的时间和考虑。

此致敬礼，
[您的姓名]""",
            'ja': f"""{coordinator_name}様

このメールがお元気でお過ごしのところに届くことを願っています。{university_name}の{program_name}プログラムについてお尋ねしたく、ご連絡いたします。

この分野で修士号を取得することに大変興味があり、プログラムの要件、入学プロセス、利用可能な機会についてもっと知りたいと思っています。

プログラムについてご提供いただける情報があれば、大変ありがたく存じます。

お時間とご配慮をいただき、ありがとうございます。

敬具
[お名前]""",
            'ko': f"""{coordinator_name}님께

이 이메일이 잘 전달되기를 바랍니다. {university_name}의 {program_name} 프로그램에 대해 문의드리고자 연락드립니다.

이 분야에서 석사 학위를 취득하는 것에 매우 관심이 있으며, 프로그램 요구사항, 입학 과정, 이용 가능한 기회에 대해 더 알고 싶습니다.

프로그램에 대해 제공해 주실 수 있는 정보가 있다면 매우 감사하겠습니다.

시간을 내어 주시고 배려해 주셔서 감사합니다.

진심으로,
[귀하의 이름]""",
            'ar': f"""عزيزي {coordinator_name}،

أتمنى أن تجدك هذه الرسالة بخير. أكتب إليك للاستفسار عن برنامج {program_name} في {university_name}.

أنا مهتم جداً بمتابعة درجة الماجستير في هذا المجال وأود معرفة المزيد عن متطلبات البرنامج وعملية القبول والفرص المتاحة.

سأكون ممتناً جداً لأي معلومات يمكنك تقديمها حول البرنامج.

شكراً لك على وقتك واهتمامك.

مع أطيب التحيات،
[اسمك]"""
        }
        return fallback_contents.get(language, fallback_contents['en'])


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
                                 count: int = 3,
                                 language: str = 'en') -> List[str]:
    """
    Get multiple subject line options
    
    Returns:
        List of subject line options
    """
    service = EmailSuggestionService()
    return service.generate_multiple_subjects(
        program_name, university_name, coordinator_name, email_type, count, language
    )