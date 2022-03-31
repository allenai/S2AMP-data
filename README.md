# S2AMP-data
Dataset for S2AMP including training/classification and inference data


S2AMP Gold
- Mentor Mentee true pairs with S2 ids.
  - `S2AMP_matched_pairs.csv`
    - _mentee_ai2_id_
    - _mentor_ai2_id_
    - _mentor_fname_ : mentor's first name
    - _mentor_lname_ : mentor's last name
    - _mentee_fname_ : mentee's first name
    - _mentee_lname_ : mentee's last name
    - _num_papers_cowritten_ : number of co-authored papers
- First Stage Train data 
  - `first_stage_features/train.csv`
  - `first_stage_features/val.csv`
  - `first_stage_features/test.csv`
    - _is_mentor_ : flag for true pair(1) and false pair(0)
- Second Stage Train data
  - `second_stage_features/train.csv`
  - `second_stage_features/val.csv`
  - `second_stage_features/test.csv`
- first stage model
- second stage model


S2AMP Inferred
- mentor-mentee pairs with scores
- mentors with author details and mentorship scores