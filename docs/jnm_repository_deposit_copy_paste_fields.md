# JNM repository deposit copy-paste fields

Use these fields when creating the public repository record for the frozen Journal of Nuclear Materials reproducibility package.

## File to upload

`submission_packages/jnm_repository_deposit_FROZEN_20260614_b9a8bd2e/journal_of_nuclear_materials_reproducibility_package.zip`

SHA256:

`b9a8bd2e16ea84ed874e31bac701fb0a45b22fe9435b3a2c898306c518a28a30`

Before upload:

```bash
submission_packages/jnm_repository_deposit_FROZEN_20260614_b9a8bd2e/VERIFY_BEFORE_UPLOAD.sh
```

## Repository fields

Resource type:

```text
Dataset
```

Title:

```text
Reduced reproducibility package for acceptance-gated bonded-template DEM of Li4SiO4 breeder-bed fracture sequences
```

Version:

```text
1.0
```

Language:

```text
English
```

Access:

```text
Open
```

License:

```text
CC BY 4.0
```

Keywords:

```text
Li4SiO4; ceramic breeder; fusion blanket; pebble bed; bonded-particle DEM; fracture-event sequence; native force network; Journal of Nuclear Materials
```

Description:

```text
Reduced reproducibility package supporting the manuscript "Acceptance-gated bonded-template DEM reveals localized fracture sequences in Li4SiO4 ceramic breeder beds". The package contains processed single-pebble validation summaries, corrected-bed thermo histories, mother-pebble bond-series tables, breakage-event tables, native force-network summaries, figure source data, manuscript figures and post-processing scripts. Very large DEM restart files and full raw local-bond dump histories are not included in this reduced package and can be assembled as larger audit bundles on reasonable request.
```

Notes:

```text
Before final deposit, confirm author names, affiliations, license choice, repository community and whether ORCID identifiers should be added. After deposit, insert the generated DOI or stable URL into the manuscript Data availability statement, cover letter and submission system.
```

## Creators

```text
Wang, Jian
Affiliation: Anhui University of Science and Technology; Institute of Plasma Physics, Chinese Academy of Sciences

Wang, Siyu
Affiliation: Anhui University of Science and Technology

Zhang, Hang
Affiliation: Anhui University of Science and Technology

Lei, Ming-Zhun
Affiliation: Institute of Plasma Physics, Chinese Academy of Sciences

Wen, Wei
Affiliation: Anhui University of Science and Technology; Institute of Plasma Physics, Chinese Academy of Sciences

Wu, Qi-Gang
Affiliation: Institute of Plasma Physics, Chinese Academy of Sciences

Shen, Gang
Affiliation: Anhui University of Science and Technology

Deng, Haishun
Affiliation: Anhui University of Science and Technology
```

## After repository deposit

After the repository creates a DOI or stable URL, run from the project root:

```bash
python3 scripts/insert_jnm_repository_identifier.py <doi-or-stable-url> --dry-run
python3 scripts/insert_jnm_repository_identifier.py <doi-or-stable-url> --apply --rebuild
```

Expected final gate after DOI insertion:

```text
overall_status=PASS
85 PASS, 0 WARN, 0 BLOCKED_EXTERNAL, 0 FAIL
```
