# NDJSON Schema Summary (FHIR Datasets)

- Dataset files analyzed: 30

## fhir/MimicCondition.ndjson/MimicCondition.ndjson
- Records: 4506
- Invalid JSON lines: 0
- Top-level field count: 7
- Top-level fields:
  - category: array (present 4506/4506 = 100.0%)
  - code: object (present 4506/4506 = 100.0%)
  - encounter: object (present 4506/4506 = 100.0%)
  - id: string (present 4506/4506 = 100.0%)
  - meta: object (present 4506/4506 = 100.0%)
  - resourceType: string (present 4506/4506 = 100.0%)
  - subject: object (present 4506/4506 = 100.0%)

## fhir/MimicConditionED.ndjson/MimicConditionED.ndjson
- Records: 545
- Invalid JSON lines: 0
- Top-level field count: 7
- Top-level fields:
  - category: array (present 545/545 = 100.0%)
  - code: object (present 545/545 = 100.0%)
  - encounter: object (present 545/545 = 100.0%)
  - id: string (present 545/545 = 100.0%)
  - meta: object (present 545/545 = 100.0%)
  - resourceType: string (present 545/545 = 100.0%)
  - subject: object (present 545/545 = 100.0%)

## fhir/MimicEncounter.ndjson/MimicEncounter.ndjson
- Records: 275
- Invalid JSON lines: 0
- Top-level field count: 14
- Top-level fields:
  - class: object (present 275/275 = 100.0%)
  - hospitalization: object (present 275/275 = 100.0%)
  - id: string (present 275/275 = 100.0%)
  - identifier: array (present 275/275 = 100.0%)
  - location: array (present 275/275 = 100.0%)
  - meta: object (present 275/275 = 100.0%)
  - period: object (present 275/275 = 100.0%)
  - priority: object (present 275/275 = 100.0%)
  - resourceType: string (present 275/275 = 100.0%)
  - serviceProvider: object (present 275/275 = 100.0%)
  - serviceType: object (present 275/275 = 100.0%)
  - status: string (present 275/275 = 100.0%)
  - subject: object (present 275/275 = 100.0%)
  - type: array (present 275/275 = 100.0%)

## fhir/MimicEncounterED.ndjson/MimicEncounterED.ndjson
- Records: 222
- Invalid JSON lines: 0
- Top-level field count: 12
- Top-level fields:
  - class: object (present 222/222 = 100.0%)
  - hospitalization: object (present 222/222 = 100.0%)
  - id: string (present 222/222 = 100.0%)
  - identifier: array (present 222/222 = 100.0%)
  - meta: object (present 222/222 = 100.0%)
  - partOf: object (present 172/222 = 77.48%)
  - period: object (present 222/222 = 100.0%)
  - resourceType: string (present 222/222 = 100.0%)
  - serviceProvider: object (present 222/222 = 100.0%)
  - status: string (present 222/222 = 100.0%)
  - subject: object (present 222/222 = 100.0%)
  - type: array (present 222/222 = 100.0%)

## fhir/MimicLocation.ndjson/MimicEncounterICU.ndjson/MimicEncounterICU.ndjson
- Records: 140
- Invalid JSON lines: 0
- Top-level field count: 11
- Top-level fields:
  - class: object (present 140/140 = 100.0%)
  - id: string (present 140/140 = 100.0%)
  - identifier: array (present 140/140 = 100.0%)
  - location: array (present 140/140 = 100.0%)
  - meta: object (present 140/140 = 100.0%)
  - partOf: object (present 140/140 = 100.0%)
  - period: object (present 140/140 = 100.0%)
  - resourceType: string (present 140/140 = 100.0%)
  - status: string (present 140/140 = 100.0%)
  - subject: object (present 140/140 = 100.0%)
  - type: array (present 140/140 = 100.0%)

## fhir/MimicLocation.ndjson/MimicLocation.ndjson
- Records: 31
- Invalid JSON lines: 0
- Top-level field count: 7
- Top-level fields:
  - id: string (present 31/31 = 100.0%)
  - managingOrganization: object (present 31/31 = 100.0%)
  - meta: object (present 31/31 = 100.0%)
  - name: string (present 31/31 = 100.0%)
  - physicalType: object (present 31/31 = 100.0%)
  - resourceType: string (present 31/31 = 100.0%)
  - status: string (present 31/31 = 100.0%)

## fhir/MimicMedication.ndjson/MimicMedication.ndjson
- Records: 1480
- Invalid JSON lines: 0
- Top-level field count: 6
- Top-level fields:
  - code: object (present 1480/1480 = 100.0%)
  - id: string (present 1480/1480 = 100.0%)
  - identifier: array (present 1480/1480 = 100.0%)
  - meta: object (present 1480/1480 = 100.0%)
  - resourceType: string (present 1480/1480 = 100.0%)
  - status: string (present 1480/1480 = 100.0%)

## fhir/MimicMedicationAdministration.ndjson/MimicMedicationAdministration.ndjson
- Records: 36131
- Invalid JSON lines: 0
- Top-level field count: 10
- Top-level fields:
  - context: object (present 35072/36131 = 97.07%)
  - dosage: object (present 32523/36131 = 90.01%)
  - effectiveDateTime: string (present 36131/36131 = 100.0%)
  - id: string (present 36131/36131 = 100.0%)
  - medicationCodeableConcept: object (present 36131/36131 = 100.0%)
  - meta: object (present 36131/36131 = 100.0%)
  - request: object (present 35026/36131 = 96.94%)
  - resourceType: string (present 36131/36131 = 100.0%)
  - status: string (present 36131/36131 = 100.0%)
  - subject: object (present 36131/36131 = 100.0%)

## fhir/MimicMedicationAdministrationICU.ndjson/MimicMedicationAdministrationICU.ndjson
- Records: 20404
- Invalid JSON lines: 0
- Top-level field count: 11
- Top-level fields:
  - category: object (present 20404/20404 = 100.0%)
  - context: object (present 20404/20404 = 100.0%)
  - dosage: object (present 20404/20404 = 100.0%)
  - effectiveDateTime: string (present 9366/20404 = 45.9%)
  - effectivePeriod: object (present 11038/20404 = 54.1%)
  - id: string (present 20404/20404 = 100.0%)
  - medicationCodeableConcept: object (present 20404/20404 = 100.0%)
  - meta: object (present 20404/20404 = 100.0%)
  - resourceType: string (present 20404/20404 = 100.0%)
  - status: string (present 20404/20404 = 100.0%)
  - subject: object (present 20404/20404 = 100.0%)

## fhir/MimicMedicationDispense.ndjson/MimicMedicationDispense.ndjson
- Records: 14293
- Invalid JSON lines: 0
- Top-level field count: 10
- Top-level fields:
  - authorizingPrescription: array (present 14293/14293 = 100.0%)
  - context: object (present 14293/14293 = 100.0%)
  - dosageInstruction: array (present 14287/14293 = 99.96%)
  - id: string (present 14293/14293 = 100.0%)
  - identifier: array (present 14293/14293 = 100.0%)
  - medicationCodeableConcept: object (present 14293/14293 = 100.0%)
  - meta: object (present 14293/14293 = 100.0%)
  - resourceType: string (present 14293/14293 = 100.0%)
  - status: string (present 14293/14293 = 100.0%)
  - subject: object (present 14293/14293 = 100.0%)

## fhir/MimicMedicationDispenseED.ndjson/MimicMedicationDispenseED.ndjson
- Records: 1082
- Invalid JSON lines: 0
- Top-level field count: 8
- Top-level fields:
  - context: object (present 1082/1082 = 100.0%)
  - id: string (present 1082/1082 = 100.0%)
  - medicationCodeableConcept: object (present 1082/1082 = 100.0%)
  - meta: object (present 1082/1082 = 100.0%)
  - resourceType: string (present 1082/1082 = 100.0%)
  - status: string (present 1082/1082 = 100.0%)
  - subject: object (present 1082/1082 = 100.0%)
  - whenHandedOver: string (present 1082/1082 = 100.0%)

## fhir/MimicMedicationMix.ndjson/MimicMedicationMix.ndjson
- Records: 314
- Invalid JSON lines: 0
- Top-level field count: 7
- Top-level fields:
  - id: string (present 314/314 = 100.0%)
  - identifier: array (present 314/314 = 100.0%)
  - ingredient: array (present 314/314 = 100.0%)
  - meta: object (present 314/314 = 100.0%)
  - resourceType: string (present 314/314 = 100.0%)
  - status: string (present 314/314 = 100.0%)
  - text: object (present 314/314 = 100.0%)

## fhir/MimicMedicationRequest.ndjson/MimicMedicationRequest.ndjson
- Records: 17552
- Invalid JSON lines: 0
- Top-level field count: 13
- Top-level fields:
  - authoredOn: string (present 17552/17552 = 100.0%)
  - dispenseRequest: object (present 14574/17552 = 83.03%)
  - dosageInstruction: array (present 15219/17552 = 86.71%)
  - encounter: object (present 17552/17552 = 100.0%)
  - id: string (present 17552/17552 = 100.0%)
  - identifier: array (present 17552/17552 = 100.0%)
  - intent: string (present 17552/17552 = 100.0%)
  - medicationCodeableConcept: object (present 2327/17552 = 13.26%)
  - medicationReference: object (present 15225/17552 = 86.74%)
  - meta: object (present 17552/17552 = 100.0%)
  - resourceType: string (present 17552/17552 = 100.0%)
  - status: string (present 17552/17552 = 100.0%)
  - subject: object (present 17552/17552 = 100.0%)

## fhir/MimicMedicationStatementED.ndjson/MimicMedicationStatementED.ndjson
- Records: 2411
- Invalid JSON lines: 0
- Top-level field count: 8
- Top-level fields:
  - context: object (present 2411/2411 = 100.0%)
  - dateAsserted: string (present 2411/2411 = 100.0%)
  - id: string (present 2411/2411 = 100.0%)
  - medicationCodeableConcept: object (present 2411/2411 = 100.0%)
  - meta: object (present 2411/2411 = 100.0%)
  - resourceType: string (present 2411/2411 = 100.0%)
  - status: string (present 2411/2411 = 100.0%)
  - subject: object (present 2411/2411 = 100.0%)

## fhir/MimicObservationChartevents.ndjson/MimicObservationChartevents.ndjson
- Records: 668862
- Invalid JSON lines: 0
- Top-level field count: 13
- Top-level fields:
  - category: array (present 668862/668862 = 100.0%)
  - code: object (present 668862/668862 = 100.0%)
  - effectiveDateTime: string (present 668862/668862 = 100.0%)
  - encounter: object (present 668862/668862 = 100.0%)
  - id: string (present 668862/668862 = 100.0%)
  - issued: string (present 667703/668862 = 99.83%)
  - meta: object (present 668862/668862 = 100.0%)
  - referenceRange: array (present 18473/668862 = 2.76%)
  - resourceType: string (present 668862/668862 = 100.0%)
  - status: string (present 668862/668862 = 100.0%)
  - subject: object (present 668862/668862 = 100.0%)
  - valueQuantity: object (present 257474/668862 = 38.49%)
  - valueString: string (present 411388/668862 = 61.51%)

## fhir/MimicObservationDatetimeevents.ndjson/MimicObservationDatetimeevents.ndjson
- Records: 15280
- Invalid JSON lines: 0
- Top-level field count: 11
- Top-level fields:
  - category: array (present 15280/15280 = 100.0%)
  - code: object (present 15280/15280 = 100.0%)
  - effectiveDateTime: string (present 15280/15280 = 100.0%)
  - encounter: object (present 15280/15280 = 100.0%)
  - id: string (present 15280/15280 = 100.0%)
  - issued: string (present 15280/15280 = 100.0%)
  - meta: object (present 15280/15280 = 100.0%)
  - resourceType: string (present 15280/15280 = 100.0%)
  - status: string (present 15280/15280 = 100.0%)
  - subject: object (present 15280/15280 = 100.0%)
  - valueDateTime: string (present 15280/15280 = 100.0%)

## fhir/MimicObservationED.ndjson/MimicObservationED.ndjson
- Records: 2742
- Invalid JSON lines: 0
- Top-level field count: 12
- Top-level fields:
  - category: array (present 2742/2742 = 100.0%)
  - code: object (present 2742/2742 = 100.0%)
  - dataAbsentReason: object (present 1343/2742 = 48.98%)
  - effectiveDateTime: string (present 2742/2742 = 100.0%)
  - encounter: object (present 2742/2742 = 100.0%)
  - id: string (present 2742/2742 = 100.0%)
  - meta: object (present 2742/2742 = 100.0%)
  - partOf: array (present 2742/2742 = 100.0%)
  - resourceType: string (present 2742/2742 = 100.0%)
  - status: string (present 2742/2742 = 100.0%)
  - subject: object (present 2742/2742 = 100.0%)
  - valueString: string (present 1399/2742 = 51.02%)

## fhir/MimicObservationLabevents.ndjson/MimicObservationLabevents.ndjson
- Records: 107727
- Invalid JSON lines: 0
- Top-level field count: 18
- Top-level fields:
  - category: array (present 107727/107727 = 100.0%)
  - code: object (present 107727/107727 = 100.0%)
  - dataAbsentReason: object (present 2/107727 = 0.0%)
  - effectiveDateTime: string (present 107727/107727 = 100.0%)
  - encounter: object (present 79307/107727 = 73.62%)
  - extension: array (present 98398/107727 = 91.34%)
  - id: string (present 107727/107727 = 100.0%)
  - identifier: array (present 107727/107727 = 100.0%)
  - issued: string (present 106735/107727 = 99.08%)
  - meta: object (present 107727/107727 = 100.0%)
  - note: array (present 18454/107727 = 17.13%)
  - referenceRange: array (present 88999/107727 = 82.62%)
  - resourceType: string (present 107727/107727 = 100.0%)
  - specimen: object (present 107727/107727 = 100.0%)
  - status: string (present 107727/107727 = 100.0%)
  - subject: object (present 107727/107727 = 100.0%)
  - valueQuantity: object (present 95258/107727 = 88.43%)
  - valueString: string (present 12467/107727 = 11.57%)

## fhir/MimicObservationMicroOrg.ndjson/MimicObservationMicroOrg.ndjson
- Records: 338
- Invalid JSON lines: 0
- Top-level field count: 11
- Top-level fields:
  - category: array (present 338/338 = 100.0%)
  - code: object (present 338/338 = 100.0%)
  - derivedFrom: array (present 338/338 = 100.0%)
  - effectiveDateTime: string (present 338/338 = 100.0%)
  - hasMember: array (present 119/338 = 35.21%)
  - id: string (present 338/338 = 100.0%)
  - meta: object (present 338/338 = 100.0%)
  - resourceType: string (present 338/338 = 100.0%)
  - status: string (present 338/338 = 100.0%)
  - subject: object (present 338/338 = 100.0%)
  - valueString: string (present 219/338 = 64.79%)

## fhir/MimicObservationMicroSusc.ndjson/MimicObservationMicroSusc.ndjson
- Records: 1036
- Invalid JSON lines: 0
- Top-level field count: 13
- Top-level fields:
  - category: array (present 1036/1036 = 100.0%)
  - code: object (present 1036/1036 = 100.0%)
  - derivedFrom: array (present 1036/1036 = 100.0%)
  - effectiveDateTime: string (present 1036/1036 = 100.0%)
  - extension: array (present 998/1036 = 96.33%)
  - id: string (present 1036/1036 = 100.0%)
  - identifier: array (present 1036/1036 = 100.0%)
  - meta: object (present 1036/1036 = 100.0%)
  - note: array (present 372/1036 = 35.91%)
  - resourceType: string (present 1036/1036 = 100.0%)
  - status: string (present 1036/1036 = 100.0%)
  - subject: object (present 1036/1036 = 100.0%)
  - valueCodeableConcept: object (present 1036/1036 = 100.0%)

## fhir/MimicObservationMicroTest.ndjson/MimicObservationMicroTest.ndjson
- Records: 1893
- Invalid JSON lines: 0
- Top-level field count: 13
- Top-level fields:
  - category: array (present 1893/1893 = 100.0%)
  - code: object (present 1893/1893 = 100.0%)
  - effectiveDateTime: string (present 1893/1893 = 100.0%)
  - encounter: object (present 1355/1893 = 71.58%)
  - hasMember: array (present 252/1893 = 13.31%)
  - id: string (present 1893/1893 = 100.0%)
  - meta: object (present 1893/1893 = 100.0%)
  - resourceType: string (present 1893/1893 = 100.0%)
  - specimen: object (present 1893/1893 = 100.0%)
  - status: string (present 1893/1893 = 100.0%)
  - subject: object (present 1893/1893 = 100.0%)
  - valueCodeableConcept: object (present 145/1893 = 7.66%)
  - valueString: string (present 1496/1893 = 79.03%)

## fhir/MimicObservationOutputevents.ndjson/MimicObservationOutputevents.ndjson
- Records: 9362
- Invalid JSON lines: 0
- Top-level field count: 11
- Top-level fields:
  - category: array (present 9362/9362 = 100.0%)
  - code: object (present 9362/9362 = 100.0%)
  - effectiveDateTime: string (present 9362/9362 = 100.0%)
  - encounter: object (present 9362/9362 = 100.0%)
  - id: string (present 9362/9362 = 100.0%)
  - issued: string (present 9362/9362 = 100.0%)
  - meta: object (present 9362/9362 = 100.0%)
  - resourceType: string (present 9362/9362 = 100.0%)
  - status: string (present 9362/9362 = 100.0%)
  - subject: object (present 9362/9362 = 100.0%)
  - valueQuantity: object (present 9362/9362 = 100.0%)

## fhir/MimicObservationVitalSignsED.ndjson/MimicObservationVitalSignsED.ndjson
- Records: 6300
- Invalid JSON lines: 0
- Top-level field count: 13
- Top-level fields:
  - category: array (present 6300/6300 = 100.0%)
  - code: object (present 6300/6300 = 100.0%)
  - component: array (present 1260/6300 = 20.0%)
  - dataAbsentReason: object (present 764/6300 = 12.13%)
  - effectiveDateTime: string (present 6300/6300 = 100.0%)
  - encounter: object (present 6300/6300 = 100.0%)
  - id: string (present 6300/6300 = 100.0%)
  - meta: object (present 6300/6300 = 100.0%)
  - partOf: array (present 6300/6300 = 100.0%)
  - resourceType: string (present 6300/6300 = 100.0%)
  - status: string (present 6300/6300 = 100.0%)
  - subject: object (present 6300/6300 = 100.0%)
  - valueQuantity: object (present 4339/6300 = 68.87%)

## fhir/MimicOrganization.ndjson/MimicOrganization.ndjson
- Records: 1
- Invalid JSON lines: 0
- Top-level field count: 7
- Top-level fields:
  - active: boolean (present 1/1 = 100.0%)
  - id: string (present 1/1 = 100.0%)
  - identifier: array (present 1/1 = 100.0%)
  - meta: object (present 1/1 = 100.0%)
  - name: string (present 1/1 = 100.0%)
  - resourceType: string (present 1/1 = 100.0%)
  - type: array (present 1/1 = 100.0%)

## fhir/MimicPatient.ndjson/MimicPatient.ndjson
- Records: 100
- Invalid JSON lines: 0
- Top-level field count: 12
- Top-level fields:
  - birthDate: string (present 100/100 = 100.0%)
  - communication: array (present 92/100 = 92.0%)
  - deceasedDateTime: string (present 31/100 = 31.0%)
  - extension: array (present 100/100 = 100.0%)
  - gender: string (present 100/100 = 100.0%)
  - id: string (present 100/100 = 100.0%)
  - identifier: array (present 100/100 = 100.0%)
  - managingOrganization: object (present 100/100 = 100.0%)
  - maritalStatus: object (present 100/100 = 100.0%)
  - meta: object (present 100/100 = 100.0%)
  - name: array (present 100/100 = 100.0%)
  - resourceType: string (present 100/100 = 100.0%)

## fhir/MimicProcedure.ndjson/MimicProcedure.ndjson
- Records: 722
- Invalid JSON lines: 0
- Top-level field count: 8
- Top-level fields:
  - code: object (present 722/722 = 100.0%)
  - encounter: object (present 722/722 = 100.0%)
  - id: string (present 722/722 = 100.0%)
  - meta: object (present 722/722 = 100.0%)
  - performedDateTime: string (present 722/722 = 100.0%)
  - resourceType: string (present 722/722 = 100.0%)
  - status: string (present 722/722 = 100.0%)
  - subject: object (present 722/722 = 100.0%)

## fhir/MimicProcedureED.ndjson/MimicProcedureED.ndjson
- Records: 1260
- Invalid JSON lines: 0
- Top-level field count: 8
- Top-level fields:
  - code: object (present 1260/1260 = 100.0%)
  - encounter: object (present 1260/1260 = 100.0%)
  - id: string (present 1260/1260 = 100.0%)
  - meta: object (present 1260/1260 = 100.0%)
  - performedDateTime: string (present 1260/1260 = 100.0%)
  - resourceType: string (present 1260/1260 = 100.0%)
  - status: string (present 1260/1260 = 100.0%)
  - subject: object (present 1260/1260 = 100.0%)

## fhir/MimicProcedureICU.ndjson/MimicProcedureICU.ndjson
- Records: 1468
- Invalid JSON lines: 0
- Top-level field count: 10
- Top-level fields:
  - bodySite: array (present 353/1468 = 24.05%)
  - category: object (present 1468/1468 = 100.0%)
  - code: object (present 1468/1468 = 100.0%)
  - encounter: object (present 1468/1468 = 100.0%)
  - id: string (present 1468/1468 = 100.0%)
  - meta: object (present 1468/1468 = 100.0%)
  - performedPeriod: object (present 1468/1468 = 100.0%)
  - resourceType: string (present 1468/1468 = 100.0%)
  - status: string (present 1468/1468 = 100.0%)
  - subject: object (present 1468/1468 = 100.0%)

## fhir/MimicSpecimen.ndjson/MimicSpecimen.ndjson
- Records: 1336
- Invalid JSON lines: 0
- Top-level field count: 7
- Top-level fields:
  - collection: object (present 1291/1336 = 96.63%)
  - id: string (present 1336/1336 = 100.0%)
  - identifier: array (present 1336/1336 = 100.0%)
  - meta: object (present 1336/1336 = 100.0%)
  - resourceType: string (present 1336/1336 = 100.0%)
  - subject: object (present 1336/1336 = 100.0%)
  - type: object (present 1336/1336 = 100.0%)

## fhir/MimicSpecimenLab.ndjson/MimicSpecimenLab.ndjson
- Records: 11122
- Invalid JSON lines: 0
- Top-level field count: 7
- Top-level fields:
  - collection: object (present 11122/11122 = 100.0%)
  - id: string (present 11122/11122 = 100.0%)
  - identifier: array (present 11122/11122 = 100.0%)
  - meta: object (present 11122/11122 = 100.0%)
  - resourceType: string (present 11122/11122 = 100.0%)
  - subject: object (present 11122/11122 = 100.0%)
  - type: object (present 11122/11122 = 100.0%)
