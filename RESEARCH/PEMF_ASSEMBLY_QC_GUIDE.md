# ZK-PP2K PEMF Mat -- Assembly Instruction & QC Verification Guide

**Document Version:** 1.0
**Date:** 2026-02-08
**Design Reference:** Steeve Bradet (PEMF with Steeve) ZK-PP2K platform
**Classification:** ASSEMBLER DOCUMENT -- distribute to any authorized builder

---

## IMPORTANT NOTICES

**This document is for educational and experimental purposes only.** PEMF devices are not FDA-approved medical devices (with limited exceptions for bone healing). This guide does not constitute medical advice. Users should consult a healthcare provider before use.

**Electrical safety:** This build involves 24V DC circuits. While 24V DC is below the threshold for dangerous skin contact, improper assembly can still cause component failure, fire, or burns. If you are not comfortable with basic electronics (soldering, multimeter use, reading wiring diagrams), get help from someone who is.

**Assembler qualifications:** You must be comfortable with soldering, using a multimeter, and reading basic circuit diagrams. No prior PEMF knowledge is required -- this document covers everything you need to know.

---

## TABLE OF CONTENTS

1. [How This Device Works (60-Second Overview)](#section-1-how-this-device-works)
2. [Parts Verification (Complete BOM)](#section-2-parts-verification)
3. [Coil Winding](#section-3-coil-winding)
4. [Polarity Verification (CRITICAL)](#section-4-polarity-verification)
5. [Control Box Assembly](#section-5-control-box-assembly)
6. [Mat Assembly](#section-6-mat-assembly)
7. [Mandatory QC Checks (Pass/Fail)](#section-7-mandatory-qc-checks)
8. [Safety Warnings](#section-8-safety-warnings)
9. [Photos & Sign-Off](#section-9-photos-and-sign-off)
10. [Troubleshooting](#section-10-troubleshooting)

---

## SECTION 1: HOW THIS DEVICE WORKS

Before you build, understand what you are building. This takes 60 seconds and will prevent mistakes.

A PEMF (Pulsed Electromagnetic Field) device has three functional blocks:

```
CONTROLLER (ZK-PP2K)  -->  POWER STAGE (resistor)  -->  COILS (in the mat)
        |                                                       |
   Sets frequency                                    Converts electricity
   and duty cycle                                    into pulsed magnetic
                                                     field
```

1. The **ZK-PP2K controller** generates a square wave signal at a user-selected frequency (typically 1-100 Hz) and duty cycle (typically 10-20%).
2. The **4-ohm power resistor** limits current to protect the controller and coils.
3. The **coils** in the mat convert the pulsed electrical signal into a pulsed magnetic field that penetrates into the body.

**Why it must be a square wave:** Research (NASA Technical Paper 2003-212054, University of Michigan replication) showed that a square wave produces the fastest change in magnetic field (highest "slew rate"). This rapid change is what transfers energy to cells. Sine waves, triangle waves, and sawtooth waves showed no significant therapeutic effect. Static magnetic fields (permanent magnets) showed zero effect.

**Why coil direction matters:** Each coil generates a magnetic field with a north pole and south pole. If all coils face the same direction, their fields ADD together (constructive). If even one coil is reversed, the fields CANCEL in that area (destructive), creating dead zones with no therapeutic effect.

**Target specifications for this build:**

| Parameter | Value |
|-----------|-------|
| Gauss per coil (at surface) | 45-55 gauss |
| Frequency range | 1-100 Hz (user adjustable) |
| Waveform | Square wave (DC, unipolar) |
| Duty cycle | 10-20% (user adjustable) |
| Power supply | 24V DC, 6A minimum |
| Coil wire | 22 AWG magnet wire (enamel coated) |
| Wraps per coil | 95 |
| Coil diameter | ~100mm (propane bottle form) |

---

## SECTION 2: PARTS VERIFICATION

**MANDATORY: Verify ALL parts are present and correct BEFORE starting assembly.** Check each item off this list. If anything is missing or wrong, stop and resolve before proceeding.

### 2A. Control Box Parts

| # | Part | Specification | Qty | Check |
|---|------|--------------|-----|-------|
| 1 | ZK-PP2K PWM controller module | 3.3-30V input, LCD display, freq 1Hz-150KHz | 1 | [ ] |
| 2 | 24V DC power supply | 6A minimum (144W+), barrel jack output | 1 | [ ] |
| 3 | Power resistor | 4 ohm, 100W minimum (200W preferred) | 1 | [ ] |
| 4 | 12V DC cooling fan | 80mm or 120mm computer fan | 1 | [ ] |
| 5 | DC-DC buck converter module | Input 24V, output adjustable (set to 12V) | 1 | [ ] |
| 6 | Project box (enclosure) | ABS plastic, approx 200x150x100mm minimum | 1 | [ ] |
| 7 | GX16 aviator connector (male, panel mount) | 2-pin or 4-pin, for box side | 1 | [ ] |
| 8 | GX16 aviator connector (female, cable mount) | Matching pin count, for mat cable | 1 | [ ] |
| 9 | DC barrel jack (panel mount) | Matching PSU barrel size (typically 5.5x2.1mm) | 1 | [ ] |
| 10 | Power switch (rocker) | 3A+ rated, panel mount | 1 | [ ] |
| 11 | 18 AWG hookup wire (red) | Stranded, 2 feet | 1 | [ ] |
| 12 | 18 AWG hookup wire (black) | Stranded, 2 feet | 1 | [ ] |
| 13 | Heat shrink tubing (assorted) | 3mm, 5mm, 8mm diameter | 1 pack | [ ] |
| 14 | Mounting screws/standoffs | M3 or #4-40, for ZK-PP2K and buck converter | 8+ | [ ] |
| 15 | Ring terminals or spade connectors | For resistor connections | 4 | [ ] |
| 16 | Zip ties | Small, for wire management | 10+ | [ ] |

### 2B. Mat Parts

| # | Part | Specification | Qty | Check |
|---|------|--------------|-----|-------|
| 17 | 22 AWG magnet wire (enamel coated copper) | 1/2 lb spool minimum per 6 coils | varies | [ ] |
| 18 | Propane bottle (empty, standard green) | ~100mm / 4in diameter, used as coil form | 1 | [ ] |
| 19 | Yoga mat or foam mat | Full body: 24" x 72". Mini: 24" x 36" | 1 | [ ] |
| 20 | Contact cement | Spray or brush-on | 1 can | [ ] |
| 21 | Electrical tape | Standard width, quality brand | 2 rolls | [ ] |
| 22 | 16 AWG hookup wire (stranded) | For interconnecting coils. Red + Black. 10 ft each | 2 pcs | [ ] |
| 23 | Cable (mat to connector) | 16 AWG, 2-conductor, 4-6 feet long | 1 | [ ] |
| 24 | Solder | 60/40 rosin core or lead-free | 1 spool | [ ] |
| 25 | Fabric cover (optional) | To cover and protect mat coils | 1 | [ ] |

### 2C. Tools Required (NOT included in BOM)

| Tool | Required For | Mandatory? |
|------|-------------|------------|
| Soldering iron (30-60W) | All solder joints | YES |
| Digital multimeter | Resistance, continuity, voltage checks | YES |
| Magnetic compass | Polarity verification | YES |
| Wire strippers | Hookup wire prep | YES |
| Heat gun or lighter | Heat shrink tubing | YES |
| Drill with bits | Enclosure holes for connectors, vents | YES |
| Sandpaper (220 grit) | Cleaning enamel off magnet wire ends | YES |
| Lighter or butane torch | Burning enamel off magnet wire ends | YES |
| Screwdrivers (Phillips + flathead) | Various fastening | YES |
| Scissors or utility knife | Mat cutting, tape | YES |
| Gaussmeter (WT10A or similar) | Gauss measurement | RECOMMENDED |
| Step drill bit (Unibit) | Clean holes in plastic enclosure | RECOMMENDED |

### 2D. Visual Parts Identification

**ZK-PP2K Module:** Small blue PCB (approx 65x55mm) with LCD screen, 3 push buttons, screw terminals on edges labeled IN+ IN- OUT+ OUT-. Has a power LED. This is the brain of the system.

**4-Ohm Power Resistor:** Large ceramic or aluminum-housed resistor. Much bigger than a typical resistor. Will be labeled "4R" or "4 ohm" and have a wattage rating of 100W or higher. Often gold/green ceramic with wire leads, or aluminum block with screw terminals.

**GX16 Aviator Connector:** Round metal connector, approximately 16mm diameter, with threaded locking ring. The male (pins) goes in the box. The female (sockets) goes on the mat cable. These lock together with a twist.

**Buck Converter Module:** Small PCB with a potentiometer (tiny screw adjustment), input/output screw terminals, and an inductor (coil wrapped in tape or a small drum component). Typically has "IN+" "IN-" "OUT+" "OUT-" labels.

---

## SECTION 3: COIL WINDING

### 3A. Overview

Each coil is made by winding 95 wraps of 22 AWG magnet wire around a propane bottle (approximately 100mm diameter). The finished coil will be a flat pancake approximately 100mm across.

**Per coil specifications:**
- Wire: 22 AWG enamel-coated magnet wire (copper)
- Wraps: 95
- Form diameter: ~100mm (propane bottle)
- Expected resistance: ~3.3 ohms per coil
- Expected field: 45-55 gauss at surface when powered

**Number of coils to wind:**

| Mat Size | Coils Needed | Wiring Config |
|----------|-------------|---------------|
| Mini (localized) | 6 | 2 parallel strings of 3 in series |
| Medium (half body) | 10 | 2 parallel strings of 5 in series |
| Full body | 15 | 3 parallel strings of 5 in series |
| Full body (premium) | 20 | 4 parallel strings of 5 in series |

**IMPORTANT: Wind 1-2 EXTRA coils beyond what you need.** This gives you spares in case a coil is damaged during assembly.

### 3B. Step-by-Step Coil Winding

**Step 1: Prepare the propane bottle.**
- Use a clean, empty standard green propane bottle (the kind used for camping stoves).
- Wipe the surface clean and dry. Any grit will snag the wire.
- Optional: wrap one layer of masking tape around the bottle where you will wind. This makes coil removal easier.

**Step 2: Secure the starting wire.**
- Tape the end of the magnet wire to the bottle with a small piece of masking tape, leaving a 6-inch (15cm) tail hanging free. This tail will become one of your connection leads.
- Label this tail "START" with a piece of tape and a marker.

**Step 3: Wind 95 wraps.**
- Wind the wire around the bottle, keeping each wrap tight and directly next to the previous one.
- Maintain consistent tension. The wire should be snug but do not pull so hard that it stretches or kinks.
- Count every wrap. Losing count means starting over or accepting an unknown count.
- TIP: Count in groups of 10. Every 10th wrap, make a small pencil mark on your tape or note it down.
- The wire will naturally try to stack into multiple layers as 95 wraps will not fit in a single layer on a 100mm form. This is normal. Keep the winding as flat (pancake-like) as possible.
- If using a drill as a winding jig: USE THE LOWEST SPEED SETTING. High speed will break the wire.

**Step 4: Secure the coil IMMEDIATELY after winding.**
- THIS IS CRITICAL. The coil will "spring open" and unwind violently if not secured immediately.
- While still holding the coil against the bottle, tape across the coil at four points, 90 degrees apart (12 o'clock, 3 o'clock, 6 o'clock, 9 o'clock positions).
- Then wrap electrical tape around the entire circumference of the coil. Pull the tape tight -- Steeve Bradet recommends "near the breaking point of the tape" for maximum coil integrity.
- Leave a 6-inch (15cm) tail on the end wire. Label this tail "END."

**Step 5: Remove the coil from the bottle.**
- Gently slide the taped coil off the propane bottle.
- If it resists, gently twist while pulling. Do not yank -- this can damage the wire.
- Wrap one more full layer of tape around the coil for protection.

**Step 6: Prepare wire ends for soldering.**
- The magnet wire is coated with enamel insulation. You MUST remove this coating from both ends before soldering.
- Method 1 (preferred): Hold a lighter flame to the last 1 inch (25mm) of each wire end for 3-5 seconds. The enamel will burn off, leaving dark/blackened copper.
- Method 2: Sand both ends with 220-grit sandpaper until you see bright shiny copper. Sand all the way around the wire.
- After burning, sand lightly to remove residue and expose clean copper.
- Test with multimeter: touch probes to both sanded ends. You should get a resistance reading of approximately 3.3 ohms. If you get "OL" (open line) or infinite resistance, the enamel is not fully removed. Sand or burn more.

**Step 7: Label the coil.**
- Write a coil number on the tape: COIL-01, COIL-02, etc.
- Keep the START and END labels on the wire tails. These matter for polarity verification.

### 3C. Coil Winding Quality Checks

After winding each coil, verify:

| Check | Expected Result | Action if Fail |
|-------|----------------|----------------|
| Resistance (multimeter, ohms) | 3.0 - 3.8 ohms | If too low: check for shorted turns (enamel damage). If too high: check wire end prep |
| Continuity (multimeter, beep mode) | Continuous beep | If no beep: broken wire inside coil. Discard and rewind |
| Physical integrity | No loose turns, no kinks, tape secure | Re-tape if loose. Rewind if kinked |
| Wire ends prepped | Shiny copper visible on both ends | Re-sand or re-burn ends |
| Labels present | Coil number, START, END marked | Label before proceeding |

**Record each coil's resistance in the QC log (Section 9).**

---

## SECTION 4: POLARITY VERIFICATION (CRITICAL)

### 4A. Why This Section Is Non-Negotiable

**If you skip this section or get it wrong, the mat will have dead zones where the magnetic field cancels itself out.** The user will get reduced or zero therapeutic effect in those areas. This is the single most common defect in PEMF mats, including those from commercial manufacturers.

### 4B. How Magnetic Polarity Works

Every coil produces a magnetic field with a North pole and a South pole, like a bar magnet. The direction of the field depends on which direction the current flows through the wire.

```
        NORTH (field exits coil)
            ^  ^  ^  ^
            |  |  |  |
    ========================
    ||      COIL          ||  <-- Current flows clockwise when
    ========================      viewed from NORTH side
            |  |  |  |
            v  v  v  v
        SOUTH (field enters coil)
```

When two coils are placed side by side:

**CONSTRUCTIVE (correct -- fields ADD together):**
```
    N    N    N    N    N
    ^    ^    ^    ^    ^
    |    |    |    |    |
  [COIL] [COIL] [COIL] [COIL] [COIL]
    |    |    |    |    |
    v    v    v    v    v
    S    S    S    S    S

  Result: Uniform field. Full coverage. Maximum Weber (total flux).
```

**DESTRUCTIVE (wrong -- fields CANCEL at boundaries):**
```
    N    S    N    S    N
    ^    v    ^    v    ^
    |    |    |    |    |
  [COIL] [COIL] [COIL] [COIL] [COIL]
    |    |    |    |    |
    v    ^    v    ^    v
    S    N    S    N    S

  Result: Dead zones between every other coil. Field cancels.
          User gets gaps in coverage. BAD.
```

### 4C. Testing Each Coil With a Compass

**You need a temporary power source for this test.** Use the completed control box (Section 5) or a bench power supply set to 12-24V DC with a current-limiting resistor.

**Test procedure for each coil:**

1. Connect the coil to a power source through a resistor (4 ohm, or the control box output).
2. Power on. The ZK-PP2K should be set to a low frequency (1-5 Hz) so you can see the compass needle move.
3. Hold a standard magnetic compass flat, directly above the center of the coil, about 1 inch (25mm) away.
4. Watch the compass needle. On each pulse, the NORTH end of the compass needle (usually the red end) will be either ATTRACTED toward the coil or REPELLED away from it.
5. Note which end of the compass needle points DOWN toward the coil during a pulse:
   - If the RED (north) end of the compass dips DOWN toward the coil: the coil's NORTH pole is on the bottom (south is facing up). Mark this coil "SOUTH UP" or "S-UP."
   - If the RED (north) end of the compass points UP/AWAY from the coil: the coil's NORTH pole is facing up toward you. Mark this coil "NORTH UP" or "N-UP."

**IMPORTANT:** It does not matter whether you choose "all North up" or "all South up." What matters is that ALL coils are the SAME. Pick one direction and verify every single coil matches.

### 4D. Marking Convention

Use a permanent marker on the tape of each coil:

```
        .-~~~-.
      .'       '.          This dot/arrow marks
     /  COIL-01  \         which side faces UP
    |    N-UP     |         when installed in the mat.
    |    (dot)    |
     \           /
      '.       .'
        '-...-'
```

Draw a large dot or arrow on the side of the coil that will face UP (toward the user) when installed in the mat. Write "N-UP" or "S-UP" next to it.

### 4E. What To Do If a Coil Has Wrong Polarity

**Do NOT rewind the coil.** Simply swap the two wire leads.

If coil-05 reads "S-UP" while all others read "N-UP":
1. Disconnect coil-05's wires.
2. Reconnect the START wire where the END wire was, and vice versa.
3. Re-test with compass. It should now read "N-UP" like the others.

This works because reversing the current direction through a coil reverses its magnetic field direction. Swapping the leads is electrically identical to physically flipping the coil upside down.

### 4F. Polarity Verification Checklist

**EVERY coil must be checked. No exceptions.**

| Coil # | Resistance (ohms) | Polarity (N-UP or S-UP) | Matches Standard? | Verified By |
|--------|-------------------|------------------------|--------------------|-------------|
| COIL-01 | _____ | _____ | [ ] YES | _____ |
| COIL-02 | _____ | _____ | [ ] YES | _____ |
| COIL-03 | _____ | _____ | [ ] YES | _____ |
| COIL-04 | _____ | _____ | [ ] YES | _____ |
| COIL-05 | _____ | _____ | [ ] YES | _____ |
| COIL-06 | _____ | _____ | [ ] YES | _____ |
| COIL-07 | _____ | _____ | [ ] YES | _____ |
| COIL-08 | _____ | _____ | [ ] YES | _____ |
| COIL-09 | _____ | _____ | [ ] YES | _____ |
| COIL-10 | _____ | _____ | [ ] YES | _____ |
| COIL-11 | _____ | _____ | [ ] YES | _____ |
| COIL-12 | _____ | _____ | [ ] YES | _____ |
| COIL-13 | _____ | _____ | [ ] YES | _____ |
| COIL-14 | _____ | _____ | [ ] YES | _____ |
| COIL-15 | _____ | _____ | [ ] YES | _____ |
| COIL-16 | _____ | _____ | [ ] YES | _____ |
| COIL-17 | _____ | _____ | [ ] YES | _____ |
| COIL-18 | _____ | _____ | [ ] YES | _____ |
| COIL-19 | _____ | _____ | [ ] YES | _____ |
| COIL-20 | _____ | _____ | [ ] YES | _____ |

(Use only the rows you need for your coil count.)

**Standard chosen for this build:** [ ] N-UP / [ ] S-UP (circle one, then ALL coils must match)

**STOP: Do not proceed to mat assembly until EVERY coil in the above table shows "YES" in the "Matches Standard" column.**

---

## SECTION 5: CONTROL BOX ASSEMBLY

### 5A. Enclosure Preparation

1. **Plan the layout** before drilling. Place all components inside the box (without connecting them) to determine positions.

Suggested layout (viewed from front of box):

```
   FRONT PANEL (faces user)
   +--------------------------------------------+
   |                                             |
   |   [POWER    [ZK-PP2K LCD      [VENT        |
   |    SWITCH]   visible           HOLES]       |
   |              through                        |
   |              cutout]                        |
   +--------------------------------------------+

   REAR PANEL
   +--------------------------------------------+
   |                                             |
   |   [DC BARREL   [GX16 AVIATOR   [VENT       |
   |    JACK]        CONNECTOR]      HOLES]      |
   |                                             |
   +--------------------------------------------+

   TOP PANEL (LID)
   +--------------------------------------------+
   |                                             |
   |        [FAN MOUNT - intake or exhaust]      |
   |        (cut 80mm or 120mm circle)           |
   |                                             |
   +--------------------------------------------+

   OUTSIDE OF BOX (rear or side)
   +--------------------------------------------+
   |                                             |
   |   [4-OHM POWER RESISTOR MOUNTED HERE]      |
   |   (bolted to outside surface with standoffs)|
   |                                             |
   +--------------------------------------------+
```

2. **Drill/cut holes for:**
   - DC barrel jack (rear panel) -- measure your specific jack diameter
   - GX16 aviator connector (rear panel) -- typically 16mm hole
   - Power switch (front panel) -- measure your specific switch
   - ZK-PP2K LCD window (front panel) -- rectangular cutout to see the display
   - Fan mount (top) -- 80mm or 120mm circle with screw holes
   - Ventilation holes (at least 6-8 holes, 6mm diameter, on the side opposite the fan)
   - Resistor mounting holes (OUTSIDE surface) -- 2 holes for M4 bolts or screws

3. **Deburr all holes** with a file or sandpaper. No sharp edges that could cut wires.

### 5B. Resistor Mounting (OUTSIDE the Box)

**The 4-ohm power resistor dissipates approximately 57 watts of heat. It MUST be mounted on the OUTSIDE of the project box with adequate airflow around it.**

If you mount it inside, it will overheat the enclosure and potentially damage other components.

1. Position the resistor on the outside surface of the box (rear or side panel).
2. Use standoffs (10-15mm) to create an air gap between the resistor body and the box surface.
3. Bolt through the box wall using M4 hardware: bolt -> washer -> box wall -> washer -> standoff -> resistor -> washer -> nut.
4. Run the resistor's connection wires through two small grommeted holes into the box interior.
5. Verify the resistor is firmly mounted and does not wobble.

```
SIDE VIEW:
                        +-----------+
                        | RESISTOR  |  <-- 4 ohm, 100-200W
                        +-----------+
                        |  standoff |  <-- 10-15mm air gap
========================|===========|========================
|  BOX INTERIOR         |   bolt    |                        |
|                       | (through  |                        |
|                       |   wall)   |                        |
=============================================================
```

### 5C. Internal Wiring

**COMPLETE WIRING DIAGRAM:**

```
                           INSIDE THE BOX
+================================================================+
|                                                                  |
|  DC BARREL  ----+---- POWER SWITCH ----+                        |
|  JACK (24V)     |                      |                        |
|                 |                      |                        |
|               [GND bus]          [+24V switched]                |
|                 |                      |                        |
|                 |            +---------+---------+               |
|                 |            |                   |               |
|                 |       ZK-PP2K (IN+)      BUCK CONVERTER        |
|                 |            |              (VIN+)               |
|                 +-------ZK-PP2K (IN-)      (VIN-)---+           |
|                 |            |              (VOUT+)--+--FAN+    |
|                 |       ZK-PP2K (OUT+)     (VOUT-)--+--FAN-    |
|                 |            |                                   |
|                 |            | (wire goes through box wall       |
|                 |            |  to EXTERNAL resistor)            |
|                 |            |                                   |
+==================|============|===================================+
                   |            |
  OUTSIDE BOX:     |            |
                   |     +------+
                   |     |
                   |   [4-OHM RESISTOR]
                   |     |
                   |     +------+
                   |            |
                   |     GX16 AVIATOR CONNECTOR
                   |      PIN 1 (signal/hot)
                   |
                   +---- GX16 AVIATOR CONNECTOR
                          PIN 2 (ground/return)
```

**Step-by-step wiring instructions:**

**STEP 1: Power input wiring**
1. Solder the DC barrel jack's positive terminal to one terminal of the power switch.
2. Solder the DC barrel jack's negative terminal to a common ground bus (a short piece of wire that will connect to multiple ground points).

**STEP 2: ZK-PP2K power input**
3. Solder a wire from the other terminal of the power switch to the ZK-PP2K "IN+" terminal. This is switched +24V.
4. Solder a wire from the ground bus to the ZK-PP2K "IN-" terminal.

**STEP 3: Buck converter for fan**
5. Solder a wire from switched +24V (same point as step 3) to the buck converter "VIN+" input.
6. Solder a wire from the ground bus to the buck converter "VIN-" input.
7. BEFORE connecting the fan: power on the circuit and use a multimeter on the buck converter's output terminals. Adjust the potentiometer screw until the output reads 12.0V (+/- 0.5V). Power off.
8. Solder the fan's red wire to buck converter "VOUT+".
9. Solder the fan's black wire to buck converter "VOUT-".

**STEP 4: ZK-PP2K to resistor to aviator connector (signal path)**
10. Solder a wire from ZK-PP2K "OUT+" terminal. Route this wire through a grommeted hole to the OUTSIDE of the box.
11. Connect this wire to one terminal of the 4-ohm power resistor (outside the box).
12. From the OTHER terminal of the resistor, run a wire back through another grommeted hole into the box and to PIN 1 of the GX16 aviator connector.
13. Solder a wire from the ground bus to PIN 2 of the GX16 aviator connector.
14. Connect ZK-PP2K "OUT-" to the ground bus.

**HEAT SHRINK EVERY SOLDER JOINT.** No exceptions. Slide heat shrink tubing onto the wire BEFORE soldering, then slide it over the joint and shrink it with a heat gun.

### 5D. Buck Converter Voltage Setting

This must be done before the fan is connected, or at minimum before final assembly.

1. Connect the 24V power supply to the barrel jack.
2. Turn on the power switch.
3. The ZK-PP2K LCD should light up. Verify the display shows frequency and duty cycle values.
4. Measure the buck converter output with a multimeter (red probe on VOUT+, black on VOUT-).
5. Using a small flathead screwdriver, turn the potentiometer on the buck converter until the multimeter reads 12.0V.
6. Power off.

### 5E. ZK-PP2K Initial Settings

With the control box powered on (but NOT connected to the mat yet):

1. Set the ZK-PP2K to **PWM mode** (not Pulse mode).
2. Set frequency to **10 Hz** (use the buttons to navigate and adjust).
3. Set duty cycle to **10%**.
4. Verify the LCD displays these values correctly.
5. The ZK-PP2K saves settings when powered off. You can adjust later, but 10 Hz / 10% is a safe starting point.

### 5F. Fan and Ventilation

1. Mount the fan to the lid or top panel of the box using the screw holes in the fan's corners.
2. Orient the fan to blow air INTO the box (intake). The vent holes on the opposite side of the box allow warm air to exit.
3. Alternatively, orient the fan to EXHAUST from the box. Either direction works as long as air flows through the box.
4. Verify the fan spins freely and does not hit any wires.

### 5G. Control Box Assembly QC Checks

Before closing the box, verify:

| Check | Expected Result | Pass? |
|-------|----------------|-------|
| Power on: ZK-PP2K LCD displays | Shows frequency + duty cycle | [ ] |
| Fan spins when powered on | Spinning, audible airflow | [ ] |
| Buck converter output | 11.5-12.5V on multimeter | [ ] |
| No loose wires | All connections soldered + heat shrunk | [ ] |
| Resistor mounted OUTSIDE box | Firm, with air gap from standoffs | [ ] |
| GX16 connector secured | Tight in panel, no rotation | [ ] |
| Power switch functions | Click on = LCD on. Click off = LCD off | [ ] |
| No wire pinch points | Close lid partially, check clearance | [ ] |

---

## SECTION 6: MAT ASSEMBLY

### 6A. Coil Layout Planning

Before gluing anything, plan where each coil will go. Lay them out on the mat substrate.

**Spacing rule:** Center-to-center distance between adjacent coils should be approximately 1.0-1.5x the coil diameter. For 100mm coils, this means 100-150mm between coil centers. Closer spacing gives more uniform coverage.

**Layout examples:**

**6-coil mini mat (24" x 36"):**
```
+------------------------------------------+
|                                          |
|    (COIL-1)    (COIL-2)    (COIL-3)     |  <-- String A (series)
|                                          |
|    (COIL-4)    (COIL-5)    (COIL-6)     |  <-- String B (series)
|                                          |
+------------------------------------------+
    CABLE EXIT (to aviator connector) -->
```

**10-coil medium mat (24" x 48"):**
```
+--------------------------------------------------+
|                                                    |
|  (C-1)   (C-2)   (C-3)   (C-4)   (C-5)          |  String A
|                                                    |
|  (C-6)   (C-7)   (C-8)   (C-9)   (C-10)         |  String B
|                                                    |
+--------------------------------------------------+
```

**15-coil full body mat (24" x 72"):**
```
+------------------------------------------------------------------------+
|                                                                          |
|  (C-1)   (C-2)   (C-3)   (C-4)   (C-5)                               |  String A
|                                                                          |
|  (C-6)   (C-7)   (C-8)   (C-9)   (C-10)                              |  String B
|                                                                          |
|  (C-11)  (C-12)  (C-13)  (C-14)  (C-15)                              |  String C
|                                                                          |
+------------------------------------------------------------------------+
```

**20-coil full body premium mat (24" x 72"):**
```
+------------------------------------------------------------------------+
|                                                                          |
|  (C-1)   (C-2)   (C-3)   (C-4)   (C-5)                               |  String A
|                                                                          |
|  (C-6)   (C-7)   (C-8)   (C-9)   (C-10)                              |  String B
|                                                                          |
|  (C-11)  (C-12)  (C-13)  (C-14)  (C-15)                              |  String C
|                                                                          |
|  (C-16)  (C-17)  (C-18)  (C-19)  (C-20)                              |  String D
|                                                                          |
+------------------------------------------------------------------------+
```

### 6B. Verify Polarity Orientation Before Gluing

**LAST CHANCE CHECK:** Before any coil is glued down, confirm that the marked "UP" side (from Section 4) is facing UP (toward where the user will lie).

All coils should have their polarity dot/arrow visible from above.

### 6C. Gluing Coils to Mat

1. Work one coil at a time.
2. Apply contact cement to the bottom (non-marked side) of the coil in a thin, even layer.
3. Apply contact cement to the mat surface where the coil will sit.
4. Wait for the contact cement to become tacky (typically 2-5 minutes, per product instructions).
5. Carefully place the coil onto the mat, polarity mark facing UP.
6. Press firmly for 30 seconds.
7. Repeat for all coils.

**Do NOT rush this step.** Contact cement bonds permanently on contact. If a coil is placed crooked, it is very difficult to reposition.

### 6D. Inter-Coil Wiring

**Wiring rule: Coils within each string are wired in SERIES. Strings are wired in PARALLEL to each other.**

**Series wiring within a string:**
- Connect the END wire of COIL-1 to the START wire of COIL-2.
- Connect the END wire of COIL-2 to the START wire of COIL-3.
- And so on for all coils in the string.
- The START wire of the first coil and the END wire of the last coil are the string's two output leads.

**CRITICAL:** When you verified polarity in Section 4 using a specific START and END convention, you must wire the coils in the same direction. If you tested COIL-1 with START on the positive terminal and got "N-UP," then in the series chain, current must flow through COIL-2, COIL-3 etc. in the same START-to-END direction. The simplest way: always connect END of previous coil to START of next coil.

```
STRING A (series):

   START                                                    END
     |                                                       |
  [COIL-1] --END-to-START-- [COIL-2] --END-to-START-- [COIL-3]
                                                              |
   (These two wires are String A's leads)              STRING A
     |                                                   LEAD +
  STRING A
   LEAD -
```

**Parallel wiring between strings:**

```
                STRING A LEAD(-)  ----+---- STRING B LEAD(-)  ----+
                                      |                           |
                                      +------ MAIN LEAD (-)------+
                                                    |
                                              [TO CABLE]

                STRING A LEAD(+)  ----+---- STRING B LEAD(+)  ----+
                                      |                           |
                                      +------ MAIN LEAD (+)------+
                                                    |
                                              [TO CABLE]
```

For 3 or 4 strings in parallel, add the additional strings the same way -- all negative leads tied together, all positive leads tied together.

### 6E. Wiring Diagram (Complete, 6-Coil Example)

```
                      MAT INTERIOR

  STRING A (3 coils in series):

  MAIN(-)----[COIL-1]----[COIL-2]----[COIL-3]----+
                                                   |
  MAIN(+)----[COIL-4]----[COIL-5]----[COIL-6]----+

  STRING B (3 coils in series)

  Where:
  ---- means: END of left coil soldered to START of right coil
  MAIN(-) and MAIN(+) are joined (String A negative to String B negative,
                                   String A positive to String B positive)
  These two MAIN leads go to the cable.
```

**Alternate clearer representation for 6-coil:**

```
             MAIN(-) --------+----------------------------+
                              |                            |
                         [COIL-1]                    [COIL-4]
                              |                            |
                         [COIL-2]                    [COIL-5]
                              |                            |
                         [COIL-3]                    [COIL-6]
                              |                            |
             MAIN(+) --------+----------------------------+

  STRING A: COIL-1 -> COIL-2 -> COIL-3 (in series, ~9.9 ohms)
  STRING B: COIL-4 -> COIL-5 -> COIL-6 (in series, ~9.9 ohms)

  String A parallel with String B = ~4.95 ohms total
```

### 6F. Expected Total Resistance

| Mat Config | Coils | Per-String Ohms | Strings in Parallel | Total Ohms |
|------------|-------|-----------------|---------------------|------------|
| 6-coil | 6 | 3 x 3.3 = 9.9 | 2 | ~5.0 |
| 10-coil | 10 | 5 x 3.3 = 16.5 | 2 | ~8.25 |
| 15-coil | 15 | 5 x 3.3 = 16.5 | 3 | ~5.5 |
| 20-coil | 20 | 5 x 3.3 = 16.5 | 4 | ~4.1 |

**Note:** Add the 4-ohm external resistor to the total for the complete circuit resistance. For example, a 6-coil mat has ~5.0 ohms from coils + 4.0 ohms from resistor = ~9.0 ohms total circuit resistance.

**Measure and record actual total mat resistance with multimeter before connecting to control box.** Acceptable range is within +/- 20% of the calculated value. Significant deviation indicates a wiring error.

### 6G. Cable and Connector

1. Solder the two MAIN leads from the mat to one end of the 2-conductor cable (16 AWG).
2. Heat shrink both solder joints.
3. Route the cable to the edge of the mat and secure it with tape or a cable tie so it will not snag.
4. At the other end of the cable, solder to the GX16 female (cable-mount) aviator connector.
   - MAIN(+) to Pin 1 (must match the pin you wired to the resistor output in the control box).
   - MAIN(-) to Pin 2 (must match the pin you wired to ground in the control box).
5. Heat shrink both connections inside the connector shell before screwing it closed.

**IMPORTANT: Document which pin is positive and which is negative. Mark the connector shell with a dot of paint or a label. If these get reversed, the coils will still pulse but their polarity will be reversed relative to your compass verification. This defeats the purpose of all the polarity work in Section 4.**

### 6H. Wire Routing and Protection

1. All inter-coil wires should lie flat on the mat surface.
2. Secure wires to the mat surface with small pieces of tape every 6 inches (15cm).
3. Optionally, apply a thin bead of contact cement over the wire paths to keep them permanently flat.
4. All solder joints between coils should be wrapped with heat shrink tubing, then taped flat to the mat.
5. No solder joints or wire should stick up more than 3mm above the mat surface. The user will be lying on this mat. Bumps are uncomfortable and can break under body weight.
6. Once all wiring is complete and tested, apply the fabric cover over the mat to protect the coils and wires.

---

## SECTION 7: MANDATORY QC CHECKS (PASS/FAIL)

**Every check in this section must pass before the unit ships.** A failure at any step requires corrective action before proceeding. Each check must be initialed by the person performing it.

### QC-01: Continuity Test on Each Individual Coil

**Tool:** Multimeter set to continuity/beep mode

**Procedure:** Touch probes to the START and END leads of each coil (before or after they are wired into the mat -- preferably both times).

| Coil | Continuity? | Initials |
|------|------------|----------|
| COIL-01 | [ ] PASS / [ ] FAIL | _____ |
| COIL-02 | [ ] PASS / [ ] FAIL | _____ |
| COIL-03 | [ ] PASS / [ ] FAIL | _____ |
| COIL-04 | [ ] PASS / [ ] FAIL | _____ |
| COIL-05 | [ ] PASS / [ ] FAIL | _____ |
| COIL-06 | [ ] PASS / [ ] FAIL | _____ |
| COIL-07 | [ ] PASS / [ ] FAIL | _____ |
| COIL-08 | [ ] PASS / [ ] FAIL | _____ |
| COIL-09 | [ ] PASS / [ ] FAIL | _____ |
| COIL-10 | [ ] PASS / [ ] FAIL | _____ |
| COIL-11 | [ ] PASS / [ ] FAIL | _____ |
| COIL-12 | [ ] PASS / [ ] FAIL | _____ |
| COIL-13 | [ ] PASS / [ ] FAIL | _____ |
| COIL-14 | [ ] PASS / [ ] FAIL | _____ |
| COIL-15 | [ ] PASS / [ ] FAIL | _____ |
| COIL-16 | [ ] PASS / [ ] FAIL | _____ |
| COIL-17 | [ ] PASS / [ ] FAIL | _____ |
| COIL-18 | [ ] PASS / [ ] FAIL | _____ |
| COIL-19 | [ ] PASS / [ ] FAIL | _____ |
| COIL-20 | [ ] PASS / [ ] FAIL | _____ |

**Failure action:** Broken wire inside coil. Replace the coil with a spare.

---

### QC-02: Resistance Measurement of Full Mat Circuit

**Tool:** Multimeter set to ohms (200 ohm range)

**Procedure:** Measure resistance across the two MAIN leads of the mat cable (at the aviator connector).

| Measurement | Expected | Actual | Pass? |
|-------------|----------|--------|-------|
| Mat resistance (coils only) | See table in 6F | _____ ohms | [ ] |
| Full circuit (mat + resistor) | Mat + 4.0 ohms | _____ ohms | [ ] |

**Acceptable range:** Within +/- 20% of expected value.
**Failure action:** If too high -- check for bad solder joint or broken wire (re-test individual coils). If too low -- check for short circuit between wires.
**Initials:** _____

---

### QC-03: Compass Verification of EVERY Coil Direction

**Tool:** Magnetic compass, powered control box, mat connected

**Procedure:** Set ZK-PP2K to 1-5 Hz, 50% duty cycle (for easy visibility). Hold compass over each coil. Verify ALL compass deflections are in the SAME direction.

| Coil | Compass deflection matches standard? | Initials |
|------|--------------------------------------|----------|
| COIL-01 | [ ] PASS / [ ] FAIL | _____ |
| COIL-02 | [ ] PASS / [ ] FAIL | _____ |
| COIL-03 | [ ] PASS / [ ] FAIL | _____ |
| COIL-04 | [ ] PASS / [ ] FAIL | _____ |
| COIL-05 | [ ] PASS / [ ] FAIL | _____ |
| COIL-06 | [ ] PASS / [ ] FAIL | _____ |
| COIL-07 | [ ] PASS / [ ] FAIL | _____ |
| COIL-08 | [ ] PASS / [ ] FAIL | _____ |
| COIL-09 | [ ] PASS / [ ] FAIL | _____ |
| COIL-10 | [ ] PASS / [ ] FAIL | _____ |
| COIL-11 | [ ] PASS / [ ] FAIL | _____ |
| COIL-12 | [ ] PASS / [ ] FAIL | _____ |
| COIL-13 | [ ] PASS / [ ] FAIL | _____ |
| COIL-14 | [ ] PASS / [ ] FAIL | _____ |
| COIL-15 | [ ] PASS / [ ] FAIL | _____ |
| COIL-16 | [ ] PASS / [ ] FAIL | _____ |
| COIL-17 | [ ] PASS / [ ] FAIL | _____ |
| COIL-18 | [ ] PASS / [ ] FAIL | _____ |
| COIL-19 | [ ] PASS / [ ] FAIL | _____ |
| COIL-20 | [ ] PASS / [ ] FAIL | _____ |

**Failure action:** Reversed coil. Swap that coil's leads (desolder, reverse, re-solder). Re-test.

---

### QC-04: Visual Inspection of All Solder Joints

**Tool:** Eyes (magnifying glass recommended)

**Procedure:** Inspect every solder joint in the control box and on the mat. Each joint should be:
- Shiny and smooth (not dull/grey/grainy -- cold joint)
- Fully covering the wire-to-wire or wire-to-terminal connection
- Covered with heat shrink tubing
- No stray solder blobs or solder bridges to adjacent connections

| Area | Joints Inspected | All Good? | Initials |
|------|------------------|-----------|----------|
| Control box interior | _____ joints | [ ] PASS / [ ] FAIL | _____ |
| Mat inter-coil connections | _____ joints | [ ] PASS / [ ] FAIL | _____ |
| Mat cable to aviator connector | 2 joints | [ ] PASS / [ ] FAIL | _____ |

**Failure action:** Re-solder any cold joints. Add heat shrink where missing. Remove any solder bridges.

---

### QC-05: Gauss Measurement (If Gaussmeter Available)

**Tool:** WT10A gaussmeter or similar, powered control box, mat connected

**Procedure:** Set ZK-PP2K to 10 Hz, 50% duty cycle. Place gaussmeter probe flat on the mat surface directly above each coil center.

| Coil | Gauss Reading | In Range (45-55G)? | Initials |
|------|---------------|---------------------|----------|
| COIL-01 | _____ G | [ ] YES / [ ] NO | _____ |
| COIL-02 | _____ G | [ ] YES / [ ] NO | _____ |
| COIL-03 | _____ G | [ ] YES / [ ] NO | _____ |
| COIL-04 | _____ G | [ ] YES / [ ] NO | _____ |
| COIL-05 | _____ G | [ ] YES / [ ] NO | _____ |
| COIL-06 | _____ G | [ ] YES / [ ] NO | _____ |
| COIL-07 | _____ G | [ ] YES / [ ] NO | _____ |
| COIL-08 | _____ G | [ ] YES / [ ] NO | _____ |
| COIL-09 | _____ G | [ ] YES / [ ] NO | _____ |
| COIL-10 | _____ G | [ ] YES / [ ] NO | _____ |
| COIL-11 | _____ G | [ ] YES / [ ] NO | _____ |
| COIL-12 | _____ G | [ ] YES / [ ] NO | _____ |
| COIL-13 | _____ G | [ ] YES / [ ] NO | _____ |
| COIL-14 | _____ G | [ ] YES / [ ] NO | _____ |
| COIL-15 | _____ G | [ ] YES / [ ] NO | _____ |
| COIL-16 | _____ G | [ ] YES / [ ] NO | _____ |
| COIL-17 | _____ G | [ ] YES / [ ] NO | _____ |
| COIL-18 | _____ G | [ ] YES / [ ] NO | _____ |
| COIL-19 | _____ G | [ ] YES / [ ] NO | _____ |
| COIL-20 | _____ G | [ ] YES / [ ] NO | _____ |

**Acceptable range:** 30-70 gauss. Target is 45-55 gauss. Readings should be consistent across all coils (+/- 15% of the average).

**If readings are significantly low on one coil:** Check that coil's connections. A bad solder joint will reduce current and therefore field strength.

**If no gaussmeter is available:** Skip this test but note "GAUSS TEST: NOT PERFORMED" on the sign-off form. The compass verification (QC-03) confirms the field is present and correctly oriented, but does not quantify strength.

---

### QC-06: Power-On Test -- ZK-PP2K Frequency Display

**Procedure:** With the mat connected, power on the control box.

| Check | Expected | Actual | Pass? |
|-------|----------|--------|-------|
| LCD powers on | Display visible | _____ | [ ] |
| Frequency displays correctly | Shows set frequency (e.g. 10 Hz) | _____ Hz | [ ] |
| Duty cycle displays correctly | Shows set duty cycle (e.g. 10%) | _____ % | [ ] |
| Buttons respond | Frequency and duty can be changed | _____ | [ ] |
| LED indicator pulses | Visible blinking at set frequency | _____ | [ ] |

**Initials:** _____

---

### QC-07: Heat Test (30-Minute Run)

**Procedure:** Set ZK-PP2K to 10 Hz, 20% duty cycle (higher duty cycle generates more heat for stress test). Run for 30 minutes continuously. Check temperatures every 10 minutes.

| Time | Resistor Temp (touch test) | Coil Temp (touch test) | Box Interior (touch test) | Pass? |
|------|---------------------------|------------------------|--------------------------|-------|
| 0 min | Room temp | Room temp | Room temp | [ ] |
| 10 min | _____ | _____ | _____ | [ ] |
| 20 min | _____ | _____ | _____ | [ ] |
| 30 min | _____ | _____ | _____ | [ ] |

**Temperature guidelines:**
- **Resistor:** Will be warm to hot. This is NORMAL -- it is dissipating ~57W. It should be hot but NOT burning (you should be able to touch it for 1-2 seconds without burning skin, roughly below 65C/150F). If you cannot touch it at all, add more airflow around the resistor or use a higher-wattage resistor.
- **Coils on mat:** Should be barely warm to the touch. If any coil is significantly hotter than the others, it may have a partial short (damaged enamel). Investigate.
- **Box interior:** Should be warm, not hot. The fan should be moving air.

**Failure action:** If anything is dangerously hot (burns on touch), power off immediately. Check resistor wattage rating, check for short circuits, verify fan operation.

**Initials:** _____

---

### QC-08: Fan Operational Check

**Procedure:** With the control box powered on, verify:

| Check | Expected | Pass? |
|-------|----------|-------|
| Fan spins | Visible rotation | [ ] |
| Airflow felt | Hold hand near vent holes, feel air movement | [ ] |
| No rattling or scraping | Smooth, quiet operation | [ ] |
| Fan does not stop after 10 min | Still running | [ ] |

**Failure action:** Check 12V buck converter output. Check fan wiring. Replace fan if defective.

**Initials:** _____

---

### QC-09: Full Mat Field Coverage Check

**Tool:** Magnetic compass

**Procedure:** With the mat powered on (1-5 Hz, 50% duty cycle), slowly sweep a compass across the ENTIRE mat surface in a grid pattern. The compass needle should deflect at every point on the mat that is near or over a coil.

| Area | Compass deflects? | Consistent direction? | Pass? |
|------|---------------------|----------------------|-------|
| Top-left quadrant | [ ] YES / [ ] NO | [ ] YES / [ ] NO | [ ] |
| Top-right quadrant | [ ] YES / [ ] NO | [ ] YES / [ ] NO | [ ] |
| Bottom-left quadrant | [ ] YES / [ ] NO | [ ] YES / [ ] NO | [ ] |
| Bottom-right quadrant | [ ] YES / [ ] NO | [ ] YES / [ ] NO | [ ] |
| Center of mat | [ ] YES / [ ] NO | [ ] YES / [ ] NO | [ ] |
| Between coils | [ ] YES / [ ] NO | [ ] YES / [ ] NO | [ ] |

**Expected:** Deflection should be strong directly over each coil and decrease between coils. The direction of deflection should be the SAME everywhere (constructive field).

**Failure action:** If a dead spot is found directly over a coil, that coil has a wiring issue. If adjacent coils show opposite deflection, one coil's leads are reversed (go back to QC-03).

**Initials:** _____

---

### QC-10: Timer Function Test (Using External Bathroom Timer)

**Procedure:** Plug the control box power supply into a standard mechanical bathroom timer (120V).

| Check | Expected | Pass? |
|-------|----------|-------|
| Set timer to 5 minutes | Timer dial turns, clicks | [ ] |
| System powers on through timer | ZK-PP2K activates, mat pulses | [ ] |
| Timer counts down and shuts off | System powers down automatically at 0 | [ ] |
| System fully off after timer expires | No display, no pulsing, fan stops | [ ] |

**Note:** The bathroom timer is a simple, proven, fail-safe method for session timing. If the timer mechanism fails, it fails to the OFF position (power disconnected), which is the safe state.

**Initials:** _____

---

## SECTION 8: SAFETY WARNINGS

### ABSOLUTE CONTRAINDICATIONS -- INCLUDE WITH EVERY UNIT

The following must be communicated to every end user, in writing:

**DO NOT USE this device if you have:**
- A pacemaker or any implanted electronic medical device
- An insulin pump
- A deep brain stimulator
- A vagal nerve stimulator
- Any other implanted device that could be affected by magnetic fields

**CONSULT A DOCTOR before use if you have:**
- Epilepsy or seizure history
- Active cancer or tumors
- Pregnancy
- Active bleeding disorders
- Organ transplant with immunosuppressive therapy
- Metal implants (generally considered safe, but verify with physician)
- Hyperthyroidism

### ELECTRICAL SAFETY RULES (FOR THE ASSEMBLER)

1. **The 4-ohm power resistor MUST be mounted OUTSIDE the project box with airflow around it.** It dissipates approximately 57 watts and will overheat inside a sealed enclosure.

2. **No exposed wire connections anywhere.** Every solder joint must be covered with heat shrink tubing. Every wire must be secured so it cannot shift and contact other conductors.

3. **Never run the power supply above 80% of its rated capacity.** A 6A supply at 24V = 144W. The system draws roughly 100-120W at typical settings. This provides adequate headroom.

4. **Use the correct wire gauge.** 18 AWG minimum for all connections carrying full load current. 22 AWG magnet wire is only acceptable for the coils themselves (which carry limited current due to the resistor).

5. **All connections to the power resistor must be secure.** Use ring terminals or heavy-duty solder joints. Loose connections at the resistor will arc and potentially cause fire.

6. **Keep away from water and moisture.** This device is not waterproof or water-resistant. Do not use near pools, baths, or in high-humidity environments where condensation can form on electronics.

7. **Do not operate unattended until thermal stability is verified** over at least three 30-minute sessions.

8. **Include a bathroom timer with every unit.** The timer provides a hardware-level session cutoff that does not depend on the user remembering to turn off the device.

9. **Never exceed 24V input to the system.** The ZK-PP2K, coils, and resistor values are calculated for 24V. Higher voltage can cause component failure.

10. **If any component (resistor, coil, wire, connector) shows signs of overheating, discoloration, melting smell, or smoke: POWER OFF IMMEDIATELY.** Unplug the power supply. Do not reconnect until the fault is identified and corrected.

### PRODUCT SAFETY LABEL TEXT

Include this on a label affixed to the control box:

```
PULSED ELECTROMAGNETIC FIELD (PEMF) DEVICE
Input: 24V DC, 6A max
Output: Pulsed magnetic field, 1-100 Hz, square wave

WARNING:
- Not for use with pacemakers or implanted electronic devices
- External resistor is hot during operation -- do not touch
- Do not submerge in water or operate in wet conditions
- Use timer to limit session duration
- Not a medical device -- for wellness use only
- Read all instructions before use
```

---

## SECTION 9: PHOTOS AND SIGN-OFF

### Required Photos (Assembler Must Capture)

Take a clear, well-lit photo of each of the following. Store photos in a folder named by the unit serial number.

| Photo # | Subject | Required Details Visible | Taken? |
|---------|---------|--------------------------|--------|
| P-01 | All parts laid out before assembly | Every BOM item visible | [ ] |
| P-02 | Individual coil (representative) | Tape wrapping, wire tails, label | [ ] |
| P-03 | Compass test setup | Compass on coil, deflection visible | [ ] |
| P-04 | Control box interior (wired, open) | All connections visible | [ ] |
| P-05 | External resistor mounting | Standoffs, air gap visible | [ ] |
| P-06 | Buck converter voltage reading | Multimeter showing ~12V | [ ] |
| P-07 | Mat coil layout (before cover) | All coils positioned, polarity marks visible | [ ] |
| P-08 | Mat wiring (before cover) | All inter-coil connections visible | [ ] |
| P-09 | Total mat resistance reading | Multimeter showing ohms value | [ ] |
| P-10 | ZK-PP2K powered on (frequency display) | LCD readable, showing settings | [ ] |
| P-11 | Completed control box (closed) | External view, all panel items visible | [ ] |
| P-12 | Completed mat (with cover) | Final product, cable visible | [ ] |
| P-13 | Gaussmeter reading (if available) | Probe on mat, reading visible | [ ] |
| P-14 | Full system connected and running | Box + mat + cable, powered on | [ ] |

### Build Sign-Off Form

```
================================================================
         PEMF MAT ASSEMBLY SIGN-OFF FORM
================================================================

Serial Number:    ____________________
Build Date:       ____________________
Builder Name:     ____________________
Builder Initials: ____________________

MAT CONFIGURATION:
  [ ] 6-coil mini    [ ] 10-coil medium
  [ ] 15-coil full   [ ] 20-coil premium

COIL SPECIFICATIONS:
  Wire gauge: 22 AWG
  Wraps per coil: 95
  Coils wound: ____
  Coils installed: ____

MEASURED VALUES:
  Average coil resistance: _______ ohms
  Total mat resistance: _______ ohms
  Full circuit resistance (mat + resistor): _______ ohms
  Buck converter voltage: _______ V
  Average gauss per coil (if measured): _______ G

QC CHECKLIST:
  [ ] QC-01: Continuity - all coils pass
  [ ] QC-02: Resistance - within spec
  [ ] QC-03: Compass polarity - all coils match
  [ ] QC-04: Visual solder inspection - all joints good
  [ ] QC-05: Gauss measurement (if available)
  [ ] QC-06: Power-on display test
  [ ] QC-07: 30-minute heat test - pass
  [ ] QC-08: Fan operational
  [ ] QC-09: Full mat field coverage
  [ ] QC-10: Timer function

ALL PHOTOS TAKEN: [ ] YES / [ ] NO
Photo folder location: ____________________

NOTES / DEVIATIONS FROM SPEC:
______________________________________________________________
______________________________________________________________
______________________________________________________________
______________________________________________________________

ASSEMBLED BY:

Signature: ____________________  Date: ____________________
Print Name: ____________________

REVIEWED BY (if applicable):

Signature: ____________________  Date: ____________________
Print Name: ____________________

================================================================
```

---

## SECTION 10: TROUBLESHOOTING

### Common Issues and Solutions

| Symptom | Likely Cause | Solution |
|---------|-------------|----------|
| ZK-PP2K display not turning on | No power reaching module | Check barrel jack connection, power switch, PSU output with multimeter |
| Display on but no compass deflection on mat | Broken wire in signal path | Check resistor connections, aviator connector pins, mat cable continuity |
| One coil has no compass deflection | Broken coil or bad solder joint | Test that coil's resistance individually. Re-solder or replace |
| One coil deflects OPPOSITE direction | Reversed coil leads | Swap START and END leads on that coil. Re-test |
| Mat resistance much higher than expected | Cold solder joint or broken wire | Re-test each coil individually. Find the open connection |
| Mat resistance much lower than expected | Short circuit between coils | Inspect wiring for bare wire touching another bare wire |
| Resistor getting extremely hot (cannot touch) | Resistor wattage too low, or circuit resistance too low | Use a higher-wattage resistor (200W). Check that mat resistance is correct |
| Fan not spinning | Buck converter not set correctly, or fan dead | Check buck converter output (should be 12V). Try a different fan |
| Buzzing or humming from mat | Normal at certain frequencies. Louder = higher duty cycle | Reduce duty cycle. This is expected and not a defect |
| ZK-PP2K display shows frequency but it seems wrong | User interface confusion | Refer to ZK-PP2K manual. Ensure PWM mode (not Pulse mode) |
| Aviator connector does not lock | Wrong connector pairing | Verify male/female match and pin count match. Twist the locking ring |
| Gauss readings vary significantly between coils | Inconsistent coil winding, different distances | Ensure consistent wrap count. Measure at same distance from each coil |
| Mat gets warm after extended use | Higher duty cycle generates heat. Normal below 40C | Reduce duty cycle to 10%. If still hot, check for short circuits |
| Solder joint cracked after mat was folded | Stress fracture from bending | Re-solder. Add strain relief (extra wire slack) at each joint |

### Resistance Debugging Table

If total mat resistance is wrong, use this process to isolate the fault:

1. Disconnect all strings from each other (undo the parallel connections).
2. Measure each string individually.
3. If a string reads wrong, disconnect coils within that string one by one and test each.

| What You Measure | What It Means |
|------------------|---------------|
| Single coil: OL (infinite) | Broken wire inside coil. Replace coil |
| Single coil: 0 ohms | Shorted turns (enamel damage). Replace coil |
| Single coil: 3.0-3.8 ohms | Normal |
| 3-coil string: 9-11.4 ohms | Normal |
| 5-coil string: 15-19 ohms | Normal |
| String reads higher than sum of coils | Cold solder joint between two coils. Find and re-solder |
| String reads same as fewer coils than expected | One coil is being bypassed (short across its leads). Fix wiring |

---

## APPENDIX A: RECOMMENDED OPERATING SETTINGS FOR END USER

Include this card with each completed unit:

```
================================================================
           PEMF MAT -- QUICK START GUIDE
================================================================

1. Plug the power supply into a bathroom timer.
2. Plug the timer into a wall outlet.
3. Connect the mat cable to the control box (twist to lock).
4. Set the timer for your desired session length:
   - First use: 20 minutes
   - Regular use: 30-60 minutes
   - Sleep mode: up to 8 hours (at 1 Hz)

5. Turn on the power switch on the control box.

6. Set frequency using the ZK-PP2K buttons:
   DAYTIME:    10-14 Hz (alert, energizing)
   AFTERNOON:  7-8 Hz (relaxing)
   SLEEP:      1-3 Hz (sleep induction)

7. Set duty cycle: 10-20%
   (Higher = more warmth on the mat. Does NOT affect
   therapeutic effectiveness.)

8. Lie on the mat. Relax.

9. When the timer expires, the system shuts off automatically.

TROUBLESHOOTING:
- No display? Check that the power switch is ON and the
  timer has not expired.
- No sensation? This is NORMAL. Most people do not feel
  PEMF directly. The magnetic field is working even if
  you feel nothing.
- Drink water after each session.

NEVER USE IF YOU HAVE A PACEMAKER OR IMPLANTED
ELECTRONIC MEDICAL DEVICE.
================================================================
```

---

## APPENDIX B: WAVEFORM REFERENCE

Why square wave matters -- for the technically curious assembler:

```
SQUARE WAVE (what we use):
     ___     ___     ___     ___
    |   |   |   |   |   |   |   |
    |   |   |   |   |   |   |   |
____|   |___|   |___|   |___|   |____

    ^       ^       ^       ^
    |       |       |       |
    These vertical edges = maximum slew rate
    = maximum rate of change of magnetic field
    = maximum energy transfer to cells (via induction)


SINE WAVE (what we do NOT use):
       .-.       .-.       .-.
      /   \     /   \     /   \
     /     \   /     \   /     \
____/       \_/       \_/       \____

    Gradual transitions = low slew rate
    = weak energy transfer
    = NASA study showed no significant therapeutic effect


STATIC FIELD (permanent magnets -- no effect):
_________________________________________

    No change at all = zero energy transfer
    = NASA study showed zero cell growth effect
    even at 1,000-2,500 gauss
```

The therapeutic mechanism depends on the CHANGE in the magnetic field, not the strength of the field itself. A 50-gauss square wave with near-instantaneous rise time transfers more energy per pulse than a 500-gauss sine wave with a gradual rise.

---

## APPENDIX C: BILL OF MATERIALS -- SOURCING GUIDE

| Part | Search Term (Amazon) | Approx. Cost | Alt Source |
|------|---------------------|-------------|------------|
| ZK-PP2K | "ZK-PP2K PWM signal generator" | $5-8 | AliExpress, eBay |
| 24V 6A power supply | "24V 6A DC power supply" | $15-25 | Amazon |
| 4 ohm 100W resistor | "4 ohm 100W power resistor" | $8-15 | Mouser, DigiKey |
| 22 AWG magnet wire | "22 AWG magnet wire enamel copper" | $8-12 (1/2 lb) | Amazon |
| GX16 aviation connector pair | "GX16 2-pin aviation connector" | $5-8 (pair) | Amazon, AliExpress |
| DC barrel jack (panel mount) | "5.5x2.1mm DC panel mount jack" | $2-3 | Amazon |
| Buck converter (adjustable) | "LM2596 buck converter module" | $3-5 | Amazon, AliExpress |
| 80mm or 120mm 12V fan | "80mm 12V DC fan" | $5-8 | Amazon |
| Project box | "ABS project enclosure 200x150x100" | $8-12 | Amazon |
| Rocker switch | "rocker switch panel mount" | $2-3 | Amazon |
| 18 AWG hookup wire | "18 AWG stranded hookup wire" | $5-8 | Amazon |
| 16 AWG hookup wire | "16 AWG stranded wire" | $5-8 | Amazon |
| Heat shrink tubing kit | "heat shrink tubing assortment" | $5-8 | Amazon |
| Yoga mat (substrate) | "yoga mat 72 inch" | $10-20 | Amazon, any retailer |
| Contact cement | "contact cement spray" | $8-12 | Hardware store |
| Electrical tape | "electrical tape" | $3-5 | Hardware store |
| Propane bottle (coil form) | Standard green camping propane | $5-8 | Hardware store, Walmart |
| Bathroom timer | "bathroom timer mechanical" | $5-10 | Hardware store |
| Magnetic compass | "magnetic compass" | $3-5 | Amazon |

**Total estimated BOM cost (6-coil mini mat):** $120-180
**Total estimated BOM cost (15-coil full body mat):** $150-220
**Total estimated BOM cost (20-coil full body premium):** $170-250

(Costs do not include tools, labor, or gaussmeter.)

---

## DOCUMENT REVISION HISTORY

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2026-02-08 | Initial release | Assembly documentation team |

---

*This document is based on the publicly available YouTube tutorials and technical guidance of Steeve Bradet (PEMF with Steeve, @Steeve. on YouTube). It is provided for educational purposes. Any commercial use of this design should comply with all applicable local, state/provincial, and federal regulations regarding electronic devices and wellness products.*
