/**
 * Paste this into an n8n "Code" node (Run Once for Each Item, JavaScript).
 * It runs AFTER the Google Gemini node in the workflow, and BEFORE the
 * HTTP Request node that compiles LaTeX -> PDF.
 *
 * Expects on the current item:
 *   $('Webhook').item.json.body.user  -> { first_name, last_name, email,
 *       location, education[], work_experience[], projects[] }   (raw, from Python)
 *   $json.gemini  -> the JSON object Gemini returned (see gemini_resume_prompt.md):
 *       { work_experience: [{ bullets:[...] }, ...] (same order as input),
 *         projects:        [{ bullets:[...] }, ...] (same order as input) }
 *
 * Outputs: { latex: "<full .tex source, ready to POST to the PDF compiler>" }
 */

function escapeLatex(str) {
  if (!str) return '';
  return String(str)
    .replace(/\\/g, '\\textbackslash{}')
    .replace(/&/g, '\\&')
    .replace(/%/g, '\\%')
    .replace(/\$/g, '\\$')
    .replace(/#/g, '\\#')
    .replace(/_/g, '\\_')
    .replace(/\{/g, '\\{')
    .replace(/\}/g, '\\}')
    .replace(/~/g, '\\textasciitilde{}')
    .replace(/\^/g, '\\textasciicircum{}');
}

const user = $('Webhook').item.json.body.user;
const gemini = $json.gemini || {};

// Gemini polishes bullet text only — dates/company/titles/tech stack stay
// exactly as the user typed them, so nothing gets hallucinated.
const polishedExperience = (user.work_experience || []).map((entry, i) => ({
  ...entry,
  bullets: (gemini.work_experience && gemini.work_experience[i] && gemini.work_experience[i].bullets)
    || entry.bullets
}));

const polishedProjects = (user.projects || []).map((entry, i) => ({
  ...entry,
  bullets: (gemini.projects && gemini.projects[i] && gemini.projects[i].bullets)
    || entry.bullets
}));

const educationBlock = (user.education || []).map(e => `
    \\resumeSubheading
      {${escapeLatex(e.institution)}}{${escapeLatex(e.location)}}
      {${escapeLatex(e.degree)}}{${escapeLatex(e.dates)}}`).join('\n');

const experienceBlock = polishedExperience.map(e => `
    \\resumeSubheading
      {${escapeLatex(e.role)}}{${escapeLatex(e.dates)}}
      {${escapeLatex(e.company)}}{${escapeLatex(e.location)}}
      \\resumeItemListStart
        ${e.bullets.map(b => `\\resumeItem{${escapeLatex(b)}}`).join('\n        ')}
      \\resumeItemListEnd`).join('\n');

const projectsBlock = polishedProjects.map(p => `
      \\resumeProjectHeading
          {\\textbf{${escapeLatex(p.title)}} $|$ \\emph{${escapeLatex(p.tech_stack)}}}{${escapeLatex(p.dates)}}
          \\resumeItemListStart
            ${p.bullets.map(b => `\\resumeItem{${escapeLatex(b)}}`).join('\n            ')}
          \\resumeItemListEnd`).join('\n');

// Technical Skills — reuse the same comma-separated skills string the
// Random Forest model matched on, so the resume and the ML matching
// always agree on what the candidate knows.
const skillsLine = escapeLatex((user.skills || []).join(', '));

const latex = `%-------------------------
% Resume in LaTeX — generated automatically, based on the Jake's Resume
% template (MIT License): https://github.com/jakeryang/resume
%------------------------
\\documentclass[letterpaper,11pt]{article}

\\usepackage{latexsym}
\\usepackage[empty]{fullpage}
\\usepackage{titlesec}
\\usepackage{marvosym}
\\usepackage[usenames,dvipsnames]{color}
\\usepackage{verbatim}
\\usepackage{enumitem}
\\usepackage[hidelinks]{hyperref}
\\usepackage{fancyhdr}
\\usepackage[english]{babel}
\\usepackage{tabularx}
\\input{glyphtounicode}

\\pagestyle{fancy}
\\fancyhf{}
\\fancyfoot{}
\\renewcommand{\\headrulewidth}{0pt}
\\renewcommand{\\footrulewidth}{0pt}

\\addtolength{\\oddsidemargin}{-0.5in}
\\addtolength{\\evensidemargin}{-0.5in}
\\addtolength{\\textwidth}{1in}
\\addtolength{\\topmargin}{-.5in}
\\addtolength{\\textheight}{1.0in}

\\urlstyle{same}
\\raggedbottom
\\raggedright
\\setlength{\\tabcolsep}{0in}

\\titleformat{\\section}{
  \\vspace{-4pt}\\scshape\\raggedright\\large
}{}{0em}{}[\\color{black}\\titlerule \\vspace{-5pt}]

\\pdfgentounicode=1

\\newcommand{\\resumeItem}[1]{\\item\\small{{#1 \\vspace{-2pt}}}}
\\newcommand{\\resumeSubheading}[4]{
  \\vspace{-2pt}\\item
    \\begin{tabular*}{0.97\\textwidth}[t]{l@{\\extracolsep{\\fill}}r}
      \\textbf{#1} & #2 \\\\
      \\textit{\\small#3} & \\textit{\\small #4} \\\\
    \\end{tabular*}\\vspace{-7pt}
}
\\newcommand{\\resumeProjectHeading}[2]{
    \\item
    \\begin{tabular*}{0.97\\textwidth}{l@{\\extracolsep{\\fill}}r}
      \\small#1 & #2 \\\\
    \\end{tabular*}\\vspace{-7pt}
}
\\newcommand{\\resumeSubItem}[1]{\\resumeItem{#1}\\vspace{-4pt}}
\\renewcommand\\labelitemii{$\\vcenter{\\hbox{\\tiny$\\bullet$}}$}
\\newcommand{\\resumeSubHeadingListStart}{\\begin{itemize}[leftmargin=0.15in, label={}]}
\\newcommand{\\resumeSubHeadingListEnd}{\\end{itemize}}
\\newcommand{\\resumeItemListStart}{\\begin{itemize}}
\\newcommand{\\resumeItemListEnd}{\\end{itemize}\\vspace{-5pt}}

\\begin{document}

\\begin{center}
    \\textbf{\\Huge \\scshape ${escapeLatex(user.first_name)} ${escapeLatex(user.last_name)}} \\\\ \\vspace{1pt}
    \\small ${escapeLatex(user.location)} $|$ \\href{mailto:${user.email}}{\\underline{${escapeLatex(user.email)}}}
\\end{center}

\\section{Education}
  \\resumeSubHeadingListStart${educationBlock}
  \\resumeSubHeadingListEnd

\\section{Experience}
  \\resumeSubHeadingListStart${experienceBlock}
  \\resumeSubHeadingListEnd

\\section{Projects}
    \\resumeSubHeadingListStart${projectsBlock}
    \\resumeSubHeadingListEnd

\\section{Technical Skills}
 \\begin{itemize}[leftmargin=0.15in, label={}]
    \\small{\\item{\\textbf{Skills}{: ${skillsLine}}}}
 \\end{itemize}

\\end{document}
`;

return { json: { latex, filename: `${user.first_name}_${user.last_name}_Resume.tex`.replace(/\s+/g, '_') } };
