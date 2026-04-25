"""
FHIR NDJSON Ingestion Pipeline
Reads all 30 MIMIC-FHIR NDJSON datasets, normalises and merges records
per patient, then stores unified case representations in SQLite.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime, date

logger = logging.getLogger("FHIRIngestion")


# ── Utility helpers ───────────────────────────────────────────────────────────

def read_ndjson(path: Path) -> List[Dict]:
    records = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            for i, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError as e:
                    logger.warning(f"  JSON parse error at line {i} in {path.name}: {e}")
    except FileNotFoundError:
        logger.warning(f"File not found: {path}")
    return records


def extract_patient_id(record: Dict) -> Optional[str]:
    """Resolve 'Patient/XXXX' references to the bare ID."""
    ref = None
    subject = record.get("subject", record.get("patient", {}))
    if isinstance(subject, dict):
        ref = subject.get("reference", "")
    if ref and "Patient/" in ref:
        return ref.split("Patient/")[-1]
    # Fallback: the record IS the patient
    if record.get("resourceType") == "Patient":
        return record.get("id")
    return None


def extract_coding(obj: Dict) -> List[Dict]:
    """Extract coding arrays from FHIR code/category objects."""
    if not obj:
        return []
    codings = obj.get("coding", [])
    result = []
    for c in codings:
        result.append({
            "code":    c.get("code", ""),
            "display": c.get("display", ""),
            "system":  c.get("system", ""),
        })
    return result


def extract_quantity(obj: Dict) -> Optional[Dict]:
    if not obj:
        return None
    return {
        "value": obj.get("value"),
        "unit":  obj.get("unit", ""),
        "code":  obj.get("code", ""),
    }


def parse_date(dt_str: Optional[str]) -> Optional[str]:
    if not dt_str:
        return None
    return dt_str[:10]  # ISO date portion only


# ── Per-resource extractors ───────────────────────────────────────────────────

class PatientExtractor:
    @staticmethod
    def extract(record: Dict) -> Dict:
        gender = record.get("gender", "unknown")
        birth_date = record.get("birthDate", "")
        deceased = record.get("deceasedDateTime")

        # Age in years (approximate)
        age = None
        if birth_date:
            try:
                bd = datetime.strptime(birth_date[:10], "%Y-%m-%d").date()
                today = date.today()
                age = today.year - bd.year - (
                    (today.month, today.day) < (bd.month, bd.day)
                )
            except ValueError:
                pass

        # Marital status
        marital = ""
        ms = record.get("maritalStatus", {})
        if isinstance(ms, dict):
            for c in ms.get("coding", []):
                marital = c.get("code", "")

        # Race / ethnicity from extensions
        race, ethnicity = "", ""
        for ext in record.get("extension", []):
            url = ext.get("url", "")
            if "race" in url.lower():
                for sub in ext.get("extension", []):
                    if sub.get("url") == "text":
                        race = sub.get("valueString", "")
            elif "ethnicity" in url.lower():
                for sub in ext.get("extension", []):
                    if sub.get("url") == "text":
                        ethnicity = sub.get("valueString", "")

        return {
            "patient_id":   record.get("id", ""),
            "gender":       gender,
            "birth_date":   birth_date,
            "age":          age,
            "deceased":     bool(deceased),
            "deceased_date": parse_date(deceased),
            "marital_status": marital,
            "race":         race,
            "ethnicity":    ethnicity,
        }


class ConditionExtractor:
    @staticmethod
    def extract(record: Dict) -> Optional[Dict]:
        patient_id = extract_patient_id(record)
        if not patient_id:
            return None
        code_obj = record.get("code", {})
        codings = extract_coding(code_obj)
        category_codings = []
        for cat in record.get("category", []):
            category_codings.extend(extract_coding(cat))
        encounter_ref = record.get("encounter", {}).get("reference", "")
        return {
            "patient_id":    patient_id,
            "condition_id":  record.get("id", ""),
            "code":          codings[0]["code"] if codings else "",
            "display":       codings[0]["display"] if codings else "",
            "system":        codings[0]["system"] if codings else "",
            "category":      category_codings[0]["code"] if category_codings else "",
            "encounter_ref": encounter_ref,
        }


class EncounterExtractor:
    @staticmethod
    def extract(record: Dict) -> Optional[Dict]:
        patient_id = extract_patient_id(record)
        if not patient_id:
            return None
        period = record.get("period", {})
        class_obj = record.get("class", {})
        hosp = record.get("hospitalization", {})
        admit_src = ""
        disch_disp = ""
        for c in hosp.get("admitSource", {}).get("coding", []):
            admit_src = c.get("code", "")
        for c in hosp.get("dischargeDisposition", {}).get("coding", []):
            disch_disp = c.get("code", "")

        encounter_type_codings = []
        for t in record.get("type", []):
            encounter_type_codings.extend(extract_coding(t))

        return {
            "patient_id":    patient_id,
            "encounter_id":  record.get("id", ""),
            "status":        record.get("status", ""),
            "class_code":    class_obj.get("code", "") if isinstance(class_obj, dict) else "",
            "class_display": class_obj.get("display", "") if isinstance(class_obj, dict) else "",
            "period_start":  parse_date(period.get("start")),
            "period_end":    parse_date(period.get("end")),
            "admit_source":  admit_src,
            "discharge_disp": disch_disp,
            "encounter_type": encounter_type_codings[0]["display"] if encounter_type_codings else "",
        }


class ObservationExtractor:
    @staticmethod
    def extract(record: Dict) -> Optional[Dict]:
        patient_id = extract_patient_id(record)
        if not patient_id:
            return None
        code_obj = record.get("code", {})
        codings = extract_coding(code_obj)
        cat_codings = []
        for cat in record.get("category", []):
            cat_codings.extend(extract_coding(cat))
        value_qty = extract_quantity(record.get("valueQuantity"))
        value_str = record.get("valueString", "")
        return {
            "patient_id":    patient_id,
            "observation_id": record.get("id", ""),
            "code":          codings[0]["code"] if codings else "",
            "display":       codings[0]["display"] if codings else "",
            "category":      cat_codings[0]["code"] if cat_codings else "",
            "effective_dt":  parse_date(record.get("effectiveDateTime")),
            "value_numeric": value_qty["value"] if value_qty else None,
            "value_unit":    value_qty["unit"] if value_qty else "",
            "value_string":  value_str,
            "encounter_ref": record.get("encounter", {}).get("reference", ""),
        }


class MedicationExtractor:
    @staticmethod
    def extract(record: Dict) -> Optional[Dict]:
        patient_id = extract_patient_id(record)
        if not patient_id:
            return None
        med_concept = record.get("medicationCodeableConcept", {})
        codings = extract_coding(med_concept)
        med_display = codings[0]["display"] if codings else ""
        med_code = codings[0]["code"] if codings else ""
        if not med_display:
            med_display = med_concept.get("text", "")
        effective = record.get("effectiveDateTime") or record.get("dateAsserted", "")
        return {
            "patient_id": patient_id,
            "med_id":     record.get("id", ""),
            "resource_type": record.get("resourceType", ""),
            "med_code":   med_code,
            "med_display": med_display,
            "status":     record.get("status", ""),
            "effective_dt": parse_date(effective),
        }


class ProcedureExtractor:
    @staticmethod
    def extract(record: Dict) -> Optional[Dict]:
        patient_id = extract_patient_id(record)
        if not patient_id:
            return None
        code_obj = record.get("code", {})
        codings = extract_coding(code_obj)
        performed = record.get("performedDateTime") or (
            record.get("performedPeriod", {}).get("start", "") if record.get("performedPeriod") else ""
        )
        return {
            "patient_id":   patient_id,
            "procedure_id": record.get("id", ""),
            "code":         codings[0]["code"] if codings else "",
            "display":      codings[0]["display"] if codings else "",
            "status":       record.get("status", ""),
            "performed_dt": parse_date(performed),
        }


# ── Pipeline orchestrator ─────────────────────────────────────────────────────

class FHIRIngestionPipeline:
    def __init__(self, config, db_manager):
        self.config = config
        self.db = db_manager
        self.patients: Dict[str, Dict] = {}
        self.conditions: Dict[str, List] = {}
        self.encounters: Dict[str, List] = {}
        self.observations: Dict[str, List] = {}
        self.medications: Dict[str, List] = {}
        self.procedures: Dict[str, List] = {}

    def run(self):
        logger.info("Starting FHIR ingestion pipeline…")
        self._load_patients()
        self._load_conditions()
        self._load_encounters()
        self._load_observations()
        self._load_medications()
        self._load_procedures()
        self._merge_and_store()
        logger.info(f"Ingestion complete. {self.db.get_case_count()} cases stored.")

    def _load_patients(self):
        path = self.config.find_file(self.config.PATIENT_FILE)
        if not path:
            logger.warning("Patient file not found!")
            return
        records = read_ndjson(path)
        ok, fail = 0, 0
        for r in records:
            try:
                data = PatientExtractor.extract(r)
                if data["patient_id"]:
                    self.patients[data["patient_id"]] = data
                    ok += 1
            except Exception as e:
                logger.debug(f"Patient extract error: {e}")
                fail += 1
        self.db.log_ingestion(path.name, "Patient", ok, fail)
        logger.info(f"  Patients loaded: {ok}")

    def _load_conditions(self):
        paths = self.config.find_files(self.config.CONDITION_FILES)
        total_ok = 0
        for path in paths:
            records = read_ndjson(path)
            ok, fail = 0, 0
            for r in records:
                try:
                    data = ConditionExtractor.extract(r)
                    if data:
                        pid = data["patient_id"]
                        self.conditions.setdefault(pid, []).append(data)
                        ok += 1
                except Exception:
                    fail += 1
            self.db.log_ingestion(path.name, "Condition", ok, fail)
            total_ok += ok
        logger.info(f"  Conditions loaded: {total_ok} from {len(paths)} files")

    def _load_encounters(self):
        paths = self.config.find_files(self.config.ENCOUNTER_FILES)
        total_ok = 0
        for path in paths:
            records = read_ndjson(path)
            ok, fail = 0, 0
            for r in records:
                try:
                    data = EncounterExtractor.extract(r)
                    if data:
                        pid = data["patient_id"]
                        self.encounters.setdefault(pid, []).append(data)
                        ok += 1
                except Exception:
                    fail += 1
            self.db.log_ingestion(path.name, "Encounter", ok, fail)
            total_ok += ok
        logger.info(f"  Encounters loaded: {total_ok} from {len(paths)} files")

    def _load_observations(self):
        paths = self.config.find_files(self.config.OBSERVATION_FILES)
        total_ok = 0
        for path in paths:
            records = read_ndjson(path)
            ok, fail = 0, 0
            for r in records:
                try:
                    data = ObservationExtractor.extract(r)
                    if data:
                        pid = data["patient_id"]
                        self.observations.setdefault(pid, []).append(data)
                        ok += 1
                except Exception:
                    fail += 1
            self.db.log_ingestion(path.name, "Observation", ok, fail)
            total_ok += ok
        logger.info(f"  Observations loaded: {total_ok} from {len(paths)} files")

    def _load_medications(self):
        paths = self.config.find_files(self.config.MEDICATION_FILES)
        total_ok = 0
        for path in paths:
            records = read_ndjson(path)
            ok, fail = 0, 0
            for r in records:
                try:
                    data = MedicationExtractor.extract(r)
                    if data:
                        pid = data["patient_id"]
                        self.medications.setdefault(pid, []).append(data)
                        ok += 1
                except Exception:
                    fail += 1
            self.db.log_ingestion(path.name, "Medication", ok, fail)
            total_ok += ok
        logger.info(f"  Medications loaded: {total_ok} from {len(paths)} files")

    def _load_procedures(self):
        paths = self.config.find_files(self.config.PROCEDURE_FILES)
        total_ok = 0
        for path in paths:
            records = read_ndjson(path)
            ok, fail = 0, 0
            for r in records:
                try:
                    data = ProcedureExtractor.extract(r)
                    if data:
                        pid = data["patient_id"]
                        self.procedures.setdefault(pid, []).append(data)
                        ok += 1
                except Exception:
                    fail += 1
            self.db.log_ingestion(path.name, "Procedure", ok, fail)
            total_ok += ok
        logger.info(f"  Procedures loaded: {total_ok} from {len(paths)} files")

    def _merge_and_store(self):
        """Merge all loaded data per patient and write unified cases to DB."""
        logger.info("Merging records per patient…")
        all_pids = set(self.patients.keys())
        # Also include patients seen only in clinical data
        for d in (self.conditions, self.encounters, self.observations,
                  self.medications, self.procedures):
            all_pids.update(d.keys())

        stored = 0
        for pid in all_pids:
            demo = self.patients.get(pid, {"patient_id": pid})
            conds = self.conditions.get(pid, [])
            encs = self.encounters.get(pid, [])
            obs = self.observations.get(pid, [])
            meds = self.medications.get(pid, [])
            procs = self.procedures.get(pid, [])

            # Summarise observations (top vitals/labs)
            obs_summary = self._summarise_observations(obs)

            # Encounter context summary
            ctx = self._summarise_encounters(encs)

            case_data = {
                "demographic_features": demo,
                "observational_features": obs_summary,
                "condition_features": conds,
                "context_features": ctx,
                "medication_features": meds,
                "procedure_features": procs,
                "encounter_count": len(encs),
                "observation_count": len(obs),
                "condition_count": len(conds),
                "medication_count": len(meds),
                "procedure_count": len(procs),
            }
            self.db.upsert_case(pid, case_data)
            stored += 1

        logger.info(f"  {stored} cases merged and stored.")

    @staticmethod
    def _summarise_observations(obs: List[Dict]) -> Dict:
        """Aggregate numeric observations into category→ {mean, min, max, last}."""
        from collections import defaultdict
        category_values: Dict[str, List[float]] = defaultdict(list)
        category_labels: Dict[str, str] = {}
        for o in obs:
            cat = o.get("category", "unknown")
            display = o.get("display", o.get("code", ""))
            val = o.get("value_numeric")
            if val is not None:
                key = f"{cat}::{display}" if display else cat
                category_values[key].append(float(val))
                category_labels[key] = o.get("value_unit", "")

        summary = {}
        for key, vals in category_values.items():
            summary[key] = {
                "mean": round(sum(vals) / len(vals), 3),
                "min":  round(min(vals), 3),
                "max":  round(max(vals), 3),
                "last": round(vals[-1], 3),
                "unit": category_labels.get(key, ""),
                "count": len(vals),
            }
        return summary

    @staticmethod
    def _summarise_encounters(encs: List[Dict]) -> Dict:
        if not encs:
            return {}
        classes = list({e.get("class_code", "") for e in encs if e.get("class_code")})
        statuses = list({e.get("status", "") for e in encs if e.get("status")})
        discharge_dispositions = [e.get("discharge_disp", "") for e in encs if e.get("discharge_disp")]
        admit_sources = [e.get("admit_source", "") for e in encs if e.get("admit_source")]
        dates = sorted([e.get("period_start", "") for e in encs if e.get("period_start")])
        return {
            "total_encounters": len(encs),
            "encounter_classes": classes,
            "statuses": statuses,
            "first_encounter": dates[0] if dates else None,
            "last_encounter": dates[-1] if dates else None,
            "discharge_dispositions": list(set(discharge_dispositions)),
            "admit_sources": list(set(admit_sources)),
        }
