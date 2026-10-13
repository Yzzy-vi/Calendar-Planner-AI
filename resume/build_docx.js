// Builds the editable Word résumé from resume_data.json.
// Placeholders for details not yet supplied are highlighted yellow.
// Usage: node resume/build_docx.js
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, AlignmentType, BorderStyle,
  LevelFormat, TabStopType, convertMillimetersToTwip,
} = require("docx");

const data = JSON.parse(fs.readFileSync(path.join(__dirname, "resume_data.json"), "utf8"));
const OUT = path.join(__dirname, "Joseph_Mmanuel_Castillo_Resume.docx");

const FONT = "Calibri";
const NAVY = "1F3A5F";
const GREY = "555555";

const run = (text, opts = {}) => new TextRun({ text, font: FONT, size: 21, ...opts });
const placeholder = (text) => run(text, { highlight: "yellow", color: "7F6000" });

const heading = (text) => new Paragraph({
  spacing: { before: 220, after: 80 },
  border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: NAVY, space: 2 } },
  children: [run(text.toUpperCase(), { bold: true, size: 22, color: NAVY, characterSpacing: 20 })],
});

const body = (children, opts = {}) => new Paragraph({ spacing: { after: 60 }, children, ...opts });

const bullet = (children) => new Paragraph({
  numbering: { reference: "bullets", level: 0 },
  spacing: { after: 40 },
  children,
});

// Label on the left, value on the right-hand tab stop.
const labelValue = (label, valueRuns) => new Paragraph({
  spacing: { after: 40 },
  tabStops: [{ type: TabStopType.LEFT, position: convertMillimetersToTwip(38) }],
  children: [run(label, { bold: true, color: GREY }), run("\t"), ...valueRuns],
});

const children = [];

// Header
children.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { after: 40 },
  children: [run(data.name, { bold: true, size: 40, color: NAVY, characterSpacing: 30 })],
}));
children.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { after: 80 },
  children: [run(data.headline, { size: 22, color: GREY })],
}));
children.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { after: 120 },
  border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: NAVY, space: 6 } },
  children: [
    run("Email: "), run(data.email),
    run("   |   "), run(data.contact_fields.phone.label + ": "), placeholder(data.contact_fields.phone.placeholder),
    run("   |   "), run(data.contact_fields.location.label + ": "), placeholder(data.contact_fields.location.placeholder),
  ],
}));

// Profile
children.push(heading("Profile"));
children.push(body([run(data.profile)], { alignment: AlignmentType.JUSTIFIED }));

// Education
const ed = data.education;
children.push(heading("Education"));
children.push(new Paragraph({
  spacing: { after: 20 },
  tabStops: [{ type: TabStopType.RIGHT, position: convertMillimetersToTwip(170) }],
  children: [
    run(ed.institution, { bold: true }),
    run("\t"),
    run(ed.completion_label + ": ", { color: GREY }),
    placeholder(ed.completion_placeholder),
  ],
}));
children.push(body([run(ed.degree, { italics: true })]));
ed.notes.forEach((n) => children.push(bullet([run(n)])));

// Training and documents
children.push(heading("Training and Documents"));
data.training_documents.forEach((t) => children.push(bullet([run(t)])));

// Sea service
children.push(heading("Sea Service"));
data.sea_service.forEach((t) => children.push(bullet([run(t)])));

// Personal details
children.push(heading("Personal Details"));
data.personal_fields.forEach((f) => children.push(labelValue(f.label, [placeholder(f.placeholder)])));

// Footer line
children.push(new Paragraph({
  spacing: { before: 200 },
  alignment: AlignmentType.CENTER,
  children: [run(data.footer, { italics: true, size: 18, color: GREY })],
}));

const doc = new Document({
  creator: data.name,
  title: "Résumé - " + data.name,
  styles: { default: { document: { run: { font: FONT, size: 21 } } } },
  numbering: {
    config: [{
      reference: "bullets",
      levels: [{
        level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 360, hanging: 240 } } },
      }],
    }],
  },
  sections: [{
    properties: {
      page: {
        // A4
        size: { width: 11906, height: 16838 },
        margin: { top: 1134, bottom: 1134, left: 1134, right: 1134 },
      },
    },
    children,
  }],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(OUT, buf);
  console.log("Wrote", OUT);
});
