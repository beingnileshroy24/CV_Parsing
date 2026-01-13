from docx import Document
from docx.shared import Pt, RGBColor

def create_template():
    doc = Document()
    
    # Title (Name)
    h1 = doc.add_heading('{{ personal_details.name }}', 0)
    
    # Contact Info
    p = doc.add_paragraph()
    p.add_run('Email: {{ personal_details.email }} | Phone: {{ personal_details.phone }} | LinkedIn: {{ personal_details.linkedin }}')
    
    # Summary
    doc.add_heading('Professional Summary', level=1)
    doc.add_paragraph('{{ personal_details.summary }}')
    
    # Skills
    doc.add_heading('Skills', level=1)
    doc.add_paragraph('{% for skill in skills %}{{ skill }}{% if not loop.last %}, {% endif %}{% endfor %}')
    
    # Education
    doc.add_heading('Education', level=1)
    # Loop for education
    p = doc.add_paragraph()
    p.add_run('{% for edu in education %}')
    p.add_run('{{ edu.degree }} - {{ edu.institution }}').bold = True
    p.add_run('\n{{ edu.year }} | {{ edu.grade }}')
    p.add_run('\n\n{% endfor %}')
    
    # Experience
    doc.add_heading('Experience', level=1)
    # Loop for experience
    p = doc.add_paragraph()
    p.add_run('{% for exp in experience %}')
    p.add_run('{{ exp.role }} at {{ exp.company }}').bold = True
    p.add_run('\n{{ exp.duration }}')
    p.add_run('\n{% for desc in exp.description %}- {{ desc }}\n{% endfor %}')
    p.add_run('\n{% endfor %}')
    
    # Projects
    doc.add_heading('Projects', level=1)
    p = doc.add_paragraph()
    p.add_run('{% for proj in projects %}')
    p.add_run('{{ proj.name }}').bold = True
    p.add_run(' - {{ proj.description }}')
    p.add_run('\nTechnologies: {% for tech in proj.technologies %}{{ tech }}{% if not loop.last %}, {% endif %}{% endfor %}')
    p.add_run('\n\n{% endfor %}')

    # Custom Sections (Dynamic)
    doc.add_paragraph('{% for section in custom_sections %}')
    doc.add_heading('{{ section.title }}', level=1)
    doc.add_paragraph('{% for item in section.content %}- {{ item }}\n{% endfor %}')
    doc.add_paragraph('{% endfor %}')
    
    doc.save('templates/cv_template.docx')

if __name__ == "__main__":
    create_template()
