#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
package="$root/submission_packages/journal_of_nuclear_materials_submission_package"
archive="$root/submission_packages/journal_of_nuclear_materials_submission_package.zip"

rm -rf "$package"
mkdir -p \
  "$package/manuscript" \
  "$package/docs" \
  "$package/docs/pdf_visual_qa/jnm_main_20260612" \
  "$package/figures/main" \
  "$package/figures/sp002" \
  "$package/figures/pb007" \
  "$package/scripts" \
  "$package/tables" \
  "$package/data/processed"

cp "$root/START_HERE_JNM_SUBMISSION.md" "$package/"

cp \
  "$root/manuscript/journal_of_nuclear_materials_submission.pdf" \
  "$root/manuscript/journal_of_nuclear_materials_submission.tex" \
  "$root/manuscript/journal_of_nuclear_materials_submission_draft.md" \
  "$root/manuscript/journal_of_nuclear_materials_author_metadata.csv" \
  "$root/manuscript/journal_of_nuclear_materials_author_declaration_checklist.md" \
  "$root/manuscript/journal_of_nuclear_materials_supplementary.pdf" \
  "$root/manuscript/journal_of_nuclear_materials_supplementary.tex" \
  "$root/manuscript/journal_of_nuclear_materials_supplementary.md" \
  "$root/manuscript/journal_of_nuclear_materials_cover_letter_draft.md" \
  "$root/manuscript/journal_of_nuclear_materials_cover_letter.docx" \
  "$root/manuscript/journal_of_nuclear_materials_elsevier_declarations.md" \
  "$root/manuscript/journal_of_nuclear_materials_elsevier_declarations.docx" \
  "$root/manuscript/journal_of_nuclear_materials_editorial_manager_upload_checklist.md" \
  "$root/manuscript/journal_of_nuclear_materials_editorial_manager_upload_matrix.csv" \
  "$root/manuscript/journal_of_nuclear_materials_editorial_manager_paste_fields.md" \
  "$root/manuscript/journal_of_nuclear_materials_highlights.md" \
  "$root/manuscript/journal_of_nuclear_materials_repository_metadata_zenodo.json" \
  "$root/manuscript/journal_of_nuclear_materials_repository_metadata_readme.md" \
  "$root/manuscript/journal_of_nuclear_materials_repro_package_readme.md" \
  "$root/manuscript/journal_of_nuclear_materials_resubmission_plan.md" \
  "$root/manuscript/journal_of_nuclear_materials_submission_asset_manifest.csv" \
  "$root/manuscript/journal_of_nuclear_materials_reviewer_risk_prebuttal.md" \
  "$root/manuscript/journal_of_nuclear_materials_reviewer_risk_matrix.csv" \
  "$root/manuscript/journal_of_nuclear_materials_figure_table_source_data_matrix.csv" \
  "$root/manuscript/journal_of_nuclear_materials_claim_evidence_boundary_matrix.csv" \
  "$root/manuscript/figure_captions.md" \
  "$root/manuscript/references.bib" \
  "$package/manuscript/"

cp \
  "$root/docs/jnm_force_transmission_validation_audit_20260612.md" \
  "$root/docs/jnm_author_final_upload_readme_zh.md" \
  "$root/docs/jnm_final_submission_action_summary.md" \
  "$root/docs/jnm_coauthor_final_approval_packet.md" \
  "$root/docs/jnm_repository_deposit_final_handoff_zh.md" \
  "$root/docs/jnm_repository_deposit_copy_paste_fields.md" \
  "$root/docs/jnm_revision_gate_after_pb006_audit_20260612.md" \
  "$root/docs/jnm_submission_readiness_audit_20260612.md" \
  "$root/docs/jnm_scientific_storyline_audit_20260613.md" \
  "$root/docs/jnm_event_topology_mechanism_audit_20260613.md" \
  "$root/docs/jnm_objective_completion_audit_20260613.md" \
  "$root/docs/jnm_final_scientific_traceability_audit_20260613.md" \
  "$root/docs/jnm_transfer_positioning_audit_20260613.md" \
  "$root/docs/jnm_materials_novelty_positioning_matrix_20260613.md" \
  "$root/docs/jnm_reviewer_boundary_audit_20260613.md" \
  "$root/docs/jnm_material_degradation_state_variables_audit_20260613.md" \
  "$root/docs/jnm_key_numeric_consistency_audit_20260613.md" \
  "$root/docs/jnm_model_parameter_consistency_audit_20260613.md" \
  "$root/docs/jnm_active_run_provenance_capsule_20260613.md" \
  "$root/docs/jnm_doi_rehearsal_after_key_numeric_audit_20260613.md" \
  "$root/docs/jnm_figure_editorial_polish_audit_20260613.md" \
  "$root/docs/single_pebble_calibration_dossier.md" \
  "$root/docs/jnm_final_submission_gate_report.md" \
  "$root/docs/jnm_final_submission_gate_report.json" \
  "$root/docs/jnm_pdf_visual_qa_20260612.md" \
  "$root/docs/jnm_upload_docx_qa.md" \
  "$root/docs/next_stage_optimization_plan.md" \
  "$package/docs/"
cp \
  "$root/docs/pdf_visual_qa/jnm_main_20260612/contact_sheet.png" \
  "$root/docs/pdf_visual_qa/jnm_main_20260612/page-01.png" \
  "$root/docs/pdf_visual_qa/jnm_main_20260612/page-02.png" \
  "$root/docs/pdf_visual_qa/jnm_main_20260612/page-03.png" \
  "$root/docs/pdf_visual_qa/jnm_main_20260612/page-04.png" \
  "$root/docs/pdf_visual_qa/jnm_main_20260612/page-05.png" \
  "$root/docs/pdf_visual_qa/jnm_main_20260612/page-06.png" \
  "$root/docs/pdf_visual_qa/jnm_main_20260612/page-07.png" \
  "$root/docs/pdf_visual_qa/jnm_main_20260612/page-08.png" \
  "$root/docs/pdf_visual_qa/jnm_main_20260612/page-09.png" \
  "$root/docs/pdf_visual_qa/jnm_main_20260612/page-10.png" \
  "$package/docs/pdf_visual_qa/jnm_main_20260612/"

cp \
  "$root/figures/main/fig1_workflow.pdf" \
  "$root/figures/main/fig1_workflow.png" \
  "$root/figures/main/journal_of_nuclear_materials_graphical_abstract.pdf" \
  "$root/figures/main/journal_of_nuclear_materials_graphical_abstract.png" \
  "$root/figures/main/journal_of_nuclear_materials_graphical_abstract.tiff" \
  "$package/figures/main/"
cp \
  "$root/figures/sp002/single_pebble_calibration_evidence.pdf" \
  "$root/figures/sp002/single_pebble_calibration_evidence.png" \
  "$root/figures/sp002/jnm_single_pebble_validation.pdf" \
  "$root/figures/sp002/jnm_single_pebble_validation.png" \
  "$root/figures/sp002/single_pebble_fragment_morphology_paraview.png" \
  "$package/figures/sp002/"
cp \
  "$root/figures/pb007/pb007_acceptance_gate_validation.pdf" \
  "$root/figures/pb007/pb007_acceptance_gate_validation.png" \
  "$root/figures/pb007/pb007_corrected_fracture_sequence.pdf" \
  "$root/figures/pb007/pb007_corrected_fracture_sequence.png" \
  "$root/figures/pb007/pb007_replicate_comparison.pdf" \
  "$root/figures/pb007/pb007_replicate_comparison.svg" \
  "$root/figures/pb007/pb007_replicate_comparison.png" \
  "$root/figures/pb007/PB-007-bonded-steprelaxed-100-seed02-600ksettle-y1p5e10-10krelax-60um-nohold-strength0p5-trigger-seed02_validation.pdf" \
  "$root/figures/pb007/PB-007-bonded-steprelaxed-100-seed02-600ksettle-y1p5e10-10krelax-60um-nohold-strength0p5-trigger-seed02_validation.png" \
  "$root/figures/pb007/PB-007-bonded-steprelaxed-100-seed02-600ksettle-y1p5e10-10krelax-60um-nohold-strength0p25-trigger-seed02_validation.pdf" \
  "$root/figures/pb007/PB-007-bonded-steprelaxed-100-seed02-600ksettle-y1p5e10-10krelax-60um-nohold-strength0p25-trigger-seed02_validation.png" \
  "$package/figures/pb007/"
cp \
  "$root/tables/single_pebble_calibration_target_evidence_summary.csv" \
  "$root/tables/single_pebble_model_ensemble_evidence_summary.csv" \
  "$root/tables/sp002_conditioned_ensemble_completed_summary.csv" \
  "$root/tables/jnm_single_pebble_resolution_summary.csv" \
  "$root/tables/jnm_single_pebble_rate_summary.csv" \
  "$root/tables/pb007_macro_topology_event_metrics.csv" \
  "$root/tables/jnm_material_degradation_mechanism_indices.csv" \
  "$root/tables/pb007_event_aligned_topology.csv" \
  "$root/tables/pb007_PB-007-bonded-steprelaxed-100-pilot-y1p5e10-10krelax-60um-fracture-pilot_acceptance_summary.csv" \
  "$root/tables/pb007_PB-007-bonded-steprelaxed-100-pilot-y1p5e10-10krelax-60um-fracture-pilot_native_summary.csv" \
  "$root/tables/pb007_PB-007-bonded-steprelaxed-100-seed02-600ksettle-y1p5e10-10krelax-60um-nohold-fracture-seed02_acceptance_summary.csv" \
  "$root/tables/pb007_PB-007-bonded-steprelaxed-100-seed02-600ksettle-y1p5e10-10krelax-60um-nohold-fracture-seed02_native_summary.csv" \
  "$root/tables/pb007_PB-007-bonded-steprelaxed-100-seed03-600ksettle-y1p5e10-10krelax-60um-nohold-fracture-seed03_acceptance_summary.csv" \
  "$root/tables/pb007_PB-007-bonded-steprelaxed-100-seed03-600ksettle-y1p5e10-10krelax-60um-nohold-fracture-seed03_native_summary.csv" \
  "$root/tables/pb007_PB-007-bonded-steprelaxed-100-seed02-600ksettle-y1p5e10-10krelax-60um-nohold-strength0p5-trigger-seed02_acceptance_summary.csv" \
  "$root/tables/pb007_PB-007-bonded-steprelaxed-100-seed02-600ksettle-y1p5e10-10krelax-60um-nohold-strength0p5-trigger-seed02_native_summary.csv" \
  "$root/tables/pb007_PB-007-bonded-steprelaxed-100-seed02-600ksettle-y1p5e10-10krelax-60um-nohold-strength0p25-trigger-seed02_acceptance_summary.csv" \
  "$root/tables/pb007_PB-007-bonded-steprelaxed-100-seed02-600ksettle-y1p5e10-10krelax-60um-nohold-strength0p25-trigger-seed02_native_summary.csv" \
  "$package/tables/"
cp \
  "$root/data/processed/PB-007-bonded-steprelaxed-100-pilot-y1p5e10-10krelax-60um-fracture-pilot_breakage_events.csv" \
  "$root/data/processed/PB-007-bonded-steprelaxed-100-pilot-y1p5e10-10krelax-60um-fracture-pilot_bond_series.csv" \
  "$root/data/processed/PB-007-bonded-steprelaxed-100-pilot-y1p5e10-10krelax-60um-fracture-pilot_native_force_network_series.csv" \
  "$root/data/processed/PB-007-bonded-steprelaxed-100-pilot-y1p5e10-10krelax-60um-fracture-pilot_thermo.csv" \
  "$root/data/processed/PB-007-bonded-steprelaxed-100-pilot-y1p5e10-10krelax-60um-fracture-pilot_validation_curve.csv" \
  "$root/data/processed/PB-007-bonded-steprelaxed-100-seed02-600ksettle-y1p5e10-10krelax-60um-nohold-fracture-seed02_breakage_events.csv" \
  "$root/data/processed/PB-007-bonded-steprelaxed-100-seed02-600ksettle-y1p5e10-10krelax-60um-nohold-fracture-seed02_bond_series.csv" \
  "$root/data/processed/PB-007-bonded-steprelaxed-100-seed02-600ksettle-y1p5e10-10krelax-60um-nohold-fracture-seed02_native_force_network_series.csv" \
  "$root/data/processed/PB-007-bonded-steprelaxed-100-seed02-600ksettle-y1p5e10-10krelax-60um-nohold-fracture-seed02_thermo.csv" \
  "$root/data/processed/PB-007-bonded-steprelaxed-100-seed02-600ksettle-y1p5e10-10krelax-60um-nohold-fracture-seed02_validation_curve.csv" \
  "$root/data/processed/PB-007-bonded-steprelaxed-100-seed03-600ksettle-y1p5e10-10krelax-60um-nohold-fracture-seed03_breakage_events.csv" \
  "$root/data/processed/PB-007-bonded-steprelaxed-100-seed03-600ksettle-y1p5e10-10krelax-60um-nohold-fracture-seed03_bond_series.csv" \
  "$root/data/processed/PB-007-bonded-steprelaxed-100-seed03-600ksettle-y1p5e10-10krelax-60um-nohold-fracture-seed03_native_force_network_series.csv" \
  "$root/data/processed/PB-007-bonded-steprelaxed-100-seed03-600ksettle-y1p5e10-10krelax-60um-nohold-fracture-seed03_thermo.csv" \
  "$root/data/processed/PB-007-bonded-steprelaxed-100-seed02-600ksettle-y1p5e10-10krelax-60um-nohold-strength0p5-trigger-seed02_breakage_events.csv" \
  "$root/data/processed/PB-007-bonded-steprelaxed-100-seed02-600ksettle-y1p5e10-10krelax-60um-nohold-strength0p5-trigger-seed02_bond_series.csv" \
  "$root/data/processed/PB-007-bonded-steprelaxed-100-seed02-600ksettle-y1p5e10-10krelax-60um-nohold-strength0p5-trigger-seed02_native_force_network_series.csv" \
  "$root/data/processed/PB-007-bonded-steprelaxed-100-seed02-600ksettle-y1p5e10-10krelax-60um-nohold-strength0p5-trigger-seed02_thermo.csv" \
  "$root/data/processed/PB-007-bonded-steprelaxed-100-seed02-600ksettle-y1p5e10-10krelax-60um-nohold-strength0p5-trigger-seed02_validation_curve.csv" \
  "$root/data/processed/PB-007-bonded-steprelaxed-100-seed02-600ksettle-y1p5e10-10krelax-60um-nohold-strength0p25-trigger-seed02_breakage_events.csv" \
  "$root/data/processed/PB-007-bonded-steprelaxed-100-seed02-600ksettle-y1p5e10-10krelax-60um-nohold-strength0p25-trigger-seed02_bond_series.csv" \
  "$root/data/processed/PB-007-bonded-steprelaxed-100-seed02-600ksettle-y1p5e10-10krelax-60um-nohold-strength0p25-trigger-seed02_native_force_network_series.csv" \
  "$root/data/processed/PB-007-bonded-steprelaxed-100-seed02-600ksettle-y1p5e10-10krelax-60um-nohold-strength0p25-trigger-seed02_thermo.csv" \
  "$root/data/processed/PB-007-bonded-steprelaxed-100-seed02-600ksettle-y1p5e10-10krelax-60um-nohold-strength0p25-trigger-seed02_validation_curve.csv" \
  "$root/data/processed/pb007_replicate_comparison_source_data.csv" \
  "$package/data/processed/"
cp \
  "$root/scripts/plot_main_workflow_figure.py" \
  "$root/scripts/plot_single_pebble_calibration_evidence.py" \
  "$root/scripts/build_jnm_single_pebble_validation.py" \
  "$root/scripts/plot_pb007_acceptance_gate_validation.py" \
  "$root/scripts/plot_pb007_corrected_fracture_sequence.py" \
  "$root/scripts/build_pb007_replicate_comparison.py" \
  "$root/scripts/summarize_pb007_mechanism_metrics.py" \
  "$root/scripts/summarize_pb007_event_aligned_topology.py" \
  "$root/scripts/build_jnm_event_topology_mechanism_audit.py" \
  "$root/scripts/postprocess_pb007_corrected_fracture_pilot.sh" \
  "$root/scripts/analyze_pb007_bond_event_sequence.py" \
  "$root/scripts/analyze_pb007_native_force_network.py" \
  "$root/scripts/analyze_pb007_native_force_network_series.py" \
  "$root/scripts/summarize_pb007_loadpath_validation.py" \
  "$root/scripts/build_journal_of_nuclear_materials_latex.py" \
  "$root/scripts/build_jnm_elsevier_flat_source_bundle.py" \
  "$root/scripts/render_jnm_pdf_visual_qa.py" \
  "$root/scripts/build_jnm_repository_deposit_staging.py" \
  "$root/scripts/build_jnm_public_repro_package.py" \
  "$root/scripts/check_jnm_abstract_scope.py" \
  "$root/scripts/check_jnm_author_metadata.py" \
  "$root/scripts/check_jnm_manuscript_integrity.py" \
  "$root/scripts/check_jnm_pdf_visual_qa.py" \
  "$root/scripts/check_jnm_pdf_frontmatter.py" \
  "$root/scripts/check_jnm_public_artifact_hygiene.py" \
  "$root/scripts/check_jnm_reader_facing_hygiene.py" \
  "$root/scripts/check_jnm_no_fake_repository_identifier.py" \
  "$root/scripts/check_jnm_submission_gate.py" \
  "$root/scripts/check_jnm_source_data_matrix.py" \
  "$root/scripts/check_jnm_claim_evidence_matrix.py" \
  "$root/scripts/check_jnm_figure_text_labels.py" \
  "$root/scripts/check_jnm_figure_captions_companion.py" \
  "$root/scripts/check_jnm_cover_letter.py" \
  "$root/scripts/check_jnm_declarations.py" \
  "$root/scripts/check_jnm_coauthor_approval_packet.py" \
  "$root/scripts/build_jnm_upload_docx.py" \
  "$root/scripts/check_jnm_upload_docx.py" \
  "$root/scripts/build_jnm_editorial_manager_paste_fields.py" \
  "$root/scripts/check_jnm_editorial_manager_paste_fields.py" \
  "$root/scripts/check_jnm_elsevier_upload_compliance.py" \
  "$root/scripts/build_jnm_editorial_manager_upload_ready.py" \
  "$root/scripts/check_jnm_editorial_manager_upload_ready.py" \
  "$root/scripts/check_jnm_repository_deposit_staging.py" \
  "$root/scripts/check_jnm_frozen_deposit_packet.py" \
  "$root/scripts/check_jnm_start_here.py" \
  "$root/scripts/check_jnm_repository_copy_paste_fields.py" \
  "$root/scripts/build_jnm_repository_deposit_handoff.py" \
  "$root/scripts/build_jnm_final_upload_manifest.py" \
  "$root/scripts/check_jnm_final_upload_manifest.py" \
  "$root/scripts/check_jnm_public_repro_package.py" \
  "$root/scripts/check_jnm_references.py" \
  "$root/scripts/check_jnm_repro_package_coverage.py" \
  "$root/scripts/check_jnm_scientific_storyline.py" \
  "$root/scripts/check_jnm_objective_completion_audit.py" \
  "$root/scripts/build_jnm_final_scientific_traceability_audit.py" \
  "$root/scripts/check_jnm_final_scientific_traceability_audit.py" \
  "$root/scripts/check_jnm_transfer_positioning_audit.py" \
  "$root/scripts/check_jnm_materials_novelty_positioning.py" \
  "$root/scripts/check_jnm_reviewer_boundaries.py" \
  "$root/scripts/check_jnm_material_degradation_state_variables.py" \
  "$root/scripts/check_jnm_key_numeric_consistency.py" \
  "$root/scripts/check_jnm_model_parameter_consistency.py" \
  "$root/scripts/check_jnm_active_run_provenance.py" \
  "$root/scripts/insert_jnm_repository_identifier.py" \
  "$root/scripts/print_jnm_repository_deposit_packet.py" \
  "$root/scripts/plot_jnm_graphical_abstract.py" \
  "$package/scripts/"

cp \
  "$root/submission_packages/journal_of_nuclear_materials_flat_source.zip" \
  "$root/submission_packages/journal_of_nuclear_materials_flat_source.zip.sha256" \
  "$root/submission_packages/jnm_editorial_manager_upload_ready.zip" \
  "$root/submission_packages/jnm_editorial_manager_upload_ready.zip.sha256" \
  "$package/"

(
  cd "$package"
  {
    echo "sha256,path,size_bytes"
    find . -type f ! -name MANIFEST.csv -print0 \
      | sort -z \
      | while IFS= read -r -d '' f; do
          hash="$(shasum -a 256 "$f" | awk '{print $1}')"
          size="$(wc -c < "$f" | tr -d ' ')"
          clean="${f#./}"
          printf "%s,%s,%s\n" "$hash" "$clean" "$size"
        done
  } > MANIFEST.csv
)

(
  cd "$root/submission_packages"
  rm -f "$(basename "$archive")"
  zip -qr "$(basename "$archive")" "$(basename "$package")"
  shasum -a 256 "$(basename "$archive")" > "$(basename "$archive").sha256"
)

echo "$archive"
