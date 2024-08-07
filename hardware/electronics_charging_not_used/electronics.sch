EESchema Schematic File Version 4
EELAYER 26 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Connector:USB_C_Receptacle_USB2.0 J3
U 1 1 5C521088
P 3700 4450
F 0 "J3" H 3805 5317 50  0000 C CNN
F 1 "USB_C_Receptacle_USB2.0" H 3805 5226 50  0000 C CNN
F 2 "Connector_USB:USB_C_Receptacle_Amphenol_12401548E4-2A" H 3850 4450 50  0001 C CNN
F 3 "https://www.usb.org/sites/default/files/documents/usb_type-c.zip" H 3850 4450 50  0001 C CNN
	1    3700 4450
	1    0    0    -1  
$EndComp
$Comp
L Connector:USB_C_Receptacle_USB2.0 J1
U 1 1 5C521188
P 3650 1950
F 0 "J1" H 3755 2817 50  0000 C CNN
F 1 "USB_C_Receptacle_USB2.0" H 3755 2726 50  0000 C CNN
F 2 "Connector_USB:USB_C_Receptacle_Amphenol_12401548E4-2A" H 3800 1950 50  0001 C CNN
F 3 "https://www.usb.org/sites/default/files/documents/usb_type-c.zip" H 3800 1950 50  0001 C CNN
	1    3650 1950
	1    0    0    -1  
$EndComp
$Comp
L Connector:USB_C_Receptacle_USB2.0 J2
U 1 1 5C52132C
P 6100 1950
F 0 "J2" H 6150 2850 50  0000 R CNN
F 1 "USB_C_Receptacle_USB2.0" H 6500 2750 50  0000 R CNN
F 2 "Connector_USB:USB_C_Receptacle_Amphenol_12401548E4-2A" H 6250 1950 50  0001 C CNN
F 3 "https://www.usb.org/sites/default/files/documents/usb_type-c.zip" H 6250 1950 50  0001 C CNN
	1    6100 1950
	-1   0    0    -1  
$EndComp
Wire Wire Line
	3650 2850 6100 2850
Wire Wire Line
	3350 2850 3350 3050
Wire Wire Line
	3350 3050 6400 3050
Wire Wire Line
	6400 3050 6400 2850
Wire Wire Line
	4250 1350 5500 1350
$Comp
L Switch:SW_SPDT SW1
U 1 1 5C522216
P 4650 3850
F 0 "SW1" H 4650 4135 50  0000 C CNN
F 1 "SW_SPDT" H 4650 4044 50  0000 C CNN
F 2 "Button_Switch_THT:SW_CuK_OS102011MA1QN1_SPDT_Angled" H 4650 3850 50  0001 C CNN
F 3 "" H 4650 3850 50  0001 C CNN
	1    4650 3850
	1    0    0    -1  
$EndComp
Wire Wire Line
	4300 3850 4450 3850
$Comp
L Device:LED_Small D1
U 1 1 5C5235CB
P 5250 4300
F 0 "D1" V 5250 4500 50  0000 R CNN
F 1 "LED_Small" V 5150 4750 50  0000 R CNN
F 2 "LED_SMD:LED_0603_1608Metric" V 5250 4300 50  0001 C CNN
F 3 "~" V 5250 4300 50  0001 C CNN
	1    5250 4300
	0    -1   -1   0   
$EndComp
$Comp
L Device:R R1
U 1 1 5C5236C3
P 5250 4800
F 0 "R1" H 5320 4846 50  0000 L CNN
F 1 "330R" H 5320 4755 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric_Pad1.05x0.95mm_HandSolder" V 5180 4800 50  0001 C CNN
F 3 "~" H 5250 4800 50  0001 C CNN
	1    5250 4800
	1    0    0    -1  
$EndComp
Wire Wire Line
	5250 4400 5250 4650
Wire Wire Line
	5250 4950 5250 5350
Wire Wire Line
	5250 5350 5600 5350
Wire Notes Line
	6800 3100 3000 3100
Wire Notes Line
	3000 3100 3000 850 
Wire Notes Line
	3000 850  6800 850 
Wire Notes Line
	6800 850  6800 3100
Text Notes 3300 1000 0    50   ~ 0
Power in to charge
Text Notes 5750 1000 0    50   ~ 0
To Battery (Charge out)
Wire Notes Line
	6950 3300 3000 3300
Wire Notes Line
	3000 3300 3000 5650
Wire Notes Line
	3000 5650 6950 5650
Wire Notes Line
	6950 5650 6950 3300
Text Notes 3350 3500 0    50   ~ 0
Power for Pi \nFrom Battery
Text Notes 5950 3400 0    50   ~ 0
Power to Pi
Text Notes 5000 3400 0    50   ~ 0
Current measure
Wire Wire Line
	5250 3800 5600 3800
Wire Wire Line
	5250 3800 5250 4200
Connection ~ 5250 3800
Wire Wire Line
	4850 3800 4850 3750
$Comp
L Connector:Screw_Terminal_01x02 J4
U 1 1 5C53380F
P 5950 4150
F 0 "J4" V 5916 3962 50  0000 R CNN
F 1 "Screw_Terminal_01x02" V 6100 4350 50  0000 R CNN
F 2 "TerminalBlock_4Ucon:TerminalBlock_4Ucon_1x02_P3.50mm_Horizontal" H 5950 4150 50  0001 C CNN
F 3 "~" H 5950 4150 50  0001 C CNN
	1    5950 4150
	1    0    0    -1  
$EndComp
Wire Wire Line
	3700 5350 5250 5350
Connection ~ 5250 5350
Wire Wire Line
	5600 5350 5600 4250
Wire Wire Line
	5600 4250 5750 4250
Wire Wire Line
	5600 3800 5600 4150
Wire Wire Line
	5600 4150 5750 4150
Wire Wire Line
	4850 3800 5250 3800
$EndSCHEMATC
