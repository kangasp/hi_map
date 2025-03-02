# hi_map
Physical interactive map of Hawaii.  Uses esp32 to pull weather info and display with e-ink.



## State Machine
* Wake Up
    * User Interaction
        * Light up to give indication of life
        * Update display if needed
        * Respond to user interaction
            * Display light and wx for knob twist
        * No interaction for 2 min? Full refresh display, sleep with alarm.
    * By Timer
        * Fetch Data for WX
        * Respong to user interaction - unlikely
        * Check battery
            * Too low?  Display warning and go to sleep, no alarm.
        * Go back to sleep with alarm.



