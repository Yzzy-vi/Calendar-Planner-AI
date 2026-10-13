# Résumé and application guidelines — Joseph Mmanuel Castillo

These rules apply to any assistant preparing or sending job applications on
Joseph's behalf. They were supplied by Joseph and must be followed as written.

## Target roles
International **Deck Cadet**, **Deck Trainee** and **Apprentice Mate**
positions that offer **paid onboard training**.

## Résumé rules
- Before sending applications, use the professional one-page résumé in this
  folder. Two formats are maintained: PDF and editable Word (`.docx`).
- Contact email on the résumé: `filesmy77@gmail.com` (confirmed by Joseph).
- The résumé must include:
  - PNTC Colleges — Bachelor of Science in Marine Transportation (BSMT).
  - Academic studies completed; seeking the required 12 months of approved
    onboard training.
  - First-time cadet seeking an initial shipboard placement.
  - Training certificates awaiting release.
  - Seaman's book application to follow once the required certificates are
    available.
- Clean, recruiter-friendly layout.
- **Never invent** skills, experience, grades, dates or credentials.
- **No salary demands on the résumé.** Joseph's requirement for a positive
  salary, stipend or allowance is used only when screening opportunities.
- Attach **only the completed résumé** (`Joseph_Mmanuel_Castillo_Resume.pdf`)
  to applications. Never attach a draft with unfilled fields. Update the
  résumé as Joseph's documents become available.

## Files in this folder
| File | Purpose |
|---|---|
| `resume_data.json` | Single source of truth for the résumé content. Edit this, then rebuild. |
| `build_docx.js` | Builds the editable Word résumé (`node resume/build_docx.js`). Any detail left blank in the data file is rendered as a yellow placeholder. |
| `build_fillable_pdf.py` | Builds a one-page fillable PDF draft (`python3 resume/build_fillable_pdf.py`). Blank details become editable form fields. Only needed while details are missing; its output is never attached. |
| `Joseph_Mmanuel_Castillo_Resume.docx` | Editable Word résumé (complete). |
| `Joseph_Mmanuel_Castillo_Resume.pdf` | Final PDF résumé exported from the Word file. **This is the file to attach.** |
| `APPLICATION_LOG.md` | Applications sent, leads to follow up, and screening notes. |

## Rebuilding after a change
```bash
node resume/build_docx.js
soffice --headless --convert-to pdf --outdir resume resume/Joseph_Mmanuel_Castillo_Resume.docx
```

## Details on file (supplied by Joseph, 13 October 2026)
- Phone: +63 962 081 9151
- Location: General Trias, Cavite, Philippines
- School: PNTC Colleges, Dasmariñas City, Cavite, Philippines
- Academic studies completed: 17 September 2026
- Nationality: Filipino; date of birth: 30 January 2003
- Languages: English, Tagalog
- Availability: immediately, as soon as a placement is offered

## Updates still pending (edit the résumé when each arrives)
1. **SDSD certificate** (Seafarer with Designated Security Duties): add
   certificate number, issuing centre and date once released.
2. **PSSR certificate** (Personal Safety and Social Responsibilities): same.
3. **Passport**: add number and expiry date once released.
4. **Seaman's Book (SIRB)**: application to be filed once the certificates
   are released; add the number once issued.
5. Any further training certificates Joseph obtains.
