#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

PACKAGE="journal_of_nuclear_materials_reproducibility_package.zip"
CHECKSUM="${PACKAGE}.sha256"
METADATA="journal_of_nuclear_materials_repository_metadata_zenodo.json"
EXPECTED_SHA="b9a8bd2e16ea84ed874e31bac701fb0a45b22fe9435b3a2c898306c518a28a30"

echo "JNM frozen repository-deposit packet verification"
echo "================================================="
echo "Folder: $(pwd)"
echo "Package: ${PACKAGE}"
echo

if [[ ! -f "${PACKAGE}" ]]; then
  echo "ERROR: missing ${PACKAGE}" >&2
  exit 1
fi

if [[ ! -f "${CHECKSUM}" ]]; then
  echo "ERROR: missing ${CHECKSUM}" >&2
  exit 1
fi

if [[ ! -f "${METADATA}" ]]; then
  echo "ERROR: missing ${METADATA}" >&2
  exit 1
fi

echo "1. Checking package checksum..."
shasum -a 256 -c "${CHECKSUM}"

ACTUAL_SHA="$(shasum -a 256 "${PACKAGE}" | awk '{print $1}')"
if [[ "${ACTUAL_SHA}" != "${EXPECTED_SHA}" ]]; then
  echo "ERROR: package SHA changed." >&2
  echo "Expected: ${EXPECTED_SHA}" >&2
  echo "Actual:   ${ACTUAL_SHA}" >&2
  exit 1
fi

echo
echo "2. Checking metadata JSON syntax..."
python3 -m json.tool "${METADATA}" >/dev/null
echo "Metadata JSON: OK"

echo
echo "3. Frozen upload packet is ready."
echo "Upload this file to Zenodo, Figshare or an institutional repository:"
echo "  $(pwd)/${PACKAGE}"
echo
echo "SHA256:"
echo "  ${EXPECTED_SHA}"
echo
echo "After the repository gives a DOI or stable URL, return to the project root and run:"
echo "  python3 scripts/insert_jnm_repository_identifier.py <doi-or-stable-url> --dry-run"
echo "  python3 scripts/insert_jnm_repository_identifier.py <doi-or-stable-url> --apply --rebuild"
