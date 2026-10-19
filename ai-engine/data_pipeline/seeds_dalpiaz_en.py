"""
seeds_dalpiaz_en.py
Koleksi benih User Story alami (Natural) Bahasa Inggris dari repositori domain publik Dalpiaz et al.
Mencakup proyek: OpenGov, FAA, CMS, SmartHome, University, Healthcare, E-Commerce, Logistics, etc.
"""

DALPIAZ_ENGLISH_SEEDS = [
    # G01 / G03 - Open Government & Transparency
    {"source_id": "dalpiaz_opengov_001", "text": "As a citizen, I want to search federal spending by agency, so that I can monitor how tax dollars are allocated."},
    {"source_id": "dalpiaz_opengov_002", "text": "As a journalist, I want to download grant recipient data in CSV format, so that I can conduct investigative reporting."},
    {"source_id": "dalpiaz_opengov_003", "text": "As a researcher, I want to view historical contract awards on a timeline, so that I can analyze procurement trends."},
    {"source_id": "dalpiaz_opengov_004", "text": "As an auditor, I want to filter fiscal transactions by date range, so that I can verify quarterly compliance reports."},
    {"source_id": "dalpiaz_opengov_005", "text": "As a taxpayer, I want to see a visual breakdown of the national budget, so that I understand government priorities."},

    # G02 - Federal Aviation Administration & Safety
    {"source_id": "dalpiaz_faa_006", "text": "As a pilot, I want to receive real-time weather radar updates, so that I can navigate around severe storm cells."},
    {"source_id": "dalpiaz_faa_007", "text": "As an air traffic controller, I want to view aircraft altitude deviations immediately, so that I can prevent airspace conflicts."},
    {"source_id": "dalpiaz_faa_008", "text": "As a flight dispatcher, I want to submit flight plans electronically, so that route clearances are processed before takeoff."},
    {"source_id": "dalpiaz_faa_009", "text": "As an airport safety officer, I want to log runway inspection results, so that maintenance crews address pavement cracks."},
    {"source_id": "dalpiaz_faa_010", "text": "As an aviation inspector, I want to review aircraft maintenance logs, so that I confirm mechanical airworthiness."},

    # G04 / G08 - Smart Home & IoT
    {"source_id": "dalpiaz_iot_011", "text": "As a homeowner, I want to schedule thermostat temperature changes by hour, so that I reduce energy consumption when away."},
    {"source_id": "dalpiaz_iot_012", "text": "As a resident, I want to receive push notifications when motion is detected at the front door, so that I know when visitors arrive."},
    {"source_id": "dalpiaz_iot_013", "text": "As a user, I want to lock all exterior doors with a single tap, so that my home is secured before sleeping."},
    {"source_id": "dalpiaz_iot_014", "text": "As a homeowner, I want to monitor daily kilowatt-hour electricity consumption, so that I can lower utility expenses."},
    {"source_id": "dalpiaz_iot_015", "text": "As a tenant, I want to grant temporary digital keypad access to delivery couriers, so that packages are safely placed inside."},

    # G10 - University Management & Student Portal
    {"source_id": "dalpiaz_univ_016", "text": "As a student, I want to register for required semester courses online, so that I secure seats in prerequisite classes."},
    {"source_id": "dalpiaz_univ_017", "text": "As a professor, I want to upload lecture slides in PDF format, so that students can prepare before seminar sessions."},
    {"source_id": "dalpiaz_univ_018", "text": "As an academic advisor, I want to view student credit progress transcripts, so that I can guide graduation readiness."},
    {"source_id": "dalpiaz_univ_019", "text": "As a student, I want to check assignment grades with instructor feedback, so that I know which concepts require improvement."},
    {"source_id": "dalpiaz_univ_020", "text": "As a registrar officer, I want to generate official student enrollment verification letters, so that students can apply for scholarships."},

    # Healthcare & Clinical Systems
    {"source_id": "dalpiaz_health_021", "text": "As a doctor, I want to look up patient allergy histories before prescribing medication, so that adverse drug interactions are avoided."},
    {"source_id": "dalpiaz_health_022", "text": "As a nurse, I want to record vital sign readings hourly, so that attending physicians observe patient stability trends."},
    {"source_id": "dalpiaz_health_023", "text": "As a patient, I want to view lab blood test results online, so that I stay informed about my medical conditions."},
    {"source_id": "dalpiaz_health_024", "text": "As a pharmacist, I want to verify electronic prescription signatures, so that controlled medications are dispensed legitimately."},
    {"source_id": "dalpiaz_health_025", "text": "As a clinic receptionist, I want to reschedule patient consultation appointments, so that doctor calendar gaps are minimized."},

    # E-Commerce & Retail Marketplace
    {"source_id": "dalpiaz_ecom_026", "text": "As a shopper, I want to filter search results by customer review ratings, so that I find well-regarded products."},
    {"source_id": "dalpiaz_ecom_027", "text": "As a buyer, I want to save multiple shipping addresses in my address book, so that I can send gifts directly to family."},
    {"source_id": "dalpiaz_ecom_028", "text": "As a merchant, I want to receive low stock alert emails when inventory drops below 10 units, so that I replenish supplies on time."},
    {"source_id": "dalpiaz_ecom_029", "text": "As a customer, I want to track parcel carrier tracking numbers on an interactive map, so that I anticipate arrival times."},
    {"source_id": "dalpiaz_ecom_030", "text": "As a seller, I want to print bulk packing slips with barcodes, so that order fulfillment time is cut down."},

    # Financial & Banking Systems
    {"source_id": "dalpiaz_fin_031", "text": "As an account holder, I want to transfer funds between my checking and savings accounts, so that I maintain required liquidity."},
    {"source_id": "dalpiaz_fin_032", "text": "As a cardholder, I want to temporarily freeze my debit card via mobile app, so that unauthorized charges are blocked after loss."},
    {"source_id": "dalpiaz_fin_033", "text": "As an investor, I want to view my retirement portfolio asset allocation percentages, so that I balance risk exposure."},
    {"source_id": "dalpiaz_fin_034", "text": "As a customer, I want to set up recurring monthly utility bill payments, so that I avoid late payment penalty fees."},
    {"source_id": "dalpiaz_fin_035", "text": "As a business owner, I want to export transaction statements to QuickBooks format, so that tax filing preparation is automated."},

    # Logistics & Fleet Management
    {"source_id": "dalpiaz_log_036", "text": "As a fleet manager, I want to track vehicle fuel efficiency metrics, so that operational costs are controlled."},
    {"source_id": "dalpiaz_log_037", "text": "As a truck driver, I want to log required rest break intervals on a digital tachograph, so that transportation laws are complied with."},
    {"source_id": "dalpiaz_log_038", "text": "As a warehouse supervisor, I want to scan pallet RFID tags upon arrival, so that inventory databases update instantaneously."},
    {"source_id": "dalpiaz_log_039", "text": "As a customer, I want to select preferred delivery time slots, so that I am available to receive packages."},
    {"source_id": "dalpiaz_log_040", "text": "As a courier, I want the navigation app to optimize delivery stop sequences, so that transit mileage is minimized."}
]
