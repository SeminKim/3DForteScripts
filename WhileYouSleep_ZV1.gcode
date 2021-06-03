; Written by Seohyun, Jung, Modified by Sehoon Tak
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
G0 F5000 Z5.0 ; Rapid down movement

G1 Y1 F2400 ; Remove
G1 Y30 F8000 ; Shake 
G1 Y1 F8000 ; Shake
G1 Y30 F8000; Shake

G0 F5000 Z15.0 ; Move up to avoid blade movement, exact height debatable
G4 S60; Don't do anything for 60 seconds, debug line

M23 print.gcode; Set current print back up for printing
M24; Restart print