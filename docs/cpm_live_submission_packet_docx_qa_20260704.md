# CPM live-submission packet DOCX QA, 2026-07-04

## File

- DOCX: `manuscript/computational_particle_mechanics_live_submission_packet.docx`
- Rendered PDF: `docs/pdf_visual_qa/cpm_live_submission_packet_20260704/computational_particle_mechanics_live_submission_packet.pdf`
- Rendered pages: `docs/pdf_visual_qa/cpm_live_submission_packet_20260704/page-1.png` to `page-4.png`

## Render check

Rendered with:

```bash
/Users/wangjian-macbook13/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  /Users/wangjian-macbook13/.codex/plugins/cache/openai-primary-runtime/documents/26.630.12135/skills/documents/render_docx.py \
  manuscript/computational_particle_mechanics_live_submission_packet.docx \
  --output_dir docs/pdf_visual_qa/cpm_live_submission_packet_20260704 \
  --emit_pdf
```

Render result:

- `page-1.png`: content bbox `(131, 152, 1391, 1823)`, area fraction `0.680`
- `page-2.png`: content bbox `(131, 145, 1397, 1818)`, area fraction `0.684`
- `page-3.png`: content bbox `(145, 149, 1398, 1743)`, area fraction `0.645`
- `page-4.png`: content bbox `(147, 147, 1024, 299)`, area fraction `0.043`

Page 4 contains only the final external-action bullets. No blank page, text
overlap, clipped table text or missing rendered page was observed in the
generated PNG/PDF outputs.

## Package checks after integration

```text
PASS repaired submission package check
PASS CPM scientific alignment: manuscript, cover letter, fields and gap map match
PASS CPM reviewer-risk preflight: 7 risks mapped to current evidence and boundaries
PASS CPM submission package: manifest=15, figures=19, docx=9, DOI, guide alignment, live packet and optional blinded package verified
repaired_submission_package.zip: OK
computational_particle_mechanics_blinded_review_optional.zip: OK
computational_particle_mechanics_upload_ready.zip: OK
```
