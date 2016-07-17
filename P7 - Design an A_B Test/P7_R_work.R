# Initial Baseline Values
Unique_cookies_to_view_page_per_day = 40000
Unique_cookies_to_click_Start_free_trial_per_day = 3200
Enrollments_per_day = 660
Click_through_probability_on_Start_free_trial = Unique_cookies_to_click_Start_free_trial_per_day / Unique_cookies_to_view_page_per_day
Probability_of_enrolling_given_click = Enrollments_per_day / Unique_cookies_to_click_Start_free_trial_per_day
Probability_of_payment_given_enroll = 0.53
Probability_of_payment_given_click = Probability_of_payment_given_enroll * Probability_of_enrolling_given_click
sample_size_of_cookies = 5000

# Calc Standard Deviations

## Gross Conversions
Clicks = sample_size_of_cookies * 
  Click_through_probability_on_Start_free_trial

Gross_Conv_SE = sqrt((Probability_of_enrolling_given_click * 
                        (1-Probability_of_enrolling_given_click))/Clicks)

## Retention
Enrollments = sample_size_of_cookies * 
  Click_through_probability_on_Start_free_trial *
  Probability_of_enrolling_given_click

Retention_SE = sqrt((Probability_of_payment_given_enroll * 
                        (1-Probability_of_payment_given_enroll))/Enrollments)

## Net Conversions
Net_Conv_SE = sqrt((Probability_of_payment_given_click * 
                        (1-Probability_of_payment_given_click))/Clicks)

# Calculating Number of Pageviews
Gross_Conv_Samples_Needed = 25835
Page_Views_Needed_1 = Gross_Conv_Samples_Needed / 
  Click_through_probability_on_Start_free_trial

Retention_Samples_Needed = 39115
Page_Views_Needed_2 = Retention_Samples_Needed / 
  (Enrollments_per_day / Unique_cookies_to_view_page_per_day)

Net_Conv_Samples_Needed = 27413
Page_Views_Needed_3 = Net_Conv_Samples_Needed / 
  Click_through_probability_on_Start_free_trial

max(Page_Views_Needed_1, Page_Views_Needed_2, Page_Views_Needed_3)

## Pageviews needed
Page_Views_Needed_2 * 
  Click_through_probability_on_Start_free_trial * 
  Probability_of_enrolling_given_click /
  Enrollments_per_day * 2 * 2

## Pageviews needed w/o Retention
max(Page_Views_Needed_1, Page_Views_Needed_3) * 
  2 * Click_through_probability_on_Start_free_trial / 3200 / .9


