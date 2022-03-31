# S2AMP-data
Dataset for S2AMP including training/classification and inference data

````
S2AMP-data/
├── [2.1G]  gold
│   ├── [812M]  first_stage_features
│   │   ├── [163M]  test.csv
│   │   ├── [485M]  train.csv
│   │   └── [164M]  val.csv
│   ├── [6.6M]  lgb_first.stage.model.pkl
│   ├── [6.3M]  lgb_second.stage.model.pkl
│   ├── [ 15M]  S2AMP_matched_pairs.csv
│   └── [1.3G]  second_stage_features
│       ├── [269M]  test.csv
│       ├── [817M]  train.csv
│       └── [272M]  val.csv
└── [9.4G]  inferred
    ├── [1.3G]  mentors_s2_fos_scores.csv
    └── [8.1G]  s2amp_predictions_with_names.csv

  12G used in 4 directories, 11 files
````

### S2AMP Gold
- Mentor Mentee true pairs with S2 ids.
  - `S2AMP_matched_pairs.csv`
    - _mentee_ai2_id_
    - _mentor_ai2_id_
    - _mentor_fname_ : mentor's first name
    - _mentor_lname_ : mentor's last name
    - _mentee_fname_ : mentee's first name
    - _mentee_lname_ : mentee's last name
    - _num_papers_cowritten_ : number of co-authored papers


- Train data
  - _is_mentor_ : flag for true pair(1) and false pair(0)
  - First Stage
    - `first_stage_features/train.csv`
    - `first_stage_features/val.csv`
    - `first_stage_features/test.csv`
      
  - Second Stage Train data
    - `second_stage_features/train.csv`
    - `second_stage_features/val.csv`
    - `second_stage_features/test.csv`

More details about the features are in `README_features.md`

- First stage model : LightGBM model trained on `first_stage_features`
  - `lgb_first.stage.model.pkl`
- Second stage model : LightGBM model trained on `second_stage_features`
  - `lgb_second.stage.model.pkl`


### S2AMP Inferred
- Mentor-mentee pairs with scores
  - `s2amp_predictions_with_names.csv`
    - _mentee_ai2id_
    - _mentor_ai2id_
    - _pred_prob_ : mentorship_score (<0.1 scores can be ignored)
    - _mentee_name_
    - _mentor_name_
- Mentors with author details and mentorship scores
  - `mentors_s2_fos_scores.csv`
    - _authors_ai2_id_ : ai2id of the author
    - _h_index_
    - _paper_count_
    - _citation_count_
    - _affiliations_
    - _mentorship_score_ : sum of mentorship scores from mentorship graph 
    - _mentorship_score_mean_ : mean of mentorship scores
    - _menteeship_score_ : sum of menteeship scores from mentorship graph 
    - _menteeship_score_mean_ : mean of menteeship scores
    - _mentee_count_ : count of mentee's mentored 
    - _mentor_count_ : count of mentor's of the author
    - _fos_ : field of study of the author
    - _log_mentee_count_
    
### Download Instructions
To obtain the S2AMP dataset, run the following command:
[Expected download size is: 12 GiB]

aws s3 sync --no-sign-request s3://ai2-s2-research-public/s2amp data/
