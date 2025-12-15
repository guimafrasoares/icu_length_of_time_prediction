
-- DROP FUNCTION IF EXISTS support.get_icd10_from_icd9(text);

CREATE OR REPLACE FUNCTION support.get_icd10_from_icd9(
	p_icd9 text)
    RETURNS text
    LANGUAGE 'sql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
  SELECT icd10cm
  FROM support.icd9toicd10
  WHERE icd9cm = $1
  LIMIT 1;
$BODY$;
