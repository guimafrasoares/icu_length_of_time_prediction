
-- DROP MATERIALIZED VIEW IF EXISTS mimiciv_icu.chartevents24hoursmean;

CREATE MATERIALIZED VIEW IF NOT EXISTS mimiciv_icu.chartevents24hoursmean
AS
 SELECT c.subject_id,
    c.hadm_id,
    c.stay_id,
    avg(
        CASE
            WHEN c.itemid = 223762 THEN (c.valuenum - 32::double precision) * 5.0::double precision / 9.0::double precision
            WHEN c.itemid = 223761 THEN c.valuenum
            ELSE NULL::double precision
        END) AS celsius_temperature,
    avg(
        CASE
            WHEN c.itemid = 220045 THEN c.valuenum
            ELSE NULL::double precision
        END) AS heart_rate,
    avg(
        CASE
            WHEN c.itemid = 220181 THEN c.valuenum
            ELSE NULL::double precision
        END) AS blood_pressure_mean,
    avg(
        CASE
            WHEN c.itemid = 220277 THEN c.valuenum
            ELSE NULL::double precision
        END) AS o2saturation,
    avg(
        CASE
            WHEN c.itemid = 220210 THEN c.valuenum
            ELSE NULL::double precision
        END) AS respiratory_rate,
    avg(
        CASE
            WHEN c.itemid = 223900 THEN c.valuenum
            ELSE NULL::double precision
        END) AS gcs_verbal_response,
    avg(
        CASE
            WHEN c.itemid = 223901 THEN c.valuenum
            ELSE NULL::double precision
        END) AS gcs_motor_response,
    avg(
        CASE
            WHEN c.itemid = 220739 THEN c.valuenum
            ELSE NULL::double precision
        END) AS gcs_eyes_opening
   FROM mimiciv_icu.chartevents c
     JOIN mimiciv_icu.noreadmissionicustays iculos ON c.stay_id = iculos.stay_id AND c.hadm_id = iculos.hadm_id AND c.subject_id = iculos.subject_id
  WHERE (c.itemid = ANY (ARRAY[223762, 223761, 220045, 220181, 220277, 220210, 223900, 223901, 220739])) AND (c.charttime - iculos.intime) >= '00:00:00'::interval AND (c.charttime - iculos.intime) <= '24:00:00'::interval
  GROUP BY c.subject_id, c.hadm_id, c.stay_id
WITH DATA;
