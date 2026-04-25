"""
Synthetic MIMIC-FHIR NDJSON Generator
Creates a minimal but realistic dataset for testing the system
when actual MIMIC data is not available.

Usage:  python generate_test_data.py --patients 30 --out dataset
"""

import json
import random
import argparse
import uuid
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)

GENDERS     = ["male", "female"]
CONDITIONS  = [
    ("73211009", "Diabetes mellitus"),
    ("44054006", "Diabetes mellitus type 2"),
    ("38341003", "Hypertensive disorder"),
    ("22298006", "Myocardial infarction"),
    ("13645005", "Chronic obstructive pulmonary disease"),
    ("59621000", "Essential hypertension"),
    ("84114007", "Heart failure"),
    ("49601007", "Disorder of cardiovascular system"),
    ("195967001", "Asthma"),
    ("709044004", "Chronic kidney disease"),
    ("367498001", "Acute respiratory distress syndrome"),
    ("302866003", "Hypoglycaemia"),
]
MEDICATIONS = [
    ("1049502", "12 HR Metformin"),
    ("313782", "Acetaminophen 325mg"),
    ("197361", "Amlodipine 5mg"),
    ("310798", "Furosemide 40mg"),
    ("197379", "Atorvastatin 40mg"),
    ("199314", "Metoprolol Succinate"),
    ("855332", "Warfarin 5mg"),
    ("892244", "Lisinopril 10mg"),
    ("309362", "Insulin Regular"),
    ("1117825", "Vancomycin"),
]
PROCEDURES  = [
    ("33195004",  "Mechanical ventilation"),
    ("265764009", "Renal dialysis"),
    ("302497006", "Haemodialysis"),
    ("71388002",  "Procedure"),
    ("432102000", "Administration of substance"),
]
OBSERVATIONS = [
    ("8867-4",  "Heart rate",             40, 180, "beats/min"),
    ("8480-6",  "Systolic blood pressure", 60, 200, "mmHg"),
    ("8462-4",  "Diastolic blood pressure",30, 130, "mmHg"),
    ("8310-5",  "Body temperature",        35, 41,  "Cel"),
    ("59408-5", "Oxygen saturation",       70, 100, "%"),
    ("9279-1",  "Respiratory rate",        8,  40,  "breaths/min"),
    ("2339-0",  "Glucose [Mass/volume]",   50, 400, "mg/dL"),
    ("2160-0",  "Creatinine",              0.5, 10, "mg/dL"),
    ("718-7",   "Hemoglobin",              5,  18,  "g/dL"),
    ("6690-2",  "Leukocytes",             1, 30,   "10*3/uL"),
]

ORG_ID = "mimic-org-1"
BASE_DATE = datetime(2150, 1, 1)


def rand_date(base=BASE_DATE, offset_days=1000):
    return base + timedelta(days=random.randint(0, offset_days))


def rand_ref(resource_type, rid):
    return {"reference": f"{resource_type}/{rid}"}


def write_ndjson(path: Path, records: list):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")
    print(f"  Written: {path} ({len(records)} records)")


def generate(n_patients: int, out_dir: str):
    base = Path(out_dir)
    base.mkdir(parents=True, exist_ok=True)

    patient_ids = [str(uuid.uuid4())[:8] for _ in range(n_patients)]
    encounter_map = {}  # patient_id -> list of encounter_ids
    all_encounters = []
    all_conditions = []
    all_obs_chart  = []
    all_obs_lab    = []
    all_meds       = []
    all_procs      = []
    patients       = []

    for pid in patient_ids:
        birth = rand_date(datetime(2050, 1, 1), 30000)
        gender = random.choice(GENDERS)
        deceased = random.random() < 0.15
        dec_dt = rand_date(birth, 30000).strftime("%Y-%m-%dT%H:%M:%SZ") if deceased else None

        patient = {
            "resourceType": "Patient",
            "id": pid,
            "meta": {"profile": ["http://mimic.mit.edu/fhir/mimic/StructureDefinition/mimic-patient"]},
            "gender": gender,
            "birthDate": birth.strftime("%Y-%m-%d"),
            "identifier": [{"system": "http://mimic.mit.edu/fhir/mimic/sid/patient", "value": pid}],
            "managingOrganization": rand_ref("Organization", ORG_ID),
            "maritalStatus": {"coding": [{"system": "http://terminology.hl7.org/CodeSystem/v3-MaritalStatus",
                                           "code": random.choice(["M", "S", "W", "D"])}]},
            "extension": [],
            "name": [{"use": "official", "family": f"Patient-{pid[:4]}"}],
        }
        if dec_dt:
            patient["deceasedDateTime"] = dec_dt
        patients.append(patient)

        # Encounters
        n_enc = random.randint(1, 8)
        enc_ids = []
        for _ in range(n_enc):
            eid = str(uuid.uuid4())[:8]
            enc_ids.append(eid)
            start = rand_date()
            end = start + timedelta(hours=random.randint(2, 240))
            enc_class = random.choice(["IMP", "EMER", "AMB"])
            all_encounters.append({
                "resourceType": "Encounter",
                "id": eid,
                "meta": {"profile": ["http://mimic.mit.edu/fhir/mimic/StructureDefinition/mimic-encounter"]},
                "status": "finished",
                "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
                           "code": enc_class, "display": enc_class},
                "subject": rand_ref("Patient", pid),
                "period": {"start": start.strftime("%Y-%m-%dT%H:%M:%SZ"),
                           "end":   end.strftime("%Y-%m-%dT%H:%M:%SZ")},
                "hospitalization": {
                    "admitSource": {"coding": [{"system": "http://mimic.mit.edu/fhir/mimic",
                                                 "code": "emergency"}]},
                    "dischargeDisposition": {"coding": [{"system": "http://mimic.mit.edu/fhir/mimic",
                                                           "code": random.choice(["home", "facility", "expired"])}]},
                },
                "identifier": [{"system": "http://mimic.mit.edu/fhir/mimic/sid/hadm",
                                  "value": eid, "use": "usual",
                                  "assigner": rand_ref("Organization", ORG_ID)}],
                "type": [{"coding": [{"system": "http://snomed.info/sct",
                                       "code": "185347001", "display": "Encounter for problem"}]}],
                "priority": {"coding": [{"system": "http://snomed.info/sct",
                                          "code": "394849002", "display": "High priority"}]},
                "serviceProvider": rand_ref("Organization", ORG_ID),
                "serviceType": {"coding": [{"system": "http://snomed.info/sct", "code": "11429006"}]},
                "location": [],
            })
        encounter_map[pid] = enc_ids

        # Conditions
        n_cond = random.randint(1, len(CONDITIONS))
        chosen_conds = random.sample(CONDITIONS, n_cond)
        for code, display in chosen_conds:
            cid = str(uuid.uuid4())[:8]
            all_conditions.append({
                "resourceType": "Condition",
                "id": cid,
                "meta": {"profile": ["http://mimic.mit.edu/fhir/mimic/StructureDefinition/mimic-condition"]},
                "subject": rand_ref("Patient", pid),
                "encounter": rand_ref("Encounter", random.choice(enc_ids)),
                "code": {"coding": [{"system": "http://snomed.info/sct",
                                      "code": code, "display": display}]},
                "category": [{"coding": [{"system": "http://terminology.hl7.org/CodeSystem/condition-category",
                                           "code": "encounter-diagnosis",
                                           "display": "Encounter Diagnosis"}]}],
            })

        # Observations (chart events)
        n_obs = random.randint(5, 40)
        obs_sample = random.choices(OBSERVATIONS, k=n_obs)
        for code, display, lo, hi, unit in obs_sample:
            oid = str(uuid.uuid4())[:8]
            val = round(random.uniform(lo, hi), 1)
            eff_dt = rand_date().strftime("%Y-%m-%dT%H:%M:%SZ")
            all_obs_chart.append({
                "resourceType": "Observation",
                "id": oid,
                "meta": {"profile": ["http://mimic.mit.edu/fhir/mimic/StructureDefinition/mimic-observation-chartevents"]},
                "status": "final",
                "subject": rand_ref("Patient", pid),
                "encounter": rand_ref("Encounter", random.choice(enc_ids)),
                "effectiveDateTime": eff_dt,
                "category": [{"coding": [{"system": "http://terminology.hl7.org/CodeSystem/observation-category",
                                           "code": "vital-signs"}]}],
                "code": {"coding": [{"system": "http://loinc.org",
                                      "code": code, "display": display}]},
                "valueQuantity": {"value": val, "unit": unit,
                                   "system": "http://unitsofmeasure.org", "code": unit},
            })

        # Medications
        n_meds = random.randint(2, 12)
        med_sample = random.choices(MEDICATIONS, k=n_meds)
        for med_code, med_name in med_sample:
            mid = str(uuid.uuid4())[:8]
            eff_dt = rand_date().strftime("%Y-%m-%dT%H:%M:%SZ")
            all_meds.append({
                "resourceType": "MedicationAdministration",
                "id": mid,
                "meta": {"profile": ["http://mimic.mit.edu/fhir/mimic/StructureDefinition/mimic-medication-administration"]},
                "status": "completed",
                "subject": rand_ref("Patient", pid),
                "context": rand_ref("Encounter", random.choice(enc_ids)),
                "effectiveDateTime": eff_dt,
                "medicationCodeableConcept": {
                    "coding": [{"system": "http://hl7.org/fhir/sid/ndc",
                                 "code": med_code}],
                    "text": med_name,
                },
            })

        # Procedures
        n_procs = random.randint(0, 4)
        proc_sample = random.choices(PROCEDURES, k=n_procs)
        for proc_code, proc_name in proc_sample:
            prid = str(uuid.uuid4())[:8]
            all_procs.append({
                "resourceType": "Procedure",
                "id": prid,
                "meta": {"profile": ["http://mimic.mit.edu/fhir/mimic/StructureDefinition/mimic-procedure"]},
                "status": "completed",
                "subject": rand_ref("Patient", pid),
                "encounter": rand_ref("Encounter", random.choice(enc_ids)),
                "code": {"coding": [{"system": "http://snomed.info/sct",
                                      "code": proc_code, "display": proc_name}]},
                "performedDateTime": rand_date().strftime("%Y-%m-%dT%H:%M:%SZ"),
            })

    # Write files
    fhir_dir = base / "fhir"
    write_ndjson(fhir_dir / "MimicPatient.ndjson" / "MimicPatient.ndjson", patients)
    write_ndjson(fhir_dir / "MimicEncounter.ndjson" / "MimicEncounter.ndjson", all_encounters)
    write_ndjson(fhir_dir / "MimicCondition.ndjson" / "MimicCondition.ndjson", all_conditions)
    write_ndjson(fhir_dir / "MimicObservationChartevents.ndjson" / "MimicObservationChartevents.ndjson", all_obs_chart)
    write_ndjson(fhir_dir / "MimicMedicationAdministration.ndjson" / "MimicMedicationAdministration.ndjson", all_meds)
    write_ndjson(fhir_dir / "MimicProcedure.ndjson" / "MimicProcedure.ndjson", all_procs)

    print(f"\n✅ Generated test dataset in '{base}/'")
    print(f"   {len(patients)} patients | {len(all_encounters)} encounters | "
          f"{len(all_conditions)} conditions | {len(all_obs_chart)} observations | "
          f"{len(all_meds)} medications | {len(all_procs)} procedures")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--patients", type=int, default=30)
    parser.add_argument("--out", default="dataset")
    args = parser.parse_args()
    generate(args.patients, args.out)
