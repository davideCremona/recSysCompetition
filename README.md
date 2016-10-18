# recSysCompetition

## File descriptions
- **interactions.csv** - the training set
- **target_users.csv** - users in the test set receiving recommendations
- **item_profile.csv** - supplementary information about the items
- **user_profile.csv** - supplemental information about the users
- **sampleSubmission.csv** - a sample submission file in the correct format

## Dataset Description

### Interactions

Interactions that the user performed on the job posting items. Fields:

- **user_id:** ID of the user who performed the interaction (points to users.id)
- **item_id:** ID of the item on which the interaction was performed (points to items.id)
- **interaction_type:** the type of interaction that was performed on the item:
    - **1** = the user clicked on the item
    - **2** = the user bookmarked the item
    - **3** = the user clicked on the reply button or application form button that is shown on some job postings
- **created_at:** a unix time stamp timestamp representing the time when the interaction got created

### Users

Details about those users who appear in the above datasets. Fields:

- **id:** anonymized ID of the user (referenced as user_id in the interaction dataset)
- **jobroles:** comma-separated list of job role terms (numeric IDs) that were extracted from the user’s current job title. 0 means that there was no known jobrole detected for the user.
- **career_level:** career level ID (e.g. beginner, experienced, manager):
    - **0** = unknown
    - **1** = Student/Intern
    - **2** = Entry Level (Beginner)
    - **3** = Professional/Experienced
    - **4** = Manager (Manager/Supervisor)
    - **5** = Executive (VP, SVP, etc.)
    - **6** = Senior Executive (CEO, CFO, President)
- **discipline_id:** anonymized IDs represent disciplines such as “Consulting”, “HR”, etc.
- **industry_id:** anonymized IDs represent industries such as “Internet”, “Automotive”, “Finance”, etc.
- **country:** describes the country in which the user is currently working:
    - **de** = Germany
    - **at** = Austria
    - **ch** = Switzerland
    - **non_dach** = non of the above countries
- **region:** is specified for some users who have as country de. Meaning of the regions: see below.
- **experience_n_entries_class:** identifies the number of CV entries that the user has listed as work experiences:
    - **0** = no entries
    - **1** = 1-2 entries
    - **2** = 3-4 entries
    - **3** = 5 or more entries
- **experience_years_experience:** number of years of work experience that the user has:
    - **0** = unknown
    - **1** = less than 1 year
    - **2** = 1-3 years
    - **3** = 3-5 years
    - **4** = 5-10 years
    - **5** = 10-15 years
    - **6** = 16-20
    - **7** = more than 20 years
- **experience_years_in_current:** number of years that the user is already working in her current job. Meaning of numbers: same as experience_years_experience
- **edu_degree:** university degree of the user:
    - **0 or NULL** = unknown
    - **1** = bachelor
    - **2** = master
    - **3** = phd
- **edu_fieldofstudies:** comma-separated fields of studies (anonymized ids) that the user studied. 0 means “unknown” and edu_fieldofstudies > 0 entries refer to broad field of studies such as Engineering, Economics and Legal, …

### Items

Details about the job postings that were and should be recommended to the users.

- **id:** anonymized ID of the item (referenced as item_id in interaction dataset)
- **title:** concepts that have been extracted from the job title of the job posting (numeric IDs)
- **career_level:** career level ID (e.g. beginner, experienced, manager):
    - **0** = unknown
    - **1** = Student/Intern
    - **2** = Entry Level (Beginner)
    - **3** = Professional/Experienced
    - **4** = Manager (Manager/Supervisor)
    - **5** = Executive (VP, SVP, etc.)
    - **6** = Senior Executive (CEO, CFO, President)
- **discipline_id:** anonymized IDs represent disciplines such as “Consulting”, “HR”, etc.
- **industry_id:** anonymized IDs represent industries such as “Internet”, “Automotive”, “Finance”, etc.
- **country:** code of the country in which the job is offered
- **region:** is specified for some users who have as country de. Meaning of the regions: see below.
- **latitude:** latitude information (rounded to ca. 10km)
- **longitude:** longitude information (rounded to ca. 10km)
- **employment:** the type of employment:
    - **0** = unknown
    - **1** = full-time
    - **2** = part-time
    - **3** = freelancer
    - **4** = intern
    - **5** = voluntary
- **tags:** concepts that have been extracted from the tags, skills or company name
- **created_at:** a Unix time stamp timestamp representing the time when the interaction happened
- **active_during_test:** is 1 if the item (job) is still active (= recommendable) during the test period and 0 if the item is not active anymore in the test period (= not recommendable)

### Regions

ID  Name
- **0+*   not specified
- **1**   Baden-Württemberg
- **2**   Bavaria
- **3**   Berlin
- **4**   Brandenburg
- **5**   Bremen
- **6**   Hamburg
- **7**   Hesse
- **8**   Mecklenburg-Vorpommern
- **9**   Lower Saxony
- **10**  North Rhine-Westphalia
- **11**  Rhineland-Palatinate
- **12**  Saarland
- **13**  Saxony
- **14**  Saxony-Anhalt
- **15**  Schleswig-Holstein
- **16**  Thuringia

### Target Users

The file target_users.csv contains those user IDs for which you finally need to submit solutions. The file lists one user ID per line (in total, 10,000 user IDs). All those target users are also contained in the training data.