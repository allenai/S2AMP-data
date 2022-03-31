
## List of features

coa : coauthor
mte : mentee
copub : period of copublication

- `mte_ai2id` : mentee ai2id
- `coa_ai2id` : coauthor ai2id
- `is_mentor` : is coauthor a mentor

### Publication count features
- `copub_count` : total papers published together 
- `total_mte_pubs` : total publications of the mentee till copub end date
- `total_coa_pubs` : total publications of the coauthor till copub end date
- `mte_copub_total` : # of papers published by mentee in copub period
- `coa_copub_total` : # of papers published by coauthor in copub period
- `mte_copub_prcnt` : ratio of copub_count to mte_copub_total
- `coa_copub_prcnt` : ratio of copub_count to coa_copub_total
- `ratio_mte_coa` : ratio of total_mte_pubs to total_coa_pubs

- #### Density features :
    - `dense_mte_copub_total` : # of papers published by mentee in dense copub period
    - `dense_coa_copub_total` : # of papers published by coauthor in dense copub period
    - `dense_total_coa_pubs` : total publications of the coauthor till dense copub end date
    - `dense_total_mte_pubs` : total publications of the mentee till dense copub end date
    - `dense_copub_count` : total papers published together during the dense copub period
    - `dense_mte_copub_prcnt` : ratio of dense copub_count to mte_copub_total
    - `dense_coa_copub_prcnt` : ratio of dense copub_count to coa_copub_total
    - `dense_ratio_mte_coa` : ratio of dense_total_mte_pubs to dense_total_coa_pubs

### Publication year features
- `copub_years` : # of years of collaboration
- `mte_years` : mentee publication years till copub end date
- `coa_years` : coauthor publication years till copub end date
- `mte_copub_years_prcnt` : ratio of copub_years to mte_years
- `coa_copub_years_prcnt` : ratio of copub_years to coa_years

- #### Density features : 
    - `dense_mte_years` : mentee publication years till dense copub end date
    - `dense_coa_years` : coauthor publication years till dense copub end date
    - `dense_mte_copub_years_prcnt` : ratio of dense copub_years to mte_years
    - `dense_coa_copub_years_prcnt` : ratio of dense copub_years to coa_years


### Graph features : 

  - `coa_out_min` : coauthor out-edge min weight
  - `coa_in_min` : coauthor in-edge min weight
  - `mte_out_min` : mentee out-edge min weight
  - `mte_in_min` : mentee in-edge min weight
    

  - `coa_out_max` : coauthor  out-edge max weight
  - `coa_in_max` : coauthor in-edge max weight
  - `mte_out_max` : mentee  out-edge max weight
  - `mte_in_max` : mentee in-edge max weight


  - `coa_out_sum` : sum of  out-edge weights for coauthor
  - `coa_in_sum` : sum of in-edge weights for coauthor
  - `mte_out_sum` : sum of  out-edge weights for mentee
  - `mte_in_sum` : sum of in-edge weights for mentee 
  

  - `mte_weight_sum` : `mte_out_sum` + `mte_in_sum`
  - `coa_weight_sum` : `coa_out_sum` + `coa_in_sum`
    

  - `mte_avg_in` : average of in-edge weights for mentee
  - `mte_avg_out` : average of  out-edge weights for mentee
  - `coa_avg_in` : average of in-edge weights for coauthor
  - `coa_avg_out` : average of  out-edge weights for coauthor

  - `mte_ratio_in_out` : ratio of `mte_in_sum` to `mte_out_sum`
  - `coa_ratio_in_out` : ratio of `coa_in_sum` to `coa_out_sum`

### Coauthor features :

- `mentee_coauthors_before_copub` : number of coauthors of mentee before copublication period
- `mentor_coauthors_before_copub` : number of coauthors of mentor before copublication period


- `mentee_coauthors_after_copub` : number of coauthors of mentee at the end of copublication period
- `mentor_coauthors_after_copub` : number of coauthors of mentor at the end of copublication period


- `mentee_coauthors_copub` : number of coauthors of mentee during copublication period
- `mentor_coauthors_copub` : number of coauthors of mentee during copublication period


- `ratio_mentee_mentor_coauthors` : `mentee_coauthors_copub` divided by `mentor_coauthors_copub`
- `ratio_mentee_mentor_coauthors_before` : `mentee_coauthors_before_copub` divided by `mentor_coauthors_before_copub`
- `ratio_mentee_mentor_coauthors_after` : `mentee_coauthors_after_copub` divided by `mentor_coauthors_after_copub`

### Position features :
- `mentee_min_position` : min position of authorship of mentee in copublications
- `mentor_min_position` : min position of authorship of mentor in copublications


- `mentee_max_position` : max position of authorship of mentee in copublications
- `mentor_max_position` : max position of authorship of mentor in copublications


- `mentee_avg_position` : avg position of authorship of mentee in copublications
- `mentor_avg_position` : avg position of authorship of mentor in copublications



P.S. : 
We extract and keep only the author pairs which have 3 or more publications together -
- 1 and 2 copubs are too less to make a predict 