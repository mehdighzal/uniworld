"""
AI-powered email templates for UniWorld platform.
This module provides intelligent email template generation.
"""

import openai
from django.conf import settings
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class AITemplateGenerator:
    """Service for generating AI-powered email templates"""
    
    def __init__(self):
        """Initialize the OpenAI client"""
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = getattr(settings, 'OPENAI_MODEL', 'gpt-3.5-turbo')
    
    def generate_dynamic_template(self,
                                 template_type: str,
                                 program_name: str,
                                 university_name: str,
                                 coordinator_name: str,
                                 coordinator_role: str,
                                 student_profile: Optional[Dict] = None) -> Dict[str, str]:
        """
        Generate AI-powered email template
        
        Args:
            template_type: Type of template (inquiry, admission, scholarship, etc.)
            program_name: Name of the master's program
            university_name: Name of the university
            coordinator_name: Name of the coordinator
            coordinator_role: Role of the coordinator
            student_profile: Optional student profile information
            
        Returns:
            Dictionary with template information
        """
        try:
            prompt = self._build_template_prompt(
                template_type, program_name, university_name,
                coordinator_name, coordinator_role, student_profile
            )
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert academic communication assistant. Generate professional, personalized email templates for students contacting university coordinators."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            template_content = response.choices[0].message.content.strip()
            
            return {
                'type': template_type,
                'subject': self._extract_subject(template_content),
                'content': template_content,
                'program_info': {
                    'name': program_name,
                    'university': university_name
                },
                'coordinator_info': {
                    'name': coordinator_name,
                    'role': coordinator_role
                }
            }
            
        except openai.RateLimitError as e:
            logger.warning(f"OpenAI rate limit exceeded, using fallback: {str(e)}")
            return self._get_fallback_template(template_type, program_name, university_name, coordinator_name)
        except openai.APIError as e:
            logger.warning(f"OpenAI API error, using fallback: {str(e)}")
            return self._get_fallback_template(template_type, program_name, university_name, coordinator_name)
        except Exception as e:
            # Fallback to static template
            return self._get_fallback_template(template_type, program_name, university_name, coordinator_name)
    
    def generate_multiple_templates(self,
                                  program_name: str,
                                  university_name: str,
                                  coordinator_name: str,
                                  coordinator_role: str,
                                  template_types: List[str] = None,
                                  student_profile: Optional[Dict] = None) -> List[Dict[str, str]]:
        """
        Generate multiple template options
        
        Args:
            program_name: Name of the master's program
            university_name: Name of the university
            coordinator_name: Name of the coordinator
            coordinator_role: Role of the coordinator
            template_types: List of template types to generate
            student_profile: Optional student profile information
            
        Returns:
            List of template dictionaries
        """
        if template_types is None:
            template_types = ['inquiry', 'admission', 'scholarship']
        
        templates = []
        for template_type in template_types:
            try:
                template = self.generate_dynamic_template(
                    template_type, program_name, university_name,
                    coordinator_name, coordinator_role, student_profile
                )
                templates.append(template)
            except openai.RateLimitError as e:
                logger.warning(f"OpenAI rate limit exceeded, using fallback: {str(e)}")
                # Add fallback template
                fallback = self._get_fallback_template(
                    template_type, program_name, university_name, coordinator_name
                )
                templates.append(fallback)
            except openai.APIError as e:
                logger.warning(f"OpenAI API error, using fallback: {str(e)}")
                # Add fallback template
                fallback = self._get_fallback_template(
                    template_type, program_name, university_name, coordinator_name
                )
                templates.append(fallback)
            except Exception as e:
                # Add fallback template
                fallback = self._get_fallback_template(
                    template_type, program_name, university_name, coordinator_name
                )
                templates.append(fallback)
        
        return templates
    
    def _get_fallback_template(self, template_type: str, program_name: str, university_name: str, coordinator_name: str) -> Dict[str, str]:
        """Get fallback template when AI generation fails"""
        
        templates = {
            'inquiry': {
                'subject': f"Inquiry about {program_name} at {university_name}",
                'content': f"""Dear {coordinator_name},

I hope this email finds you well. I am writing to inquire about the {program_name} program at {university_name}.

I am very interested in pursuing my master's degree in this field and would like to learn more about the program requirements, application process, and opportunities available.

I would greatly appreciate any information you could provide about the program.

Thank you for your time and consideration.

Best regards,
[Your Name]"""
            },
            'admission': {
                'subject': f"Admission Inquiry - {program_name}",
                'content': f"""Dear {coordinator_name},

I hope this email finds you well. I am writing to inquire about the admission process for the {program_name} program at {university_name}.

I am very interested in applying for this program and would like to understand the admission requirements, application deadlines, and selection criteria.

Could you please provide information about:
- Application requirements
- Required documents
- Application deadlines
- Selection process
- Any specific prerequisites

I would greatly appreciate your guidance on the admission process.

Thank you for your time and consideration.

Best regards,
[Your Name]"""
            },
            'scholarship': {
                'subject': f"Scholarship Inquiry - {program_name}",
                'content': f"""Dear {coordinator_name},

I hope this email finds you well. I am writing to inquire about scholarship opportunities for the {program_name} program at {university_name}.

I am very interested in pursuing this program and would like to learn about available funding options and scholarship opportunities.

Could you please provide information about:
- Available scholarships
- Application requirements
- Application deadlines
- Selection criteria
- Funding amounts

I would greatly appreciate any information about financial aid opportunities.

Thank you for your time and consideration.

Best regards,
[Your Name]"""
            },
            'research': {
                'subject': f"Research Opportunities - {program_name}",
                'content': f"""Dear {coordinator_name},

I hope this email finds you well. I am writing to inquire about research opportunities within the {program_name} program at {university_name}.

I am very interested in pursuing research in this field and would like to learn about available research projects and opportunities.

Could you please provide information about:
- Current research projects
- Research opportunities for students
- How to get involved in research
- Research requirements
- Available supervisors

I would greatly appreciate any information about research opportunities.

Thank you for your time and consideration.

Best regards,
[Your Name]"""
            },
            'career': {
                'subject': f"Career Opportunities - {program_name}",
                'content': f"""Dear {coordinator_name},

I hope this email finds you well. I am writing to inquire about career opportunities and outcomes for graduates of the {program_name} program at {university_name}.

I am very interested in this program and would like to understand the career prospects and opportunities available to graduates.

Could you please provide information about:
- Career outcomes for graduates
- Employment statistics
- Industry connections
- Career support services
- Alumni network

I would greatly appreciate any information about career opportunities.

Thank you for your time and consideration.

Best regards,
[Your Name]"""
            }
        }
        
        return {
            'type': template_type,
            'subject': templates.get(template_type, templates['inquiry'])['subject'],
            'content': templates.get(template_type, templates['inquiry'])['content'],
            'program_info': {
                'name': program_name,
                'university': university_name
            },
            'coordinator_info': {
                'name': coordinator_name,
                'role': 'Coordinator'
            }
        }
    
    def _build_template_prompt(self, template_type, program_name, university_name, coordinator_name, coordinator_role, student_profile):
        """Build the prompt for template generation"""
        
        prompts = {
            'inquiry': f"""Write a professional inquiry email for a student contacting {coordinator_name} ({coordinator_role}) at {university_name} about the {program_name} program.

The email should:
- Express genuine interest in the program
- Ask for general information about the program
- Be professional and respectful
- Include proper greeting and closing
- Be specific about what information is being sought""",
            
            'admission': f"""Write a professional admission inquiry email for a student contacting {coordinator_name} ({coordinator_role}) at {university_name} about the {program_name} program.

The email should:
- Focus on admission requirements and process
- Ask about application deadlines and requirements
- Be professional and respectful
- Include proper greeting and closing
- Show preparedness and seriousness about applying""",
            
            'scholarship': f"""Write a professional scholarship inquiry email for a student contacting {coordinator_name} ({coordinator_role}) at {university_name} about the {program_name} program.

The email should:
- Focus on funding and scholarship opportunities
- Ask about available financial aid
- Be professional and respectful
- Include proper greeting and closing
- Show genuine need and interest in funding""",
            
            'research': f"""Write a professional research inquiry email for a student contacting {coordinator_name} ({coordinator_role}) at {university_name} about the {program_name} program.

The email should:
- Focus on research opportunities and projects
- Ask about current research activities
- Be professional and respectful
- Include proper greeting and closing
- Show academic interest and research potential""",
            
            'career': f"""Write a professional career inquiry email for a student contacting {coordinator_name} ({coordinator_role}) at {university_name} about the {program_name} program.

The email should:
- Focus on career outcomes and opportunities
- Ask about employment prospects and statistics
- Be professional and respectful
- Include proper greeting and closing
- Show career-focused mindset"""
        }
        
        base_prompt = prompts.get(template_type, prompts['inquiry'])
        
        if student_profile:
            base_prompt += f"\n\nStudent background: {student_profile.get('background', 'Not specified')}"
            if student_profile.get('interests'):
                base_prompt += f"\nStudent interests: {student_profile.get('interests')}"
            if student_profile.get('experience'):
                base_prompt += f"\nStudent experience: {student_profile.get('experience')}"
        
        base_prompt += f"""

Requirements:
- Professional and respectful tone
- Specific to the {template_type} context
- Personalized for {coordinator_name} and {program_name}
- Include a clear subject line
- Use proper academic email format
- Keep it concise but informative"""

        return base_prompt
    
    def _extract_subject(self, content: str) -> str:
        """Extract subject line from email content"""
        lines = content.split('\n')
        for line in lines:
            if line.strip().startswith('Subject:') or line.strip().startswith('Re:'):
                return line.strip().replace('Subject:', '').replace('Re:', '').strip()
        return "Email Inquiry"


# Convenience functions for easy integration
def get_ai_template(template_type: str,
                   program_name: str,
                   university_name: str,
                   coordinator_name: str,
                   coordinator_role: str = 'coordinator',
                   student_profile: Optional[Dict] = None) -> Dict[str, str]:
    """
    Get AI-powered email template
    
    Returns:
        Dictionary with template information
    """
    generator = AITemplateGenerator()
    return generator.generate_dynamic_template(
        template_type, program_name, university_name,
        coordinator_name, coordinator_role, student_profile
    )

def get_multiple_ai_templates(program_name: str,
                             university_name: str,
                             coordinator_name: str,
                             coordinator_role: str = 'coordinator',
                             template_types: List[str] = None,
                             student_profile: Optional[Dict] = None) -> List[Dict[str, str]]:
    """
    Get multiple AI-powered email templates
    
    Returns:
        List of template dictionaries
    """
    generator = AITemplateGenerator()
    return generator.generate_multiple_templates(
        program_name, university_name, coordinator_name,
        coordinator_role, template_types, student_profile
    )

def get_template_categories() -> Dict[str, List[Dict[str, str]]]:
    """
    Get template categories with sample templates
    
    Returns:
        Dictionary with template categories
    """
    return {
        'inquiry': [
            {'type': 'inquiry', 'name': 'General Inquiry', 'description': 'Ask for general program information'},
            {'type': 'admission', 'name': 'Admission Inquiry', 'description': 'Ask about admission requirements'},
            {'type': 'scholarship', 'name': 'Scholarship Inquiry', 'description': 'Ask about funding opportunities'},
        ],
        'admission': [
            {'type': 'admission', 'name': 'Admission Requirements', 'description': 'Ask about specific admission criteria'},
            {'type': 'admission', 'name': 'Application Process', 'description': 'Ask about application procedures'},
            {'type': 'admission', 'name': 'Deadlines', 'description': 'Ask about important dates'},
        ],
        'scholarship': [
            {'type': 'scholarship', 'name': 'Funding Options', 'description': 'Ask about available funding'},
            {'type': 'scholarship', 'name': 'Scholarship Application', 'description': 'Ask about scholarship process'},
            {'type': 'scholarship', 'name': 'Financial Aid', 'description': 'Ask about financial assistance'},
        ],
        'research': [
            {'type': 'research', 'name': 'Research Projects', 'description': 'Ask about current research'},
            {'type': 'research', 'name': 'Research Opportunities', 'description': 'Ask about research involvement'},
            {'type': 'research', 'name': 'Supervisors', 'description': 'Ask about research supervision'},
        ],
        'career': [
            {'type': 'career', 'name': 'Career Outcomes', 'description': 'Ask about graduate employment'},
            {'type': 'career', 'name': 'Industry Connections', 'description': 'Ask about industry partnerships'},
            {'type': 'career', 'name': 'Career Support', 'description': 'Ask about career services'},
        ]
    }