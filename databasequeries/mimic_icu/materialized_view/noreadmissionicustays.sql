
-- DROP MATERIALIZED VIEW IF EXISTS mimiciv_icu.noreadmissionicustays;

CREATE MATERIALIZED VIEW IF NOT EXISTS mimiciv_icu.noreadmissionicustays AS
 SELECT icustays.subject_id,
    icustays.hadm_id,
    icustays.stay_id,
        CASE
            WHEN icustays.first_careunit::text ~~ '%(MICU)%'::text THEN 'MICU'::text
            WHEN icustays.first_careunit::text ~~ '%(SICU)%'::text THEN 'SICU'::text
            WHEN icustays.first_careunit::text ~~ '%(TSICU)%'::text THEN 'SICU'::text
            ELSE 'NA'::text
        END AS careunit,
    icustays.intime,
    icustays.outtime,
    icustays.los
   FROM mimiciv_icu.icustays
  WHERE icustays.los > 1::double precision AND icustays.los < 30::double precision AND (icustays.hadm_id IN ( SELECT icustays_1.hadm_id
           FROM mimiciv_icu.icustays icustays_1
          GROUP BY icustays_1.hadm_id
         HAVING count(*) = 1))
WITH DATA;

CREATE INDEX idx_noreadmissionicustays_hadm
    ON mimiciv_icu.noreadmissionicustays USING btree
    (hadm_id);

CREATE INDEX idx_noreadmissionicustays_subject_id
    ON mimiciv_icu.noreadmissionicustays USING btree
    (subject_id, hadm_id, stay_id);