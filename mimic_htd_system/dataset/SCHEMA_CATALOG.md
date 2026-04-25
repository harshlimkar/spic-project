# FHIR NDJSON Schema Catalog

Generated from 30 NDJSON files.

## Global Structure
Each file is NDJSON (one JSON resource per line). Every dataset has valid JSON lines only (0 invalid lines detected).

## ResourceType: Condition

Common top-level fields across Condition datasets: category, code, encounter, id, meta, resourceType, subject

### Dataset: fhir/MimicCondition.ndjson/MimicCondition.ndjson
- Records: 4506
- Top-level fields: 7
- Required fields (100% present): category, code, encounter, id, meta, resourceType, subject
- Field schema:
  - category: type=array, presence=100.0%
  - code: type=object, presence=100.0%
  - encounter: type=object, presence=100.0%
  - id: type=string, presence=100.0%
  - meta: type=object, presence=100.0%
  - resourceType: type=string, presence=100.0%
  - subject: type=object, presence=100.0%

### Dataset: fhir/MimicConditionED.ndjson/MimicConditionED.ndjson
- Records: 545
- Top-level fields: 7
- Required fields (100% present): category, code, encounter, id, meta, resourceType, subject
- Field schema:
  - category: type=array, presence=100.0%
  - code: type=object, presence=100.0%
  - encounter: type=object, presence=100.0%
  - id: type=string, presence=100.0%
  - meta: type=object, presence=100.0%
  - resourceType: type=string, presence=100.0%
  - subject: type=object, presence=100.0%

## ResourceType: Encounter

Common top-level fields across Encounter datasets: class, id, identifier, meta, period, resourceType, status, subject, type

### Dataset: fhir/MimicEncounter.ndjson/MimicEncounter.ndjson
- Records: 275
- Top-level fields: 14
- Required fields (100% present): class, hospitalization, id, identifier, location, meta, period, priority, resourceType, serviceProvider, serviceType, status, subject, type
- Field schema:
  - class: type=object, presence=100.0%
  - hospitalization: type=object, presence=100.0%
  - id: type=string, presence=100.0%
  - identifier: type=array, presence=100.0%
  - location: type=array, presence=100.0%
  - meta: type=object, presence=100.0%
  - period: type=object, presence=100.0%
  - priority: type=object, presence=100.0%
  - resourceType: type=string, presence=100.0%
  - serviceProvider: type=object, presence=100.0%
  - serviceType: type=object, presence=100.0%
  - status: type=string, presence=100.0%
  - subject: type=object, presence=100.0%
  - type: type=array, presence=100.0%

### Dataset: fhir/MimicEncounterED.ndjson/MimicEncounterED.ndjson
- Records: 222
- Top-level fields: 12
- Required fields (100% present): class, hospitalization, id, identifier, meta, period, resourceType, serviceProvider, status, subject, type
- Field schema:
  - class: type=object, presence=100.0%
  - hospitalization: type=object, presence=100.0%
  - id: type=string, presence=100.0%
  - identifier: type=array, presence=100.0%
  - meta: type=object, presence=100.0%
  - partOf: type=object, presence=77.48%
  - period: type=object, presence=100.0%
  - resourceType: type=string, presence=100.0%
  - serviceProvider: type=object, presence=100.0%
  - status: type=string, presence=100.0%
  - subject: type=object, presence=100.0%
  - type: type=array, presence=100.0%

### Dataset: fhir/MimicLocation.ndjson/MimicEncounterICU.ndjson/MimicEncounterICU.ndjson
- Records: 140
- Top-level fields: 11
- Required fields (100% present): class, id, identifier, location, meta, partOf, period, resourceType, status, subject, type
- Field schema:
  - class: type=object, presence=100.0%
  - id: type=string, presence=100.0%
  - identifier: type=array, presence=100.0%
  - location: type=array, presence=100.0%
  - meta: type=object, presence=100.0%
  - partOf: type=object, presence=100.0%
  - period: type=object, presence=100.0%
  - resourceType: type=string, presence=100.0%
  - status: type=string, presence=100.0%
  - subject: type=object, presence=100.0%
  - type: type=array, presence=100.0%

## ResourceType: Location

Common top-level fields across Location datasets: id, managingOrganization, meta, name, physicalType, resourceType, status

### Dataset: fhir/MimicLocation.ndjson/MimicLocation.ndjson
- Records: 31
- Top-level fields: 7
- Required fields (100% present): id, managingOrganization, meta, name, physicalType, resourceType, status
- Field schema:
  - id: type=string, presence=100.0%
  - managingOrganization: type=object, presence=100.0%
  - meta: type=object, presence=100.0%
  - name: type=string, presence=100.0%
  - physicalType: type=object, presence=100.0%
  - resourceType: type=string, presence=100.0%
  - status: type=string, presence=100.0%

## ResourceType: Medication

Common top-level fields across Medication datasets: id, identifier, meta, resourceType, status

### Dataset: fhir/MimicMedication.ndjson/MimicMedication.ndjson
- Records: 1480
- Top-level fields: 6
- Required fields (100% present): code, id, identifier, meta, resourceType, status
- Field schema:
  - code: type=object, presence=100.0%
  - id: type=string, presence=100.0%
  - identifier: type=array, presence=100.0%
  - meta: type=object, presence=100.0%
  - resourceType: type=string, presence=100.0%
  - status: type=string, presence=100.0%

### Dataset: fhir/MimicMedicationMix.ndjson/MimicMedicationMix.ndjson
- Records: 314
- Top-level fields: 7
- Required fields (100% present): id, identifier, ingredient, meta, resourceType, status, text
- Field schema:
  - id: type=string, presence=100.0%
  - identifier: type=array, presence=100.0%
  - ingredient: type=array, presence=100.0%
  - meta: type=object, presence=100.0%
  - resourceType: type=string, presence=100.0%
  - status: type=string, presence=100.0%
  - text: type=object, presence=100.0%

## ResourceType: MedicationAdministration

Common top-level fields across MedicationAdministration datasets: context, dosage, effectiveDateTime, id, medicationCodeableConcept, meta, resourceType, status, subject

### Dataset: fhir/MimicMedicationAdministration.ndjson/MimicMedicationAdministration.ndjson
- Records: 36131
- Top-level fields: 10
- Required fields (100% present): effectiveDateTime, id, medicationCodeableConcept, meta, resourceType, status, subject
- Field schema:
  - context: type=object, presence=97.07%
  - dosage: type=object, presence=90.01%
  - effectiveDateTime: type=string, presence=100.0%
  - id: type=string, presence=100.0%
  - medicationCodeableConcept: type=object, presence=100.0%
  - meta: type=object, presence=100.0%
  - request: type=object, presence=96.94%
  - resourceType: type=string, presence=100.0%
  - status: type=string, presence=100.0%
  - subject: type=object, presence=100.0%

### Dataset: fhir/MimicMedicationAdministrationICU.ndjson/MimicMedicationAdministrationICU.ndjson
- Records: 20404
- Top-level fields: 11
- Required fields (100% present): category, context, dosage, id, medicationCodeableConcept, meta, resourceType, status, subject
- Field schema:
  - category: type=object, presence=100.0%
  - context: type=object, presence=100.0%
  - dosage: type=object, presence=100.0%
  - effectiveDateTime: type=string, presence=45.9%
  - effectivePeriod: type=object, presence=54.1%
  - id: type=string, presence=100.0%
  - medicationCodeableConcept: type=object, presence=100.0%
  - meta: type=object, presence=100.0%
  - resourceType: type=string, presence=100.0%
  - status: type=string, presence=100.0%
  - subject: type=object, presence=100.0%

## ResourceType: MedicationDispense

Common top-level fields across MedicationDispense datasets: context, id, medicationCodeableConcept, meta, resourceType, status, subject

### Dataset: fhir/MimicMedicationDispense.ndjson/MimicMedicationDispense.ndjson
- Records: 14293
- Top-level fields: 10
- Required fields (100% present): authorizingPrescription, context, id, identifier, medicationCodeableConcept, meta, resourceType, status, subject
- Field schema:
  - authorizingPrescription: type=array, presence=100.0%
  - context: type=object, presence=100.0%
  - dosageInstruction: type=array, presence=99.96%
  - id: type=string, presence=100.0%
  - identifier: type=array, presence=100.0%
  - medicationCodeableConcept: type=object, presence=100.0%
  - meta: type=object, presence=100.0%
  - resourceType: type=string, presence=100.0%
  - status: type=string, presence=100.0%
  - subject: type=object, presence=100.0%

### Dataset: fhir/MimicMedicationDispenseED.ndjson/MimicMedicationDispenseED.ndjson
- Records: 1082
- Top-level fields: 8
- Required fields (100% present): context, id, medicationCodeableConcept, meta, resourceType, status, subject, whenHandedOver
- Field schema:
  - context: type=object, presence=100.0%
  - id: type=string, presence=100.0%
  - medicationCodeableConcept: type=object, presence=100.0%
  - meta: type=object, presence=100.0%
  - resourceType: type=string, presence=100.0%
  - status: type=string, presence=100.0%
  - subject: type=object, presence=100.0%
  - whenHandedOver: type=string, presence=100.0%

## ResourceType: MedicationRequest

Common top-level fields across MedicationRequest datasets: authoredOn, dispenseRequest, dosageInstruction, encounter, id, identifier, intent, medicationCodeableConcept, medicationReference, meta, resourceType, status, subject

### Dataset: fhir/MimicMedicationRequest.ndjson/MimicMedicationRequest.ndjson
- Records: 17552
- Top-level fields: 13
- Required fields (100% present): authoredOn, encounter, id, identifier, intent, meta, resourceType, status, subject
- Field schema:
  - authoredOn: type=string, presence=100.0%
  - dispenseRequest: type=object, presence=83.03%
  - dosageInstruction: type=array, presence=86.71%
  - encounter: type=object, presence=100.0%
  - id: type=string, presence=100.0%
  - identifier: type=array, presence=100.0%
  - intent: type=string, presence=100.0%
  - medicationCodeableConcept: type=object, presence=13.26%
  - medicationReference: type=object, presence=86.74%
  - meta: type=object, presence=100.0%
  - resourceType: type=string, presence=100.0%
  - status: type=string, presence=100.0%
  - subject: type=object, presence=100.0%

## ResourceType: MedicationStatement

Common top-level fields across MedicationStatement datasets: context, dateAsserted, id, medicationCodeableConcept, meta, resourceType, status, subject

### Dataset: fhir/MimicMedicationStatementED.ndjson/MimicMedicationStatementED.ndjson
- Records: 2411
- Top-level fields: 8
- Required fields (100% present): context, dateAsserted, id, medicationCodeableConcept, meta, resourceType, status, subject
- Field schema:
  - context: type=object, presence=100.0%
  - dateAsserted: type=string, presence=100.0%
  - id: type=string, presence=100.0%
  - medicationCodeableConcept: type=object, presence=100.0%
  - meta: type=object, presence=100.0%
  - resourceType: type=string, presence=100.0%
  - status: type=string, presence=100.0%
  - subject: type=object, presence=100.0%

## ResourceType: Observation

Common top-level fields across Observation datasets: category, code, effectiveDateTime, id, meta, resourceType, status, subject

### Dataset: fhir/MimicObservationChartevents.ndjson/MimicObservationChartevents.ndjson
- Records: 668862
- Top-level fields: 13
- Required fields (100% present): category, code, effectiveDateTime, encounter, id, meta, resourceType, status, subject
- Field schema:
  - category: type=array, presence=100.0%
  - code: type=object, presence=100.0%
  - effectiveDateTime: type=string, presence=100.0%
  - encounter: type=object, presence=100.0%
  - id: type=string, presence=100.0%
  - issued: type=string, presence=99.83%
  - meta: type=object, presence=100.0%
  - referenceRange: type=array, presence=2.76%
  - resourceType: type=string, presence=100.0%
  - status: type=string, presence=100.0%
  - subject: type=object, presence=100.0%
  - valueQuantity: type=object, presence=38.49%
  - valueString: type=string, presence=61.51%

### Dataset: fhir/MimicObservationDatetimeevents.ndjson/MimicObservationDatetimeevents.ndjson
- Records: 15280
- Top-level fields: 11
- Required fields (100% present): category, code, effectiveDateTime, encounter, id, issued, meta, resourceType, status, subject, valueDateTime
- Field schema:
  - category: type=array, presence=100.0%
  - code: type=object, presence=100.0%
  - effectiveDateTime: type=string, presence=100.0%
  - encounter: type=object, presence=100.0%
  - id: type=string, presence=100.0%
  - issued: type=string, presence=100.0%
  - meta: type=object, presence=100.0%
  - resourceType: type=string, presence=100.0%
  - status: type=string, presence=100.0%
  - subject: type=object, presence=100.0%
  - valueDateTime: type=string, presence=100.0%

### Dataset: fhir/MimicObservationED.ndjson/MimicObservationED.ndjson
- Records: 2742
- Top-level fields: 12
- Required fields (100% present): category, code, effectiveDateTime, encounter, id, meta, partOf, resourceType, status, subject
- Field schema:
  - category: type=array, presence=100.0%
  - code: type=object, presence=100.0%
  - dataAbsentReason: type=object, presence=48.98%
  - effectiveDateTime: type=string, presence=100.0%
  - encounter: type=object, presence=100.0%
  - id: type=string, presence=100.0%
  - meta: type=object, presence=100.0%
  - partOf: type=array, presence=100.0%
  - resourceType: type=string, presence=100.0%
  - status: type=string, presence=100.0%
  - subject: type=object, presence=100.0%
  - valueString: type=string, presence=51.02%

### Dataset: fhir/MimicObservationLabevents.ndjson/MimicObservationLabevents.ndjson
- Records: 107727
- Top-level fields: 18
- Required fields (100% present): category, code, effectiveDateTime, id, identifier, meta, resourceType, specimen, status, subject
- Field schema:
  - category: type=array, presence=100.0%
  - code: type=object, presence=100.0%
  - dataAbsentReason: type=object, presence=0.0%
  - effectiveDateTime: type=string, presence=100.0%
  - encounter: type=object, presence=73.62%
  - extension: type=array, presence=91.34%
  - id: type=string, presence=100.0%
  - identifier: type=array, presence=100.0%
  - issued: type=string, presence=99.08%
  - meta: type=object, presence=100.0%
  - note: type=array, presence=17.13%
  - referenceRange: type=array, presence=82.62%
  - resourceType: type=string, presence=100.0%
  - specimen: type=object, presence=100.0%
  - status: type=string, presence=100.0%
  - subject: type=object, presence=100.0%
  - valueQuantity: type=object, presence=88.43%
  - valueString: type=string, presence=11.57%

### Dataset: fhir/MimicObservationMicroOrg.ndjson/MimicObservationMicroOrg.ndjson
- Records: 338
- Top-level fields: 11
- Required fields (100% present): category, code, derivedFrom, effectiveDateTime, id, meta, resourceType, status, subject
- Field schema:
  - category: type=array, presence=100.0%
  - code: type=object, presence=100.0%
  - derivedFrom: type=array, presence=100.0%
  - effectiveDateTime: type=string, presence=100.0%
  - hasMember: type=array, presence=35.21%
  - id: type=string, presence=100.0%
  - meta: type=object, presence=100.0%
  - resourceType: type=string, presence=100.0%
  - status: type=string, presence=100.0%
  - subject: type=object, presence=100.0%
  - valueString: type=string, presence=64.79%

### Dataset: fhir/MimicObservationMicroSusc.ndjson/MimicObservationMicroSusc.ndjson
- Records: 1036
- Top-level fields: 13
- Required fields (100% present): category, code, derivedFrom, effectiveDateTime, id, identifier, meta, resourceType, status, subject, valueCodeableConcept
- Field schema:
  - category: type=array, presence=100.0%
  - code: type=object, presence=100.0%
  - derivedFrom: type=array, presence=100.0%
  - effectiveDateTime: type=string, presence=100.0%
  - extension: type=array, presence=96.33%
  - id: type=string, presence=100.0%
  - identifier: type=array, presence=100.0%
  - meta: type=object, presence=100.0%
  - note: type=array, presence=35.91%
  - resourceType: type=string, presence=100.0%
  - status: type=string, presence=100.0%
  - subject: type=object, presence=100.0%
  - valueCodeableConcept: type=object, presence=100.0%

### Dataset: fhir/MimicObservationMicroTest.ndjson/MimicObservationMicroTest.ndjson
- Records: 1893
- Top-level fields: 13
- Required fields (100% present): category, code, effectiveDateTime, id, meta, resourceType, specimen, status, subject
- Field schema:
  - category: type=array, presence=100.0%
  - code: type=object, presence=100.0%
  - effectiveDateTime: type=string, presence=100.0%
  - encounter: type=object, presence=71.58%
  - hasMember: type=array, presence=13.31%
  - id: type=string, presence=100.0%
  - meta: type=object, presence=100.0%
  - resourceType: type=string, presence=100.0%
  - specimen: type=object, presence=100.0%
  - status: type=string, presence=100.0%
  - subject: type=object, presence=100.0%
  - valueCodeableConcept: type=object, presence=7.66%
  - valueString: type=string, presence=79.03%

### Dataset: fhir/MimicObservationOutputevents.ndjson/MimicObservationOutputevents.ndjson
- Records: 9362
- Top-level fields: 11
- Required fields (100% present): category, code, effectiveDateTime, encounter, id, issued, meta, resourceType, status, subject, valueQuantity
- Field schema:
  - category: type=array, presence=100.0%
  - code: type=object, presence=100.0%
  - effectiveDateTime: type=string, presence=100.0%
  - encounter: type=object, presence=100.0%
  - id: type=string, presence=100.0%
  - issued: type=string, presence=100.0%
  - meta: type=object, presence=100.0%
  - resourceType: type=string, presence=100.0%
  - status: type=string, presence=100.0%
  - subject: type=object, presence=100.0%
  - valueQuantity: type=object, presence=100.0%

### Dataset: fhir/MimicObservationVitalSignsED.ndjson/MimicObservationVitalSignsED.ndjson
- Records: 6300
- Top-level fields: 13
- Required fields (100% present): category, code, effectiveDateTime, encounter, id, meta, partOf, resourceType, status, subject
- Field schema:
  - category: type=array, presence=100.0%
  - code: type=object, presence=100.0%
  - component: type=array, presence=20.0%
  - dataAbsentReason: type=object, presence=12.13%
  - effectiveDateTime: type=string, presence=100.0%
  - encounter: type=object, presence=100.0%
  - id: type=string, presence=100.0%
  - meta: type=object, presence=100.0%
  - partOf: type=array, presence=100.0%
  - resourceType: type=string, presence=100.0%
  - status: type=string, presence=100.0%
  - subject: type=object, presence=100.0%
  - valueQuantity: type=object, presence=68.87%

## ResourceType: Organization

Common top-level fields across Organization datasets: active, id, identifier, meta, name, resourceType, type

### Dataset: fhir/MimicOrganization.ndjson/MimicOrganization.ndjson
- Records: 1
- Top-level fields: 7
- Required fields (100% present): active, id, identifier, meta, name, resourceType, type
- Field schema:
  - active: type=boolean, presence=100.0%
  - id: type=string, presence=100.0%
  - identifier: type=array, presence=100.0%
  - meta: type=object, presence=100.0%
  - name: type=string, presence=100.0%
  - resourceType: type=string, presence=100.0%
  - type: type=array, presence=100.0%

## ResourceType: Patient

Common top-level fields across Patient datasets: birthDate, communication, deceasedDateTime, extension, gender, id, identifier, managingOrganization, maritalStatus, meta, name, resourceType

### Dataset: fhir/MimicPatient.ndjson/MimicPatient.ndjson
- Records: 100
- Top-level fields: 12
- Required fields (100% present): birthDate, extension, gender, id, identifier, managingOrganization, maritalStatus, meta, name, resourceType
- Field schema:
  - birthDate: type=string, presence=100.0%
  - communication: type=array, presence=92.0%
  - deceasedDateTime: type=string, presence=31.0%
  - extension: type=array, presence=100.0%
  - gender: type=string, presence=100.0%
  - id: type=string, presence=100.0%
  - identifier: type=array, presence=100.0%
  - managingOrganization: type=object, presence=100.0%
  - maritalStatus: type=object, presence=100.0%
  - meta: type=object, presence=100.0%
  - name: type=array, presence=100.0%
  - resourceType: type=string, presence=100.0%

## ResourceType: Procedure

Common top-level fields across Procedure datasets: code, encounter, id, meta, resourceType, status, subject

### Dataset: fhir/MimicProcedure.ndjson/MimicProcedure.ndjson
- Records: 722
- Top-level fields: 8
- Required fields (100% present): code, encounter, id, meta, performedDateTime, resourceType, status, subject
- Field schema:
  - code: type=object, presence=100.0%
  - encounter: type=object, presence=100.0%
  - id: type=string, presence=100.0%
  - meta: type=object, presence=100.0%
  - performedDateTime: type=string, presence=100.0%
  - resourceType: type=string, presence=100.0%
  - status: type=string, presence=100.0%
  - subject: type=object, presence=100.0%

### Dataset: fhir/MimicProcedureED.ndjson/MimicProcedureED.ndjson
- Records: 1260
- Top-level fields: 8
- Required fields (100% present): code, encounter, id, meta, performedDateTime, resourceType, status, subject
- Field schema:
  - code: type=object, presence=100.0%
  - encounter: type=object, presence=100.0%
  - id: type=string, presence=100.0%
  - meta: type=object, presence=100.0%
  - performedDateTime: type=string, presence=100.0%
  - resourceType: type=string, presence=100.0%
  - status: type=string, presence=100.0%
  - subject: type=object, presence=100.0%

### Dataset: fhir/MimicProcedureICU.ndjson/MimicProcedureICU.ndjson
- Records: 1468
- Top-level fields: 10
- Required fields (100% present): category, code, encounter, id, meta, performedPeriod, resourceType, status, subject
- Field schema:
  - bodySite: type=array, presence=24.05%
  - category: type=object, presence=100.0%
  - code: type=object, presence=100.0%
  - encounter: type=object, presence=100.0%
  - id: type=string, presence=100.0%
  - meta: type=object, presence=100.0%
  - performedPeriod: type=object, presence=100.0%
  - resourceType: type=string, presence=100.0%
  - status: type=string, presence=100.0%
  - subject: type=object, presence=100.0%

## ResourceType: Specimen

Common top-level fields across Specimen datasets: collection, id, identifier, meta, resourceType, subject, type

### Dataset: fhir/MimicSpecimen.ndjson/MimicSpecimen.ndjson
- Records: 1336
- Top-level fields: 7
- Required fields (100% present): id, identifier, meta, resourceType, subject, type
- Field schema:
  - collection: type=object, presence=96.63%
  - id: type=string, presence=100.0%
  - identifier: type=array, presence=100.0%
  - meta: type=object, presence=100.0%
  - resourceType: type=string, presence=100.0%
  - subject: type=object, presence=100.0%
  - type: type=object, presence=100.0%

### Dataset: fhir/MimicSpecimenLab.ndjson/MimicSpecimenLab.ndjson
- Records: 11122
- Top-level fields: 7
- Required fields (100% present): collection, id, identifier, meta, resourceType, subject, type
- Field schema:
  - collection: type=object, presence=100.0%
  - id: type=string, presence=100.0%
  - identifier: type=array, presence=100.0%
  - meta: type=object, presence=100.0%
  - resourceType: type=string, presence=100.0%
  - subject: type=object, presence=100.0%
  - type: type=object, presence=100.0%
