from typing import List, Optional
from pydantic import BaseModel, Field

class PersonalDetails(BaseModel):
    name: str = Field(..., description="Full name of the candidate")
    job_title: Optional[str] = Field(None, description="Current role or Applied Position (e.g. Software Engineer)")
    email: Optional[str] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    address: Optional[str] = Field(None, description="Physical address or Location")
    date_of_birth: Optional[str] = Field(None, description="Date of Birth")
    gender: Optional[str] = Field(None, description="Gender")
    linkedin: Optional[str] = Field(None, description="LinkedIn profile URL")
    github: Optional[str] = Field(None, description="GitHub profile URL")
    portfolio: Optional[str] = Field(None, description="Portfolio or Personal Website URL")
    summary: Optional[str] = Field(None, description="Professional summary")

class Education(BaseModel):
    degree: str = Field(..., description="Degree obtained")
    institution: str = Field(..., description="University or Institution name")
    year: Optional[str] = Field(None, description="Year of graduation")
    grade: Optional[str] = Field(None, description="Grade or GPA")

class Experience(BaseModel):
    role: str = Field(..., description="Job title")
    company: str = Field(..., description="Company name")
    duration: Optional[str] = Field(None, description="Duration of employment (e.g., 'Jan 2020 - Present')")
    description: List[str] = Field(default_factory=list, description="List of responsibilities or achievements")

class Project(BaseModel):
    name: str = Field(..., description="Project name")
    description: str = Field(..., description="Project description")
    technologies: List[str] = Field(default_factory=list, description="Technologies used")
    url: Optional[str] = Field(None, description="URL to the project or repository")

class CustomSection(BaseModel):
    title: str = Field(..., description="Title of the custom section (e.g., 'Awards', 'Certifications', 'Volunteering')")
    content: List[str] = Field(..., description="List of items or descriptions for this section")

class Tech6Project(BaseModel):
    """Specific schema for the 'Work Undertaken that Best Illustrates Capability' section"""
    name: str = Field(..., description="Name of assignment or project")
    year: str = Field(..., description="Year(s) of the project (e.g. '2021-2022')")
    location: str = Field(..., description="Location of the project (City, Country)")
    client: str = Field(..., description="Procuring Agency or Client Name")
    main_features: str = Field(..., description="Narrative description of project scope and features")
    positions_held: str = Field(..., description="Exact designation held during this project")
    activities: str = Field(..., description="Specific activities performed by the staff")

class Membership(BaseModel):
    society: str = Field(..., description="Name of the professional society")
    date: str = Field(..., description="Membership date (DD/MM/YYYY) or year")

class Training(BaseModel):
    title: str = Field(..., description="Training course title")
    start_date: str = Field(..., description="Start date")
    end_date: str = Field(..., description="End date")

class LanguageSkill(BaseModel):
    language: str = Field(..., description="Language name")
    proficiency: str = Field(..., description="Proficiency level (e.g. Excellent in speaking, reading, writing)")

class CVData(BaseModel):
    # Personal Details
    personal_details: PersonalDetails
    
    # TECH-6 Specific Header Info
    firm_name: Optional[str] = Field(None, description="Name of the Firm proposing the staff")
    proposed_position: Optional[str] = Field(None, description="Title of the position proposed for this assignment")
    nationality: Optional[str] = Field(None, description="Nationality")
    
    education: List[Education] = Field(default_factory=list)
    memberships: List[Membership] = Field(default_factory=list)
    training: List[Training] = Field(default_factory=list)
    countries_of_work: List[str] = Field(default_factory=list, description="List of countries where staff has worked")
    
    # Employment Record (Reverse Chronological)
    experience: List[Experience] = Field(default_factory=list) # Mapping employment_record to existing 'experience' field
    
    # CRITICAL: The single project selected for 'Best Illustrates Capability'
    representative_project: Optional[Tech6Project] = Field(None)
    
    projects: List[Project] = Field(default_factory=list)
    skills: List[str] = Field(default_factory=list, description="List of technical/soft skills")
    languages: List[LanguageSkill] = Field(default_factory=list, description="List of spoken languages with proficiency")
    custom_sections: List[CustomSection] = Field(default_factory=list, description="Any other sections found in the CV not covered above")
