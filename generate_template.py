from docx import Document
from docx.shared import Pt, RGBColor

def create_template():
    doc = Document()
    
    # Title (Name)
    doc.add_heading('{{ personal_details.name }}', 0)
    
    # Contact Info
    p = doc.add_paragraph()
    p.add_run('Email: {{ personal_details.email }}').bold = True
    p.add_run(' | Phone: {{ personal_details.phone }}')
    
    # Optional Personal Details
    p.add_run('{% if personal_details.address %}\nAddress: {{ personal_details.address }}{% endif %}')
    
    p2 = doc.add_paragraph()
    p2.add_run('{% if personal_details.linkedin %}LinkedIn: {{ personal_details.linkedin }}{% endif %}')
    p2.add_run('{% if personal_details.github %} | GitHub: {{ personal_details.github }}{% endif %}')
    p2.add_run('{% if personal_details.portfolio %} | Portfolio: {{ personal_details.portfolio }}{% endif %}')
    
    # Summary
    doc.add_paragraph('{% if personal_details.summary %}')
    doc.add_heading('Professional Summary', level=1)
    doc.add_paragraph('{{ personal_details.summary }}')
    doc.add_paragraph('{% endif %}')
    
    # Skills
    doc.add_paragraph('{% if skills %}')
    doc.add_heading('Skills', level=1)
    doc.add_paragraph('{% for skill in skills %}{{ skill }}{% if not loop.last %}, {% endif %}{% endfor %}')
    doc.add_paragraph('{% endif %}')
    
    # Education
    doc.add_paragraph('{% if education %}')
    doc.add_heading('Education', level=1)
    doc.add_paragraph('{% for edu in education %}')
    doc.add_paragraph('{{ edu.degree }} - {{ edu.institution }}').bold = True
    doc.add_paragraph('{{ edu.year }}{% if edu.grade %} | {{ edu.grade }}{% endif %}')
    doc.add_paragraph('{% endfor %}')
    doc.add_paragraph('{% endif %}')
    
    # Experience
    doc.add_paragraph('{% if experience %}')
    doc.add_heading('Experience', level=1)
    doc.add_paragraph('{% for exp in experience %}')
    doc.add_paragraph('{{ exp.role }} at {{ exp.company }}').bold = True
    doc.add_paragraph('{{ exp.duration }}')
    doc.add_paragraph('{% for desc in exp.description %}- {{ desc }}\n{% endfor %}')
    doc.add_paragraph('{% endfor %}')
    doc.add_paragraph('{% endif %}')
    
    # Projects
    doc.add_paragraph('{% if projects %}')
    doc.add_heading('Projects', level=1)
    doc.add_paragraph('{% for proj in projects %}')
    doc.add_paragraph('{{ proj.name }}').bold = True
    doc.add_paragraph('{{ proj.description }}')
    doc.add_paragraph('Technologies: {% for tech in proj.technologies %}{{ tech }}{% if not loop.last %}, {% endif %}{% endfor %}')
    doc.add_paragraph('{% endfor %}')
    doc.add_paragraph('{% endif %}')
    
    # Custom Sections (Dynamic)
    doc.add_paragraph('{% for section in custom_sections %}')
    doc.add_heading('{{ section.title }}', level=1)
    doc.add_paragraph('{% for item in section.content %}- {{ item }}\n{% endfor %}')
    doc.add_paragraph('{% endfor %}')
    
    doc.save('templates/cv_template.docx')

if __name__ == "__main__":
    create_template()
