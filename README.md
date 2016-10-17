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
    1. 1 = the user clicked on the item
    2. 2 = the user bookmarked the item
    3. 3 = the user clicked on the reply button or application form button that is shown on some job postings
- **created_at:** a unix time stamp timestamp representing the time when the interaction got created

