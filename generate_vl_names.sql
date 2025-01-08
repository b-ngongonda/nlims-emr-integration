use openmrs_warehouse;
SELECT 
    'Neno' AS district,
    avl.location AS health_facility_name,
    first_name,
    last_name,
    gender,
    opi.identifier AS arv_number,
    birthdate AS date_of_birth,
    visit_date AS date_sample_drawn,
    reason_for_test AS sample_priority,
    'Viral Load' AS tests
FROM
    mw_art_viral_load avl
        JOIN
    omrs_patient_identifier opi ON opi.patient_id = avl.patient_id
        AND type = 'arv number'
        AND avl.location = opi.location
        JOIN
    mw_patient mp ON mp.patient_id = avl.patient_id
WHERE
    visit_date BETWEEN '2024-01-01' AND '2024-12-09'
        AND (viral_load_result IS NULL
        AND less_than_limit IS NULL
        AND ldl IS NULL
        AND other_results IS NULL)
LIMIT 10
