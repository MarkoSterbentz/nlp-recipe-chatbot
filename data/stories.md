## start path1
* greet
  - utter_greet
  - utter_url_prompt
* url
  - action_get_recipe
  - utter_prompt
> check_interaction_loop

## start path
* url
  - action_get_recipe
  - utter_prompt
> check_interaction_loop

## display ingredients
> check_interaction_loop
* display_ingredients
  - action_display_ingredients
  - utter_prompt
> check_interaction_loop

## display current step
> check_interaction_loop
* display_current_step
  - action_display_current_step
  - utter_prompt
> check_interaction_loop

## display all steps
> check_interaction_loop
* display_all_steps
  - action_display_all_steps
  - utter_prompt
> check_interaction_loop

## navigate recipe
> check_interaction_loop
* go_to_step
  - slot{"step_number":"1"}
  - action_go_to_step
  - utter_prompt
> check_interaction_loop

## transform recipe
> check_interaction_loop
* transform_recipe
  - slot{"transformation_type":"mexico"}
  - action_transform_recipe
  - utter_prompt
> check_interaction_loop

## answer what is question
> check_interaction_loop
* what_is
  - slot{"what_is_object":"garlic"}
  - action_answer_what_is
  - utter_prompt
> check_interaction_loop

## answer how to question
> check_interaction_loop
* how_to
  - slot{"how_to_object":"cook"}
  - action_answer_how_to
  - utter_prompt
> check_interaction_loop

## end path
> check_interaction_loop
* goodbye
  - utter_goodbye
