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

    # G04 - Content Management & Digital Publishing
    {"source_id": "dalpiaz_cms_041", "text": "As an editor, I want to schedule article publication timestamps in advance, so that content goes live during peak readership hours."},
    {"source_id": "dalpiaz_cms_042", "text": "As a writer, I want to save drafts automatically every two minutes, so that progress is not lost during network interruptions."},
    {"source_id": "dalpiaz_cms_043", "text": "As a site administrator, I want to assign role-based editing permissions to authors, so that unauthorized personnel cannot publish live changes."},
    {"source_id": "dalpiaz_cms_044", "text": "As a content creator, I want to crop and compress uploaded images directly in the browser, so that web page loading speeds remain optimal."},
    {"source_id": "dalpiaz_cms_045", "text": "As an archivist, I want to restore earlier document revisions from the version history, so that unintended text modifications can be rolled back."},

    # Cybersecurity, IAM & Compliance
    {"source_id": "dalpiaz_sec_046", "text": "As a security administrator, I want to enforce multi-factor authentication for all remote logins, so that unauthorized credential use is prevented."},
    {"source_id": "dalpiaz_sec_047", "text": "As a compliance officer, I want to export immutable system audit logs, so that security incident forensics meet regulatory mandates."},
    {"source_id": "dalpiaz_sec_048", "text": "As a network engineer, I want to receive automated alerts upon detection of anomalous traffic spikes, so that potential DDoS attacks are neutralized rapidly."},
    {"source_id": "dalpiaz_sec_049", "text": "As a system user, I want to reset my expired password via a self-service verification email, so that I regain platform access without IT intervention."},
    {"source_id": "dalpiaz_sec_050", "text": "As a database administrator, I want to encrypt sensitive database fields at rest, so that stored data remains protected in the event of hardware theft."},

    # Customer Support & CRM
    {"source_id": "dalpiaz_crm_051", "text": "As a support agent, I want to merge duplicate customer inquiry tickets, so that communication history is unified across channels."},
    {"source_id": "dalpiaz_crm_052", "text": "As a team lead, I want to assign high-priority tickets automatically to available senior staff, so that service level agreement breaches are avoided."},
    {"source_id": "dalpiaz_crm_053", "text": "As a customer, I want to view my open support tickets in a self-service portal, so that I can monitor issue resolution progress."},
    {"source_id": "dalpiaz_crm_054", "text": "As a helpdesk specialist, I want to insert pre-approved canned responses into replies, so that recurring questions are addressed efficiently."},
    {"source_id": "dalpiaz_crm_055", "text": "As an operations manager, I want to generate weekly first-contact resolution metrics, so that support staffing needs can be evaluated."},

    # Travel, Hospitality & Booking
    {"source_id": "dalpiaz_travel_056", "text": "As a traveler, I want to filter hotel searches by refundable cancellation policies, so that I retain financial flexibility if travel plans shift."},
    {"source_id": "dalpiaz_travel_057", "text": "As a passenger, I want to choose my airplane seat on an interactive cabin layout map, so that I secure my preferred seating arrangement."},
    {"source_id": "dalpiaz_travel_058", "text": "As a front desk clerk, I want to mark hotel room turnover states as inspected, so that housekeeping readiness is clear before guest check-in."},
    {"source_id": "dalpiaz_travel_059", "text": "As a vacationer, I want to download boarding passes directly into my mobile wallet, so that airport check-in is frictionless without physical paper."},
    {"source_id": "dalpiaz_travel_060", "text": "As a hotel manager, I want to adjust seasonal room pricing tiers dynamically, so that occupancy rates and room revenue are maximized."},

    # Human Resources & Talent Acquisition
    {"source_id": "dalpiaz_hr_061", "text": "As a recruiter, I want to parse applicant resume PDFs for specific programming keywords, so that candidate shortlisting is streamlined."},
    {"source_id": "dalpiaz_hr_062", "text": "As a job applicant, I want to track my recruitment pipeline status online, so that I know whether my portfolio has reached the interview stage."},
    {"source_id": "dalpiaz_hr_063", "text": "As an employee, I want to submit annual leave requests via the portal calendar, so that my supervisor can review and approve scheduling."},
    {"source_id": "dalpiaz_hr_064", "text": "As an HR manager, I want to track team mandatory compliance training completion rates, so that corporate policy certifications stay current."},
    {"source_id": "dalpiaz_hr_065", "text": "As a department manager, I want to document quarterly performance evaluation milestones, so that promotion reviews are based on documented achievements."},

    # Media Streaming & Entertainment
    {"source_id": "dalpiaz_media_066", "text": "As a subscriber, I want to adjust video playback speeds from 0.5x to 2.0x, so that I consume instructional content at my own pace."},
    {"source_id": "dalpiaz_media_067", "text": "As a viewer, I want to resume video playback from the exact timestamp I paused on another device, so that cross-platform continuity is maintained."},
    {"source_id": "dalpiaz_media_068", "text": "As a listener, I want to download audio tracks for offline playback, so that I can listen to playlists without mobile data coverage."},
    {"source_id": "dalpiaz_media_069", "text": "As a parent, I want to configure content age-rating filters on child profiles, so that mature programs remain inaccessible to young viewers."},
    {"source_id": "dalpiaz_media_070", "text": "As a user, I want to search movies by director and cast members, so that I discover relevant filmographies efficiently."},

    # Telecommunications & Network Infrastructure
    {"source_id": "dalpiaz_telecom_071", "text": "As a subscriber, I want to view remaining cellular data balances in real time, so that unexpected bandwidth overage fees are prevented."},
    {"source_id": "dalpiaz_telecom_072", "text": "As a network technician, I want to run remote ping and traceroute diagnostics on cell towers, so that hardware outages are isolated quickly."},
    {"source_id": "dalpiaz_telecom_073", "text": "As a customer, I want to purchase international roaming data packages through the mobile application, so that connectivity is instant upon arrival abroad."},
    {"source_id": "dalpiaz_telecom_074", "text": "As an infrastructure engineer, I want to monitor base transceiver station battery backups, so that power grid failures do not sever emergency communications."},
    {"source_id": "dalpiaz_telecom_075", "text": "As an account holder, I want to enable automatic monthly data plan renewals, so that mobile network services operate without disruption."},

    # Energy, Utilities & Sustainability
    {"source_id": "dalpiaz_energy_076", "text": "As a facility manager, I want to track peak power load intervals across commercial buildings, so that high-demand utility penalties are minimized."},
    {"source_id": "dalpiaz_energy_077", "text": "As a resident, I want to receive SMS notifications regarding scheduled water maintenance shutoffs, so that domestic tasks can be prepared beforehand."},
    {"source_id": "dalpiaz_energy_078", "text": "As a solar panel owner, I want to measure net kilowatt-hour power fed back into the electrical grid, so that utility feed-in tariff credits are accurately computed."},
    {"source_id": "dalpiaz_energy_079", "text": "As a meter inspector, I want to record residential gas consumption readings on an offline mobile tablet, so that rural readings sync automatically when reconnected."},
    {"source_id": "dalpiaz_energy_080", "text": "As an environmental analyst, I want to export facility greenhouse gas emission records, so that corporate carbon sustainability reports satisfy government guidelines."},

    # Project Collaboration & Issue Tracking
    {"source_id": "dalpiaz_collab_081", "text": "As a developer, I want to link Git commit hashes to issue tracker tickets, so that code changes can be traced back to business requirements."},
    {"source_id": "dalpiaz_collab_082", "text": "As a project manager, I want to visualize task dependencies on an interactive Gantt chart, so that critical path bottlenecks are identified early."},
    {"source_id": "dalpiaz_collab_083", "text": "As a scrum master, I want to track sprint velocity trends across consecutive iterations, so that sprint capacity planning is grounded in historical velocity."},
    {"source_id": "dalpiaz_collab_084", "text": "As a team member, I want to mention colleagues using their username in task comment threads, so that relevant collaborators are notified directly."},
    {"source_id": "dalpiaz_collab_085", "text": "As a product owner, I want to drag and drop backlog items to reprioritize deliverables, so that upcoming sprint priorities reflect stakeholder feedback."},

    # EdTech & E-Learning Platforms
    {"source_id": "dalpiaz_edu_086", "text": "As an instructor, I want to configure randomized quiz question orders, so that academic integrity is upheld during online examinations."},
    {"source_id": "dalpiaz_edu_087", "text": "As a student, I want to download supplementary reading PDFs for offline study, so that learning can continue during travel without internet."},
    {"source_id": "dalpiaz_edu_088", "text": "As a teaching assistant, I want to grade student assignments using standardized rubrics, so that assessment criteria remain consistent across all submissions."},
    {"source_id": "dalpiaz_edu_089", "text": "As a learner, I want to generate course completion certificates with unique verification IDs, so that credentials can be confirmed by prospective employers."},
    {"source_id": "dalpiaz_edu_090", "text": "As a course creator, I want to embed interactive coding sandboxes within modules, so that students can execute exercises directly inside their web browser."},

    # LegalTech & Contract Management
    {"source_id": "dalpiaz_legal_091", "text": "As a legal counsel, I want to compare two versions of a service agreement side by side, so that contractual revisions are pinpointed accurately."},
    {"source_id": "dalpiaz_legal_092", "text": "As a procurement specialist, I want to receive automated contract renewal reminders 60 days before expiration, so that renegotiations begin before services lapse."},
    {"source_id": "dalpiaz_legal_093", "text": "As a corporate signatory, I want to sign documents using cryptographic digital signatures, so that the legal validity of commercial contracts is assured."},
    {"source_id": "dalpiaz_legal_094", "text": "As a paralegal, I want to redact personal identifying information across court filings, so that privacy guidelines are respected before public disclosure."},
    {"source_id": "dalpiaz_legal_095", "text": "As a compliance auditor, I want to search contract archives by governing jurisdiction clauses, so that regional legal exposure can be audited efficiently."},

    # Autonomous & Connected Vehicles
    {"source_id": "dalpiaz_auto_096", "text": "As an electric vehicle driver, I want to locate available fast-charging stations along a planned route, so that range anxiety is avoided on road trips."},
    {"source_id": "dalpiaz_auto_097", "text": "As a car owner, I want to trigger cabin pre-conditioning through my smartphone app, so that the interior is warmed up prior to winter departure."},
    {"source_id": "dalpiaz_auto_098", "text": "As a vehicle maintenance technician, I want to read onboard diagnostic error codes over Bluetooth, so that powertrain sensor issues are diagnosed quickly."},
    {"source_id": "dalpiaz_auto_099", "text": "As a driver, I want to receive over-the-air firmware updates for the infotainment console, so that system bug fixes install without a service center visit."},
    {"source_id": "dalpiaz_auto_100", "text": "As a fleet dispatcher, I want to receive geofence exit alerts when fleet vehicles depart assigned routes, so that unauthorized vehicle operation is detected."}
]
