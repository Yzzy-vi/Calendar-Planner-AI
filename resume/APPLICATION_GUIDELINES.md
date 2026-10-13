# Résumé and application guidelines — Joseph Mmanuel Castillo

These rules apply to any assistant preparing or sending job applications on
Joseph's behalf. They were supplied by Joseph and must be followed as written.

## Target roles
International **Deck Cadet**, **Deck Trainee** and **Apprentice Mate**
positions that offer **paid onboard training**.

## Résumé rules
- Before sending applications, use the professional one-page résumé in this
  folder. Two formats are maintained: PDF and editable Word (`.docx`).
- Contact email on the résumé: `filemy77@gmail.com`.
- The résumé must include:
  - PNTC — Bachelor of Science in Marine Transportation (BSMT).
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
- Attach **only the completed résumé** to applications. The fillable draft is
  never attached. Update the résumé as Joseph's documents become available.

## Files in this folder
| File | Purpose |
|---|---|
| `resume_data.json` | Single source of truth for the résumé content. Edit this, then rebuild. |
| `build_docx.js` | Builds the editable Word résumé (`node resume/build_docx.js`). Placeholders are highlighted yellow. |
| `build_fillable_pdf.py` | Builds the fillable one-page PDF draft (`python3 resume/build_fillable_pdf.py`). Missing details are editable form fields. |
| `Joseph_Mmanuel_Castillo_Resume.docx` | Editable Word résumé (draft until placeholders are replaced). |
| `Joseph_Mmanuel_Castillo_Resume_Fillable_Draft.pdf` | Fillable PDF draft. **Do not attach to applications.** |

Once the details below are supplied, replace the placeholders in
`resume_data.json`, rebuild both files, and export the final PDF from the Word
document (or convert it with LibreOffice) under the name
`Joseph_Mmanuel_Castillo_Resume.pdf`. That final PDF is the only version to
attach.

## Details still needed from Joseph
Ask for all of these together, in one message:

1. **Email confirmation.** The instructions say `filemy77@gmail.com`, but the
   account used to give the instructions is `filesmy77@gmail.com`. Confirm
   which address recruiters should use.
2. **Phone number**, including country code.
3. **Location** (city and country) for the résumé header.
4. **Academic completion date** (month and year) for the BSMT program.
5. **Full official name of the school** and campus to print instead of the
   abbreviation "PNTC", if desired.
6. **Nationality** and **date of birth** (commonly requested on seafarer CVs;
   can be left off if preferred).
7. **Passport status**: held or not, and expiry date if held.
8. **Training certificates**: which certificates are pending release, and any
   already held, so they can be listed once issued.
9. **Languages** spoken.
10. **Date available** to join a vessel.
