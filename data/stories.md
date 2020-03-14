## start path1
* greet
  - utter_greet
  - utter_url_prompt
* url
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

## display ingredients
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
