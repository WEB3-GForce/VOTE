db name: vote

- collections
    - member (table)
    - bill (table)
    - stance (table)
    - strategy (table)
    - group (table)
    - decision (table)
    - issue (table)

member:

- name
- fname
- lname
- english_short
- notes
- gender
- votes
- new_votes
- stances
- issues
- credo
- groups
- relations
- pro_rel_stances
- con_rel_stances
- stance_sort_key (LOYALTY or EQUITY)
- district
- term_start
- term_end
- party
- committees

decision:

- for_stances
- agn_stances
- neg_for_stances
- neg_agn_stances
- con_rel_for_stances
- con_rel_agn_stances
- no_update
- number_for
- number_agn
- group_for
- group_agn
- for_norms
- agn_norms
- for_bnorms
- agn_bnorms
- split_group
- split_record
- split_credo
- MI_stance
- MI_group
- MI_credo
- MI_record
- MI_norm
- strategy
- result
- reason
- downside
- downside_record
- deeper_analysis
- real_vote
- score
