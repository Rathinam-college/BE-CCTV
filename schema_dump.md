# App: Cctv
## Table: cctv_camera (Model: Camera)
| Column Name | Type | Description |
|---|---|---|
| id | BigAutoField |  |
| cameraId | CharField |  |
| name | CharField |  |
| siteName | CharField |  |
| ipAddress | CharField |  |
| dvrNvrDetails | TextField |  |
| warranty | CharField |  |
| status | CharField |  |
| installationDate | DateTimeField |  |
| createdAt | DateTimeField |  |
| updatedAt | DateTimeField |  |
| divisionName | CharField |  |
| block | CharField |  |
| floor | CharField |  |
| room | CharField |  |
| campusZone | CharField |  |
| deviceType | CharField |  |
| brand | CharField |  |
| model | CharField |  |
| serialNumber | CharField |  |
| macAddress | CharField |  |
| index | CharField |  |
| subnetMask | CharField |  |
| gateway | CharField |  |
| portNumber | CharField |  |
| remarks | TextField |  |

## Table: cctv_nvr (Model: NVR)
| Column Name | Type | Description |
|---|---|---|
| id | BigAutoField |  |
| ipAddress | CharField |  |
| subnetMask | CharField |  |
| gateway | CharField |  |
| macAddress | CharField |  |
| portNumber | CharField |  |
| nvrName | CharField |  |
| location | CharField |  |
| brand | CharField |  |
| model | CharField |  |
| hardDisk | CharField |  |
| channel | CharField |  |
| serialNumber | CharField |  |
| status | CharField |  |
| createdAt | DateTimeField |  |
| updatedAt | DateTimeField |  |
| divisionName | CharField |  |
| block | CharField |  |
| floor | CharField |  |
| room | CharField |  |
| campusZone | CharField |  |
| remarks | TextField |  |

## Table: cctv_biometric (Model: Biometric)
| Column Name | Type | Description |
|---|---|---|
| id | BigAutoField |  |
| name | CharField |  |
| location | CharField |  |
| type | CharField |  |
| usage | CharField |  |
| brand | CharField |  |
| model | CharField |  |
| ipAddress | CharField |  |
| subnetMask | CharField |  |
| gateway | CharField |  |
| serverIp | CharField |  |
| serialNumber | CharField |  |
| hardwareSerial | CharField |  |
| macAddress | CharField |  |
| syncStatus | CharField |  |
| lastCheckIn | CharField |  |
| status | CharField |  |
| createdAt | DateTimeField |  |
| updatedAt | DateTimeField |  |
| divisionName | CharField |  |
| block | CharField |  |
| floor | CharField |  |
| room | CharField |  |
| campusZone | CharField |  |
| remarks | TextField |  |

## Table: cctv_barrier (Model: Barrier)
| Column Name | Type | Description |
|---|---|---|
| id | BigAutoField |  |
| name | CharField |  |
| location | CharField |  |
| type | CharField |  |
| gateStatus | CharField |  |
| controller | CharField |  |
| lastUsed | CharField |  |
| status | CharField |  |
| createdAt | DateTimeField |  |
| updatedAt | DateTimeField |  |
| divisionName | CharField |  |
| block | CharField |  |
| floor | CharField |  |
| room | CharField |  |
| campusZone | CharField |  |
| remarks | TextField |  |

## Table: cctv_networkswitch (Model: NetworkSwitch)
| Column Name | Type | Description |
|---|---|---|
| id | BigAutoField |  |
| name | CharField |  |
| ipAddress | CharField |  |
| subnetMask | CharField |  |
| gateway | CharField |  |
| macAddress | CharField |  |
| location | CharField |  |
| brand | CharField |  |
| model | CharField |  |
| portCount | CharField |  |
| ethUplink | CharField |  |
| sfpUplink | CharField |  |
| serialNumber | CharField |  |
| status | CharField |  |
| createdAt | DateTimeField |  |
| updatedAt | DateTimeField |  |
| divisionName | CharField |  |
| block | CharField |  |
| floor | CharField |  |
| room | CharField |  |
| campusZone | CharField |  |
| remarks | TextField |  |

## Table: cctv_activitylog (Model: ActivityLog)
| Column Name | Type | Description |
|---|---|---|
| id | BigAutoField |  |
| user_id | ForeignKey |  -> users_user |
| action | CharField |  |
| page | CharField |  |
| details | TextField |  |
| ipAddress | CharField |  |
| timestamp | DateTimeField |  |

## Table: cctv_cameraremark (Model: CameraRemark)
| Column Name | Type | Description |
|---|---|---|
| id | BigAutoField |  |
| camera_id | ForeignKey |  -> cctv_camera |
| user_id | ForeignKey |  -> users_user |
| remark | TextField |  |
| device_status | CharField |  |
| date | DateField |  |
| time | TimeField |  |
| createdAt | DateTimeField |  |

## Table: cctv_nvrremark (Model: NVRRemark)
| Column Name | Type | Description |
|---|---|---|
| id | BigAutoField |  |
| nvr_id | ForeignKey |  -> cctv_nvr |
| user_id | ForeignKey |  -> users_user |
| remark | TextField |  |
| device_status | CharField |  |
| date | DateField |  |
| time | TimeField |  |
| createdAt | DateTimeField |  |

## Table: cctv_biometricremark (Model: BiometricRemark)
| Column Name | Type | Description |
|---|---|---|
| id | BigAutoField |  |
| biometric_id | ForeignKey |  -> cctv_biometric |
| user_id | ForeignKey |  -> users_user |
| remark | TextField |  |
| device_status | CharField |  |
| date | DateField |  |
| time | TimeField |  |
| createdAt | DateTimeField |  |

## Table: cctv_switchremark (Model: SwitchRemark)
| Column Name | Type | Description |
|---|---|---|
| id | BigAutoField |  |
| switch_id | ForeignKey |  -> cctv_networkswitch |
| user_id | ForeignKey |  -> users_user |
| remark | TextField |  |
| device_status | CharField |  |
| date | DateField |  |
| time | TimeField |  |
| createdAt | DateTimeField |  |

## Table: cctv_camerarelocation (Model: CameraRelocation)
| Column Name | Type | Description |
|---|---|---|
| id | BigAutoField |  |
| camera_id | ForeignKey |  -> cctv_camera |
| user_id | ForeignKey |  -> users_user |
| old_location | CharField |  |
| new_location | CharField |  |
| old_ip | CharField |  |
| new_ip | CharField |  |
| remark | TextField |  |
| createdAt | DateTimeField |  |

## Table: cctv_nvrrelocation (Model: NVRRelocation)
| Column Name | Type | Description |
|---|---|---|
| id | BigAutoField |  |
| nvr_id | ForeignKey |  -> cctv_nvr |
| user_id | ForeignKey |  -> users_user |
| old_location | CharField |  |
| new_location | CharField |  |
| old_ip | CharField |  |
| new_ip | CharField |  |
| remark | TextField |  |
| createdAt | DateTimeField |  |

## Table: cctv_biometricrelocation (Model: BiometricRelocation)
| Column Name | Type | Description |
|---|---|---|
| id | BigAutoField |  |
| biometric_id | ForeignKey |  -> cctv_biometric |
| user_id | ForeignKey |  -> users_user |
| old_location | CharField |  |
| new_location | CharField |  |
| old_ip | CharField |  |
| new_ip | CharField |  |
| remark | TextField |  |
| createdAt | DateTimeField |  |

## Table: cctv_switchrelocation (Model: SwitchRelocation)
| Column Name | Type | Description |
|---|---|---|
| id | BigAutoField |  |
| switch_id | ForeignKey |  -> cctv_networkswitch |
| user_id | ForeignKey |  -> users_user |
| old_location | CharField |  |
| new_location | CharField |  |
| old_ip | CharField |  |
| new_ip | CharField |  |
| remark | TextField |  |
| createdAt | DateTimeField |  |

## Table: cctv_globalsiteconfig (Model: GlobalSiteConfig)
| Column Name | Type | Description |
|---|---|---|
| id | BigAutoField |  |
| divisionName | CharField |  |
| block | CharField |  |
| floor | CharField |  |
| room | CharField |  |
| brand | CharField |  |
| assignedTo_id | ForeignKey |  -> users_user |
| updatedAt | DateTimeField |  |

## Table: cctv_block (Model: Block)
| Column Name | Type | Description |
|---|---|---|
| id | BigAutoField |  |
| name | CharField |  |
| createdAt | DateTimeField |  |

## Table: cctv_floor (Model: Floor)
| Column Name | Type | Description |
|---|---|---|
| id | BigAutoField |  |
| name | CharField |  |
| block_id | ForeignKey |  -> cctv_block |
| createdAt | DateTimeField |  |

## Table: cctv_room (Model: Room)
| Column Name | Type | Description |
|---|---|---|
| id | BigAutoField |  |
| name | CharField |  |
| block_id | ForeignKey |  -> cctv_block |
| floor_id | ForeignKey |  -> cctv_floor |
| createdAt | DateTimeField |  |

## Table: cctv_rack (Model: Rack)
| Column Name | Type | Description |
|---|---|---|
| id | BigAutoField |  |
| name | CharField |  |
| location | CharField |  |
| brand | CharField |  |
| model | CharField |  |
| uSpace | CharField |  |
| serialNumber | CharField |  |
| status | CharField |  |
| createdAt | DateTimeField |  |
| updatedAt | DateTimeField |  |
| divisionName | CharField |  |
| block | CharField |  |
| floor | CharField |  |
| room | CharField |  |
| campusZone | CharField |  |
| remarks | TextField |  |

## Table: cctv_rackremark (Model: RackRemark)
| Column Name | Type | Description |
|---|---|---|
| id | BigAutoField |  |
| rack_id | ForeignKey |  -> cctv_rack |
| user_id | ForeignKey |  -> users_user |
| remark | TextField |  |
| device_status | CharField |  |
| date | DateField |  |
| time | TimeField |  |
| createdAt | DateTimeField |  |

## Table: cctv_rackrelocation (Model: RackRelocation)
| Column Name | Type | Description |
|---|---|---|
| id | BigAutoField |  |
| rack_id | ForeignKey |  -> cctv_rack |
| user_id | ForeignKey |  -> users_user |
| old_location | CharField |  |
| new_location | CharField |  |
| remark | TextField |  |
| createdAt | DateTimeField |  |

## Table: cctv_division (Model: Division)
| Column Name | Type | Description |
|---|---|---|
| id | BigAutoField |  |
| name | CharField |  |
| division_type | CharField |  |
| merged_from | JSONField |  |
| createdAt | DateTimeField |  |

## Table: cctv_brand (Model: Brand)
| Column Name | Type | Description |
|---|---|---|
| id | BigAutoField |  |
| name | CharField |  |
| createdAt | DateTimeField |  |

# App: Maintenance
## Table: maintenance_project (Model: Project)
| Column Name | Type | Description |
|---|---|---|
| id | BigAutoField |  |
| name | CharField |  |
| client_name | CharField |  |
| description | TextField |  |
| start_date | DateField |  |
| end_date | DateField |  |
| status | CharField |  |
| instructionBy | CharField |  |
| bill_number | CharField |  |
| po_number | CharField |  |
| bill_document | FileField |  |
| po_document | FileField |  |
| createdAt | DateTimeField |  |

## Table: maintenance_projectdocument (Model: ProjectDocument)
| Column Name | Type | Description |
|---|---|---|
| id | BigAutoField |  |
| project_id | ForeignKey |  -> maintenance_project |
| name | CharField |  |
| file | FileField |  |
| uploaded_at | DateTimeField |  |

## Table: maintenance_ticket (Model: Ticket)
| Column Name | Type | Description |
|---|---|---|
| id | BigAutoField |  |
| projectId | ForeignKey |  -> maintenance_project |
| cameraId | ForeignKey |  -> cctv_camera |
| raisedBy | ForeignKey |  -> users_user |
| raisedByName | CharField |  |
| assignedTo | ForeignKey |  -> users_user |
| issueDescription | TextField |  |
| status | CharField |  |
| remarks | TextField |  |
| operationDate | DateField |  |
| divisionName | CharField |  |
| block | CharField |  |
| floor | CharField |  |
| room | CharField |  |
| location | CharField |  |
| category | CharField |  |
| ticketDevice | CharField |  |
| actionTaken | TextField |  |
| instructionBy | CharField |  |
| receivedDate | DateField |  |
| receivedTime | CharField |  |
| endTime | CharField |  |
| totalTime | CharField |  |
| serviceImage | FileField |  |
| workImage | FileField |  |
| createdImage | FileField |  |
| createdVideo | FileField |  |
| createdDate | DateField |  |
| createdTime | CharField |  |
| inProgressImage | FileField |  |
| inProgressVideo | FileField |  |
| inProgressDate | DateField |  |
| inProgressTime | CharField |  |
| completedImage | FileField |  |
| completedVideo | FileField |  |
| completedDate | DateField |  |
| completedTime | CharField |  |
| workRemarks | TextField |  |
| replacedParts | TextField |  |
| nextServiceDate | DateTimeField |  |
| bill_number | CharField |  |
| po_number | CharField |  |
| bill_document | FileField |  |
| po_document | FileField |  |
| createdAt | DateTimeField |  |
| updatedAt | DateTimeField |  |

## Table: maintenance_ticketremark (Model: TicketRemark)
| Column Name | Type | Description |
|---|---|---|
| id | BigAutoField |  |
| ticket_id | ForeignKey |  -> maintenance_ticket |
| remark | TextField |  |
| image | FileField |  |
| device_status | CharField |  |
| date | DateField |  |
| time | TimeField |  |
| user_id | ForeignKey |  -> users_user |
| createdAt | DateTimeField |  |

## Table: maintenance_ticketdocument (Model: TicketDocument)
| Column Name | Type | Description |
|---|---|---|
| id | BigAutoField |  |
| ticket_id | ForeignKey |  -> maintenance_ticket |
| name | CharField |  |
| file | FileField |  |
| uploaded_at | DateTimeField |  |

## Table: maintenance_ticketcompletedimage (Model: TicketCompletedImage)
| Column Name | Type | Description |
|---|---|---|
| id | BigAutoField |  |
| ticket_id | ForeignKey |  -> maintenance_ticket |
| image | FileField |  |
| uploaded_at | DateTimeField |  |

## Table: maintenance_generalbillinginfo (Model: GeneralBillingInfo)
| Column Name | Type | Description |
|---|---|---|
| id | BigAutoField |  |
| work | CharField |  |
| location | CharField |  |
| area_budget | CharField |  |
| vendor_name | CharField |  |
| bill_no | CharField |  |
| bill_date | DateField |  |
| amount | CharField |  |
| bill_status | CharField |  |
| pr_no | CharField |  |
| po_no | CharField |  |
| po_value | CharField |  |
| opex_no | CharField |  |
| opex_value | CharField |  |
| opex_status | CharField |  |
| payment_status | CharField |  |
| handover_to | CharField |  |
| bill_document | FileField |  |
| po_document | FileField |  |
| createdAt | DateTimeField |  |

## Table: maintenance_generalbillingdocument (Model: GeneralBillingDocument)
| Column Name | Type | Description |
|---|---|---|
| id | BigAutoField |  |
| general_billing_id | ForeignKey |  -> maintenance_generalbillinginfo |
| name | CharField |  |
| file | FileField |  |
| uploaded_at | DateTimeField |  |

## Table: maintenance_projectbillingrecord (Model: ProjectBillingRecord)
| Column Name | Type | Description |
|---|---|---|
| id | BigAutoField |  |
| project_id | ForeignKey |  -> maintenance_project |
| record_type | CharField |  |
| number | CharField |  |
| amount | CharField |  |
| file | FileField |  |
| uploaded_at | DateTimeField |  |

## Table: maintenance_ticketbillingrecord (Model: TicketBillingRecord)
| Column Name | Type | Description |
|---|---|---|
| id | BigAutoField |  |
| ticket_id | ForeignKey |  -> maintenance_ticket |
| record_type | CharField |  |
| number | CharField |  |
| amount | CharField |  |
| file | FileField |  |
| uploaded_at | DateTimeField |  |

# App: Users
## Table: users_user (Model: User)
| Column Name | Type | Description |
|---|---|---|
| id | BigAutoField |  |
| password | CharField |  |
| last_login | DateTimeField |  |
| is_superuser | BooleanField |  |
| first_name | CharField |  |
| last_name | CharField |  |
| is_staff | BooleanField |  |
| is_active | BooleanField |  |
| date_joined | DateTimeField |  |
| email | CharField |  |
| name | CharField |  |
| role | CharField |  |
| branch | CharField |  |
| permissions | JSONField |  |
| raw_password | CharField |  |
