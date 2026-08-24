"""
Parses the plain-text profile fields (education / work experience / projects)
that the user types into Tkinter Text boxes into structured lists of dicts,
ready to be sent to n8n as JSON and dropped straight into the Jake's Resume
LaTeX template.

Input format (one entry per line, fields separated by ' ; '):

  Education line:
      Institution ; Location ; Degree ; Start - End

  Work experience line:
      Company ; Location ; Role ; Start - End ; bullet one | bullet two

  Project line:
      Project Title ; Tech Stack (comma-separated) ; Start - End ; bullet one | bullet two

Blank lines and lines starting with '#' are ignored, so the Text box can also
contain the instructional placeholder text without breaking parsing.
"""


def _split_line(line):
    return [part.strip() for part in line.split(';')]


def _split_bullets(raw):
    if not raw:
        return []
    return [b.strip() for b in raw.split('|') if b.strip()]


def _usable_lines(text):
    for raw_line in (text or '').splitlines():
        line = raw_line.strip()
        if not line or line.startswith('#'):
            continue
        yield line


def parse_education(text):
    """-> [{'institution','location','degree','dates'}]"""
    entries = []
    for line in _usable_lines(text):
        parts = _split_line(line)
        parts += [''] * (4 - len(parts))
        institution, location, degree, dates = parts[:4]
        if institution:
            entries.append({
                'institution': institution,
                'location': location,
                'degree': degree,
                'dates': dates
            })
    return entries


def parse_work_experience(text):
    """-> [{'company','location','role','dates','bullets':[...]}]"""
    entries = []
    for line in _usable_lines(text):
        parts = _split_line(line)
        parts += [''] * (5 - len(parts))
        company, location, role, dates, bullets_raw = parts[:5]
        if company:
            entries.append({
                'company': company,
                'location': location,
                'role': role,
                'dates': dates,
                'bullets': _split_bullets(bullets_raw)
            })
    return entries


def parse_projects(text):
    """-> [{'title','tech_stack','dates','bullets':[...]}]"""
    entries = []
    for line in _usable_lines(text):
        parts = _split_line(line)
        parts += [''] * (4 - len(parts))
        title, tech_stack, dates, bullets_raw = parts[:4]
        if title:
            entries.append({
                'title': title,
                'tech_stack': tech_stack,
                'dates': dates,
                'bullets': _split_bullets(bullets_raw)
            })
    return entries
