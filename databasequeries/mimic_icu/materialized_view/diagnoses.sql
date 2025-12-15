
-- DROP MATERIALIZED VIEW IF EXISTS mimiciv_icu.diagnoses;

CREATE MATERIALIZED VIEW IF NOT EXISTS mimiciv_icu.diagnoses AS
 SELECT max(icd.subject_id) AS subject_id,
    max(icd.hadm_id) AS hadm_id,
    max(
        CASE
            WHEN icd.seq_num = 1 AND icd.icd_version = 10 THEN icd.icd_code
            WHEN icd.seq_num = 1 AND icd.icd_version = 9 THEN (( SELECT support.get_icd10_from_icd9(icd.icd_code::text) AS get_icd10_from_icd9))::bpchar
            ELSE NULL::bpchar
        END) AS diagnosis_1,
    max(
        CASE
            WHEN icd.seq_num = 2 AND icd.icd_version = 10 THEN icd.icd_code
            WHEN icd.seq_num = 2 AND icd.icd_version = 9 THEN (( SELECT support.get_icd10_from_icd9(icd.icd_code::text) AS get_icd10_from_icd9))::bpchar
            ELSE NULL::bpchar
        END) AS diagnosis_2,
    max(
        CASE
            WHEN icd.seq_num = 3 AND icd.icd_version = 10 THEN icd.icd_code
            WHEN icd.seq_num = 3 AND icd.icd_version = 9 THEN (( SELECT support.get_icd10_from_icd9(icd.icd_code::text) AS get_icd10_from_icd9))::bpchar
            ELSE NULL::bpchar
        END) AS diagnosis_3
   FROM mimiciv_hosp.diagnoses_icd icd
     JOIN mimiciv_icu.noreadmissionicustays stays ON icd.hadm_id = stays.hadm_id AND icd.subject_id = stays.subject_id
  GROUP BY icd.subject_id, icd.hadm_id
WITH DATA;

CREATE INDEX idx_diagnoses_ids
    ON mimiciv_icu.diagnoses USING btree
    (subject_id, hadm_id);