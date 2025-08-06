PORT=8002
SERVICE_NAME=skill-assessment
VAULT_ADDR=http://vault:8200
KAFKA_BOOTSTRAP=kafka:9092
OPA_URL=http://opa:8181/v1/data/authz/allow
DB_NAME=skill_assessment
DB_HOST=postgres
DB_PORT=5432
LOG_LEVEL=INFO
ASSESSMENT_ALGORITHMS=multi_modal_evaluation,competency_mapping,skill_gap_analysis
BIAS_ELIMINATION=merit_based_assessment_v2.0
SKILL_ENGINE=proficiency_measurement_only
# Because we measure skills, not schmoozing ability! 🎓⚖️
CERTIFICATION_TRACKING=industry_standard_validation
# No bias, just pure skill science! ✨
