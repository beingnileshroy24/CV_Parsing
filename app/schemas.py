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

class CVData(BaseModel):
    personal_details: PersonalDetails
    education: List[Education] = Field(default_factory=list)
    experience: List[Experience] = Field(default_factory=list)
    projects: List[Project] = Field(default_factory=list)
    skills: List[str] = Field(default_factory=list, description="List of technical/soft skills")
    languages: List[str] = Field(default_factory=list, description="List of spoken languages")
    custom_sections: List[CustomSection] = Field(default_factory=list, description="Any other sections found in the CV not covered above")
