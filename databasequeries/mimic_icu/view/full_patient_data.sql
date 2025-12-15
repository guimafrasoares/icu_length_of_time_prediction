
-- DROP VIEW mimiciv_icu.full_patient_data;

CREATE OR REPLACE VIEW mimiciv_icu.full_patient_data AS
 SELECT icu.los,
    icu.subject_id,
    icu.hadm_id,
    icu.stay_id,
    icu.careunit,
    icu.intime,
    icu.outtime,
    pat.gender,
    pat.anchor_age AS age,
    events.celsius_temperature AS temperature,
    events.heart_rate,
    events.blood_pressure_mean,
    events.o2saturation,
    events.respiratory_rate,
    events.gcs_verbal_response,
    events.gcs_motor_response,
    events.gcs_eyes_opening,
    diag.diagnosis_1,
    diag.diagnosis_2,
    diag.diagnosis_3,
    lab.anion_gap_mean,
    lab.bicarbonate_mean,
    lab.chloride_mean,
    lab.creatinine_mean,
    lab.glucose_mean_blood AS glucose_mean,
    lab.hematocrit_mean_blood AS hematocrit_mean,
    lab.hemoglobin_blood_mean,
    lab.magnesium_mean,
    lab.mhc_mean,
    lab.mchc_mean,
    lab.mvc_mean,
    lab.platelet_count_mean,
    lab.potassium_mean,
    lab.rdw_mean,
    lab.red_blood_cells_mean,
    lab.sodium_mean,
    lab.urea_nitrogen_mean,
    lab.white_blood_cells_mean
   FROM mimiciv_icu.noreadmissionicustays icu
     JOIN mimiciv_icu.chartevents24hoursmean events
     ON icu.stay_id = events.stay_id AND icu.hadm_id = events.hadm_id AND icu.subject_id = events.subject_id
     JOIN mimiciv_icu.diagnoses diag
     ON icu.subject_id = diag.subject_id AND icu.hadm_id = diag.hadm_id
     JOIN mimiciv_icu.laboratoryevents_first24hours lab
     ON icu.subject_id = lab.subject_id AND icu.hadm_id = lab.hadm_id AND icu.stay_id = lab.stay_id
     JOIN mimiciv_hosp.patients pat
     ON pat.subject_id = icu.subject_id;
