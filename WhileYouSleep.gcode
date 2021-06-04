; Written by Seohyun, Jung
; When print is cancelled or finished

G90

M104 S0; Turn-off hotend
M106 S0; Turn-off fan

G0 F6000 X150.0 Y200.0;
G0 Z250;
G0 X110;

G0 X98 Y160;
G0 X110;

G0 X98 Y120;
G0 X110;

G0 X98 Y80;
G0 X110;

G0 X98 Y40;
G0 X110;

G0 X98 Y1;
G0 X110 Y200;

G0 X115;

M118 EASYSERVO_ABS 12 100; Rotate blade to remove position while head stays up at its maximum height
G0 F2400 Y200; Blade sweep to the back end

G0 F5000 Z5.0 ; Rapid down movement

G1 Y1 F2400 ; Remove
G1 Y30 F8000 ; Shake 
G1 Y1 F8000 ; Shake
G1 Y30 F8000; Shake

M118 EASYSERVO_ABS 12 0; Rotate blade to inital position

M140 S0 ;Turn-off bed
M84 X Y E Z
