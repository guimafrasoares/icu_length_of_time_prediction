
-- DROP MATERIALIZED VIEW IF EXISTS mimiciv_icu.laboratoryevents_first24hours;

CREATE MATERIALIZED VIEW IF NOT EXISTS mimiciv_icu.laboratoryevents_first24hours AS
 SELECT max(lab.subject_id) AS subject_id,
    max(lab.hadm_id) AS hadm_id,
    max(icu.stay_id) AS stay_id,
    avg(
        CASE
            WHEN lab.itemid = ANY (ARRAY[52500, 50868]) THEN lab.valuenum
            ELSE NULL::double precision
        END) AS anion_gap_mean,
    avg(
        CASE
            WHEN lab.itemid = 50882 THEN lab.valuenum
            ELSE NULL::double precision
        END) AS bicarbonate_mean,
    avg(
        CASE
            WHEN lab.itemid = ANY (ARRAY[50902, 52535]) THEN lab.valuenum
            ELSE NULL::double precision
        END) AS chloride_mean,
    avg(
        CASE
            WHEN lab.itemid = ANY (ARRAY[50912, 52546]) THEN lab.valuenum
            ELSE NULL::double precision
        END) AS creatinine_mean,
    avg(
        CASE
            WHEN lab.itemid = ANY (ARRAY[50931, 52569, 50809]) THEN lab.valuenum
            ELSE NULL::double precision
        END) AS glucose_mean_blood,
    avg(
        CASE
            WHEN lab.itemid = ANY (ARRAY[51981, 51478]) THEN lab.valuenum
            ELSE NULL::double precision
        END) AS glucose_mean_urine,
    avg(
        CASE
            WHEN lab.itemid = ANY (ARRAY[51221, 52028, 51639, 51638]) THEN lab.valuenum
            ELSE NULL::double precision
        END) AS hematocrit_mean_blood,
    avg(
        CASE
            WHEN lab.itemid = ANY (ARRAY[51480]) THEN lab.valuenum
            ELSE NULL::double precision
        END) AS hematocrit_mean_urine,
    avg(
        CASE
            WHEN lab.itemid = ANY (ARRAY[50811, 51640, 51222]) THEN lab.valuenum
            ELSE NULL::double precision
        END) AS hemoglobin_blood_mean,
    avg(
        CASE
            WHEN lab.itemid = 50960 THEN lab.valuenum
            ELSE NULL::double precision
        END) AS magnesium_mean,
    avg(
        CASE
            WHEN lab.itemid = ANY (ARRAY[53186, 51248]) THEN lab.valuenum
            ELSE NULL::double precision
        END) AS mhc_mean,
    avg(
        CASE
            WHEN lab.itemid = ANY (ARRAY[51249, 53185]) THEN lab.valuenum
            ELSE NULL::double precision
        END) AS mchc_mean,
    avg(
        CASE
            WHEN lab.itemid = ANY (ARRAY[51250, 51691]) THEN lab.valuenum
            ELSE NULL::double precision
        END) AS mvc_mean,
    avg(
        CASE
            WHEN lab.itemid = ANY (ARRAY[53189, 51265]) THEN lab.valuenum
            ELSE NULL::double precision
        END) AS platelet_count_mean,
    avg(
        CASE
            WHEN lab.itemid = ANY (ARRAY[50971, 52610]) THEN lab.valuenum
            ELSE NULL::double precision
        END) AS potassium_mean,
    avg(
        CASE
            WHEN lab.itemid = 51277 THEN lab.valuenum
            ELSE NULL::double precision
        END) AS rdw_mean,
    avg(
        CASE
            WHEN lab.itemid = 51279 THEN lab.valuenum
            ELSE NULL::double precision
        END) AS red_blood_cells_mean,
    avg(
        CASE
            WHEN lab.itemid = ANY (ARRAY[50983, 52623]) THEN lab.valuenum
            ELSE NULL::double precision
        END) AS sodium_mean,
    avg(
        CASE
            WHEN lab.itemid = ANY (ARRAY[52647, 51006]) THEN lab.valuenum
            ELSE NULL::double precision
        END) AS urea_nitrogen_mean,
    avg(
        CASE
            WHEN lab.itemid = ANY (ARRAY[51301, 51756, 51755]) THEN lab.valuenum
            ELSE NULL::double precision
        END) AS white_blood_cells_mean
   FROM mimiciv_hosp.labevents lab
     JOIN mimiciv_icu.noreadmissionicustays icu ON lab.hadm_id = icu.hadm_id AND lab.subject_id = icu.subject_id
  WHERE (lab.itemid = ANY (ARRAY[50809, 50811, 50833, 50868, 50882, 50902, 50912, 50931, 50960, 50971, 50983, 51006, 51221, 51222, 51248, 51249, 51250, 51265, 51277, 51279, 51301, 51478, 51480, 51638, 51639, 51640, 51691, 51755, 51756, 51981, 52028, 52500, 52535, 52546, 52569, 52610, 52623, 52647, 53185, 53186, 53189])) AND (lab.charttime - icu.intime) >= '00:00:00'::interval AND (lab.charttime - icu.intime) <= '24:00:00'::interval
  GROUP BY lab.subject_id, lab.hadm_id
WITH DATA;
