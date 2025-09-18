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
                             student_profile: Optional[Dict] = None) -> str:
        """
        Generate an AI-powered email subject line
        
        Args:
            program_name: Name of the master's program
            university_name: Name of the university
            coordinator_name: Name of the coordinator
            email_type: Type of email (inquiry, admission, scholarship, etc.)
            student_profile: Optional student profile information
            
        Returns:
            Generated subject line
        """
        try:
            prompt = self._build_subject_prompt(
                program_name, university_name, coordinator_name, 
                email_type, student_profile
            )
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert academic communication assistant. Generate professional, concise email subject lines for students contacting university coordinators."},
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
                              custom_requirements: Optional[List[str]] = None) -> str:
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
            
        Returns:
            Generated email content
        """
        try:
            prompt = self._build_content_prompt(
                program_name, university_name, coordinator_name, 
                coordinator_role, email_type, student_profile, custom_requirements
            )
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert academic communication assistant. Generate professional, personalized email content for students contacting university coordinators. Be respectful, specific, and demonstrate genuine interest in the program."},
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
    
    def _build_subject_prompt(self, program_name, university_name, coordinator_name, email_type, student_profile):
        """Build the prompt for subject generation"""
        prompt = f"""Generate a professional email subject line for a student contacting {coordinator_name} at {university_name} about the {program_name} program.

Email type: {email_type}
Program: {program_name}
University: {university_name}
Coordinator: {coordinator_name}"""

        if student_profile:
            prompt += f"\nStudent background: {student_profile.get('background', 'Not specified')}"
            if student_profile.get('interests'):
                prompt += f"\nStudent interests: {student_profile.get('interests')}"

        prompt += "\n\nRequirements:\n- Professional and concise (under 60 characters)\n- Specific to the program and university\n- Appropriate for academic communication\n- Clear and direct"

        return prompt
    
    def _build_content_prompt(self, program_name, university_name, coordinator_name, coordinator_role, email_type, student_profile, custom_requirements):
        """Build the prompt for content generation"""
        prompt = f"""Write a professional email for a student contacting {coordinator_name} ({coordinator_role}) at {university_name} about the {program_name} program.

Email type: {email_type}
Program: {program_name}
University: {university_name}
Coordinator: {coordinator_name} ({coordinator_role})"""

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
                          student_profile: Optional[Dict] = None) -> Dict[str, str]:
    """
    Get complete email suggestions (subject + content)
    
    Returns:
        Dictionary with 'subject' and 'content' keys
    """
    service = EmailSuggestionService()
    
    subject = service.generate_email_subject(
        program_name, university_name, coordinator_name, email_type, student_profile
    )
    
    content = service.generate_email_content(
        program_name, university_name, coordinator_name, coordinator_role, 
        email_type, student_profile
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