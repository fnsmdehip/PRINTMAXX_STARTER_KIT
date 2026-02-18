# DIY PEMF Device Build Guide

Comprehensive guide to building a Pulsed Electromagnetic Field therapy device at home. Covers three build tiers ($30-600), coil design, safety, and verified community projects.

**Disclaimer:** PEMF devices are not FDA-approved medical devices (with limited exceptions for bone healing). This guide is for educational and experimental purposes. Consult a healthcare provider before use. Do not use if you have a pacemaker, are pregnant, have active bleeding disorders, or have epilepsy/seizure history.

---

## Table of contents

1. [How PEMF works (the 30-second version)](#1-how-pemf-works)
2. [Core components every PEMF device needs](#2-core-components)
3. [The NASA finding that matters](#3-the-nasa-finding)
4. [Frequency protocol chart](#4-frequency-protocols)
5. [TIER 1 build: Basic ($30-80)](#5-tier-1-basic)
6. [TIER 2 build: Intermediate ($100-250)](#6-tier-2-intermediate)
7. [TIER 3 build: Advanced ($300-600)](#7-tier-3-advanced)
8. [Coil design deep dive](#8-coil-design)
9. [Achieving specific gauss levels](#9-gauss-targeting)
10. [Measuring and verifying output](#10-measurement)
11. [Safety](#11-safety)
12. [Existing open-source projects and community builds](#12-community-projects)
13. [Parts sourcing quick reference](#13-parts-sourcing)
14. [Arduino/ESP32 code reference](#14-code-reference)

---

## 1. How PEMF works

A PEMF device has three functional blocks:

```
Signal Generator --> Amplifier/Driver --> Coil (produces magnetic field)
```

1. **Signal generator** produces a low-frequency waveform (typically 1-100 Hz, square wave preferred)
2. **Amplifier/driver** boosts the signal to push enough current through the coil
3. **Coil** converts electrical current into a pulsed magnetic field measured in gauss (G) or tesla (T)

The pulsed magnetic field penetrates tissue and (per research) influences cell membrane potential, ion transport, and gene expression related to healing and regeneration.

**Unit conversions:**
- 1 Tesla = 10,000 Gauss
- 1 milliTesla (mT) = 10 Gauss
- 1 microTesla (uT) = 0.01 Gauss

---

## 2. Core components

Every DIY PEMF device needs these:

| Component | Function | Budget option | Better option |
|-----------|----------|---------------|---------------|
| **Signal generator** | Produces the waveform at target frequency | Smartphone app (free) | Arduino/ESP32 or XR2206 module ($5-15) |
| **Amplifier/driver** | Powers the coil with enough current | ZK-PP2K PWM module ($5-8) | Class D audio amp or MOSFET H-bridge ($15-40) |
| **Coil** | Converts current to magnetic field | Hand-wound copper coil ($5-15) | Multi-layer precision wound ($20-50) |
| **Power supply** | Provides DC voltage | Old laptop charger 19V ($0-free) | ATX PC PSU 12V/20A ($15-30) |
| **Wiring** | Connects everything | 18 AWG hookup wire ($5) | 12 AWG for high current ($8) |
| **Enclosure** | Houses electronics | Plastic project box ($5) | 3D printed custom ($10) |

**Optional but recommended:**
- Gaussmeter to verify output ($20-60)
- Timer/relay module for session control ($3-8)
- Heat sink for MOSFETs ($3-5)
- Fuse holder + fuse for safety ($2)

---

## 3. The NASA finding

NASA Technical Paper 2003-212054 tested five waveform types on neural stem cells:

| Waveform | Cell growth increase |
|----------|---------------------|
| Static/DC | Minimal |
| Sine wave | Low |
| Triangle wave | Low-moderate |
| Delta impulse | Moderate |
| **Square wave** | **Up to 4x (400%)** |

**NASA's optimal parameters:**
- **Frequency:** 10 Hz
- **Waveform:** Square wave (rapid rise/fall time, high dB/dT)
- **Intensity:** 1-20 microTesla (0.01-0.2 Gauss) -- note: very low intensity
- **Key finding:** The rapid rate of change (dB/dT) matters more than raw intensity
- **Results:** 160+ growth/regeneration genes upregulated, 300-400% increase in mitochondrial density

This means: for general wellness, you do NOT need hundreds of gauss. Sub-1 gauss at the right frequency and waveform may be more effective than brute-force intensity. However, for deep tissue penetration (bone healing, dense muscle), higher gauss (50-300) is used clinically.

---

## 4. Frequency protocols

Based on published research and clinical device manufacturer recommendations:

### Frequency ranges by application

| Frequency range | Application | Research basis |
|----------------|-------------|----------------|
| **1-3 Hz** | Deep relaxation, sleep, cortisol regulation | Delta brainwave entrainment |
| **4-7 Hz** | Meditation, stress relief, anxiety | Theta brainwave range |
| **7.83 Hz** | Schumann resonance (Earth's natural frequency), general wellness | Schumann resonance research |
| **8-10 Hz** | Relaxation, mild pain relief, cellular repair | NASA study (10 Hz optimal), alpha brainwave |
| **10-15 Hz** | Bone healing, fracture repair, tissue regeneration | Multiple clinical studies, FDA-cleared bone stimulators use 15 Hz |
| **15-30 Hz** | Pain relief, inflammation reduction, circulation | Clinical PEMF devices (4-30 Hz standard range) |
| **40 Hz** | Neurological applications, cognitive function | Gamma brainwave research |
| **50-75 Hz** | Cartilage repair, osteoarthritis, joint inflammation | 75 Hz shown superior for cartilage in PMC study |
| **100 Hz** | Acute pain, nerve stimulation | Higher-frequency clinical protocols |

### Recommended starting protocol

- **Frequency:** 10 Hz (NASA-validated, good general starting point)
- **Waveform:** Square wave
- **Duty cycle:** 10% (on 10% of each cycle, off 90%)
- **Session duration:** 20-30 minutes
- **Sessions per day:** 1-2
- **Intensity:** Start low, increase gradually

### Duty cycle explanation

At 10 Hz with 10% duty cycle:
- Each cycle = 100ms (1/10 Hz)
- Pulse ON time = 10ms
- Pulse OFF time = 90ms
- This pulsing pattern is what creates the rapid dB/dT that NASA found effective

Commercial devices from reputable manufacturers use: 4-30 Hz frequency, 5-15% duty cycle, 4-23 gauss output.

---

## 5. TIER 1 build: Basic ($30-80)

The simplest functional PEMF device. Uses a pre-built PWM driver module and hand-wound coil.

### Architecture

```
Power Supply (12-19V DC) --> ZK-PP2K PWM Module --> Coil
```

### Parts list

| Part | Specification | Approx. cost | Source |
|------|--------------|-------------|--------|
| ZK-PP2K PWM Signal Generator/Driver Module | 3.3-30V, 8A max, LCD display, freq 1Hz-150KHz, duty 0-100% | $5-8 | Amazon (B09GCQ8KMH), AliExpress, eBay |
| Laptop power supply (recycled) | 19V DC, 3A+ (50W minimum) | $0 (recycled) or $8-12 new | Any old laptop charger, Amazon |
| Magnet wire (lacquered copper) | 22 AWG (0.64mm), 1/2 lb spool | $8-12 | Amazon, electronics suppliers |
| Plastic coil form | 17cm (6.7") diameter, PVC pipe section or 3D printed | $3-5 | Hardware store, PVC pipe |
| DC barrel jack connector | Matching laptop PSU connector | $2 | Amazon |
| Hookup wire | 18 AWG, stranded, 10 feet | $3-5 | Amazon |
| Project enclosure | Plastic, ~150x100x50mm | $5-8 | Amazon |
| **TOTAL** | | **$26-50** | |

### Coil winding (Tier 1)

**Target coil specifications:**
- Diameter: 17cm (6.7 inches) -- good for limb/joint applications
- Wire: 22 AWG lacquered copper (0.64mm diameter)
- Turns: 180
- Expected resistance: ~12 ohms
- Expected inductance: ~5 mH
- Expected output: 10-15 gauss

**Winding steps:**
1. Cut a section of 17cm diameter PVC pipe, 3cm tall, as a coil form
2. Drill a small hole near the bottom edge for the wire start
3. Thread the wire through and leave 30cm (12") tail
4. Wind 180 turns tightly, layer by layer. Keep turns neat and close together
5. Secure the outer end with tape, leave 30cm tail
6. Wrap completed coil with electrical tape for protection
7. Solder leads to longer hookup wire for connection to the driver module

**Resistance check (important):**
- With 19V supply: coil must be at least 9 ohms (to protect MOSFET)
- With 12V supply: coil must be at least 6 ohms
- Measure with multimeter before connecting. If below minimum, add more turns

### Assembly steps

1. **Test the ZK-PP2K module** on its own first -- connect power supply, verify LCD displays and buttons work
2. **Set frequency:** Use the module's buttons to set frequency to 10 Hz (or 13 Hz, the default in many PEMF projects)
3. **Set duty cycle:** Set to 10%
4. **Set mode:** PWM mode (not pulse mode)
5. **Connect coil:** Wire the coil to the module's output terminals (polarity does not matter for the coil)
6. **Power on:** Connect power supply. The LED indicator should pulse at the set frequency
7. **Test:** Hold a compass near the coil. The needle should deflect with each pulse. Alternatively, place a small magnet near the coil -- you should feel or hear a gentle tick at each pulse
8. **Enclose:** Mount everything in the project box. Drill holes for the DC jack and coil wires

### ZK-PP2K module settings for PEMF

The ZK-PP2K has an LCD screen and 3 buttons for adjustment:

- **PWM mode:** Set frequency (1 Hz to 150 KHz) and duty cycle (0-100%)
- **PULSE mode:** Set number of pulses, delay time, pulse width
- **For PEMF use PWM mode:** Frequency = 10 Hz, Duty = 10%
- **Power-down memory:** Settings are saved when powered off

---

## 6. TIER 2 build: Intermediate ($100-250)

Adds digital control, higher power output, multiple frequency presets, and better coil design. Two approach options.

### Option A: Smartphone + Class D Amplifier approach

This is the most elegant intermediate build. Your phone becomes a programmable signal generator with 0.01 Hz precision.

**Architecture:**
```
Smartphone (Signal Gen App) --> 3.5mm cable --> Class D Amplifier --> Coil
```

**Parts list:**

| Part | Specification | Approx. cost | Source |
|------|--------------|-------------|--------|
| Class D Bluetooth Audio Amplifier Board | TPA3116D2, 2x50W, 12-24V DC input | $15-25 | Amazon, AliExpress |
| OR: DFRobot XY-WRBT Bluetooth 5.0 Audio Receiver Board | Bluetooth receiver + amp in one | $12-18 | Amazon, DFRobot |
| Laptop power supply | 19V DC, 3A+ | $0-12 | Recycled or new |
| 3.5mm AUX cable | Standard audio cable | $3 | Amazon |
| Magnet wire | 20 AWG (0.81mm), 1 lb spool | $12-18 | Amazon |
| Coil form | 20cm diameter, rigid plastic or PVC | $5 | Hardware store |
| Smartphone app | "Signal Generator" by XYZ-Apps (Android, free) OR "Frequency Sound Generator" by LuxDeLux | $0 | Google Play / App Store |
| Project enclosure | Larger plastic box ~200x150x70mm | $8-10 | Amazon |
| Banana plug connectors (optional) | For easy coil swapping | $5 | Amazon |
| Heat sink for amp board | Aluminum, small | $3-5 | Amazon |
| **TOTAL** | | **$63-116** | |

**Coil winding (Tier 2):**
- Diameter: 20cm
- Wire: 20 AWG lacquered copper (0.81mm, thicker = lower resistance = stronger field)
- Turns: 200
- Target resistance: ~5 ohms (sweet spot for 50W amp)
- Expected output: ~20 gauss with 50W amplifier at ~5 ohm coil

**Assembly:**
1. Wind the coil per specifications above
2. Connect the amplifier board to the 19V power supply
3. Connect phone to amp via 3.5mm AUX cable (or pair via Bluetooth)
4. Connect coil to amp output where speakers would normally connect (use one channel)
5. Open Signal Generator app on phone
6. Set: Square wave, 10 Hz, amplitude at 50% to start
7. Press play. You should hear/feel the coil pulsing
8. **Volume controls intensity:** Phone volume + amp gain = total power to coil. Start at 30-50% and increase gradually
9. Never exceed 80% volume to protect the coil from overheating

**Signal Generator app settings:**
- Waveform: Square (most effective per NASA research)
- Frequency: 10 Hz (adjustable with 0.01 Hz precision)
- The app lets you save presets for different protocols (bone healing, relaxation, pain, etc.)

**Why this approach is good:**
- Infinite frequency adjustment via phone app
- Save multiple protocol presets
- Bluetooth means no cable between phone and amp
- Total cost under $120
- Matches or exceeds many $200-500 commercial devices

### Option B: Arduino/ESP32 + MOSFET Driver approach

More DIY, fully programmable, no phone needed.

**Architecture:**
```
Arduino Nano / ESP32 --> MOSFET Gate Driver --> Power MOSFET(s) --> Coil
                                                      ^
                                            Power Supply (12-24V)
```

**Parts list:**

| Part | Specification | Approx. cost | Source |
|------|--------------|-------------|--------|
| Arduino Nano (or ESP32 DevKit) | ATmega328P / ESP32-WROOM-32 | $5-12 | Amazon, AliExpress |
| N-Channel MOSFET | IRF3205 (55V, 110A) or IRFZ44N (55V, 49A) | $2-5 (pack of 5) | Amazon |
| Gate resistor | 100 ohm, 1/4W | $0.50 | Amazon (assortment pack) |
| Flyback diode | 1N5408 (3A, 1000V) -- CRITICAL for coil protection | $1 (pack of 10) | Amazon |
| Pull-down resistor | 10K ohm, 1/4W (keeps MOSFET off when Arduino boots) | $0.50 | Amazon |
| Power supply | 12V 5A (60W) switching PSU | $10-15 | Amazon |
| Magnet wire | 20 AWG, 1 lb | $12-18 | Amazon |
| OLED display (optional) | 0.96" I2C SSD1306 128x64 | $5-8 | Amazon |
| Rotary encoder (optional) | KY-040, for frequency/duty adjustment | $3 | Amazon |
| Buttons (optional) | Tactile pushbuttons for preset selection | $2 | Amazon |
| Perfboard or PCB | 70x90mm prototype board | $3 | Amazon |
| Enclosure | Plastic project box | $8 | Amazon |
| Heat sink | For MOSFET, TO-220 clip-on or aluminum block | $3-5 | Amazon |
| **TOTAL** | | **$55-130** | |

**Circuit schematic (text description):**
```
Arduino Pin D9 (PWM) --> 100 ohm resistor --> MOSFET Gate (IRF3205)
Arduino GND --> MOSFET Source
MOSFET Source --> Power Supply GND
MOSFET Drain --> Coil terminal 1
Coil terminal 2 --> Power Supply +12V
1N5408 diode across coil: Cathode to +12V, Anode to MOSFET Drain
   (this flyback diode protects the MOSFET from voltage spikes when coil switches off)
10K pull-down resistor: MOSFET Gate to GND
```

**Important: The flyback diode (1N5408) is NON-NEGOTIABLE.** Coils generate voltage spikes (back-EMF) when current is suddenly switched off. Without the flyback diode, these spikes WILL destroy your MOSFET, possibly your Arduino, and potentially cause a fire. Always include it.

**Assembly:**
1. Build the MOSFET driver circuit on perfboard per schematic above
2. Upload the Arduino code (see Section 14)
3. Connect 12V power supply
4. Connect coil to MOSFET drain and +12V
5. Power on Arduino via USB (separate from 12V supply)
6. Verify pulsing with compass or multimeter set to AC mode

### PC-Controlled Option (Tier 2 variant)

Uses computer sound card as signal generator with high-power MOSFET driver.

**Architecture:**
```
PC (CHIamp software or Audacity) --> Line Out --> Signal Shifter Circuit --> 3x MOSFET (IRF3205) --> Coil
```

**Key components (from mircemk's Hackster.io project):**
- 3x IRF3205 power MOSFETs
- 3x 100 ohm resistors
- 1N5408 diode
- 10K potentiometer (intensity control)
- NPN transistor + 2 resistors (signal level shifter -- converts audio-level signal to MOSFET gate-level)
- 12V, 60W minimum power supply

**Software:** CHIamp by Ken Uzzell (free) or Audacity (free, generate tones at any frequency)

**Output:** Up to 150 gauss depending on coil design and power supply.

---

## 7. TIER 3 build: Advanced ($300-600)

Comparable to commercial devices selling for $1,000-5,000. Programmable protocols, high gauss output, professional coils, temperature monitoring, and safety shutoffs.

### Architecture

```
Arduino Nano/ESP32
  |
  |--> OLED Display (protocol info, gauss estimate, timer)
  |--> Rotary Encoder (frequency select)
  |--> Buttons (protocol presets, start/stop)
  |--> Thermistor(s) (coil + MOSFET temperature monitoring)
  |
  |--> MOSFET Gate Driver (IR2110 or similar)
        |
        |--> Multiple parallel MOSFETs (SCRs for highest power)
              |
              |--> Professional-grade coil(s) (multiple coil options)
                    |
              Power Supply (12V 20A ATX PSU or 24V 10A)
```

### Parts list

| Part | Specification | Approx. cost | Source |
|------|--------------|-------------|--------|
| Arduino Nano or ESP32 | Main controller | $5-12 | Amazon |
| MOSFET gate driver IC | IR2110 or IR2104 (bootstrap high/low side driver) | $5-8 | Amazon, Mouser |
| Power MOSFETs | 4-8x IRF3205 (paralleled for high current) or 4x P50N06 | $8-15 | Amazon |
| SCRs (optional, for highest power) | Silicon Controlled Rectifiers (as used in AuroraSky design) | $10-15 | Mouser, DigiKey |
| Flyback diodes | 4x 1N5408 (one per MOSFET pair) | $2 | Amazon |
| Gate resistors | 8x 100 ohm | $1 | Amazon |
| Thermistors | 2x NTC 10K (coil temp + MOSFET temp monitoring) | $3 | Amazon |
| ATX power supply | 12V / 20A (from old PC, or buy new) | $0-30 | Recycled or Amazon |
| OR: 24V switching PSU | 24V, 10A, 240W | $25-35 | Amazon |
| OLED display | 1.3" I2C SSD1306 | $6-8 | Amazon |
| Rotary encoder | KY-040 with push button | $3 | Amazon |
| Tactile buttons | 4x for preset protocols | $2 | Amazon |
| Status LEDs | 3x (power, active, overheat warning) | $1 | Amazon |
| Professional magnet wire | 12 AWG (2.05mm), 168 feet / 5 lbs | $40-60 | Amazon, wire suppliers |
| Coil form (large) | 8" (20cm) inner diameter, machined or 3D printed | $15-30 | 3D print or machine shop |
| Aluminum heat sink | Large, for MOSFET array | $8-12 | Amazon |
| PCB (custom) | Double-sided, designed in KiCad/EagleCAD, ordered from PCBWay/JLCPCB | $15-25 (5 boards) | PCBWay, JLCPCB |
| Enclosure | Aluminum or thick ABS, ventilated | $20-30 | Amazon |
| Fuse holder + 15A fuse | Safety cutoff | $3 | Amazon |
| Main power switch | Rocker switch, 15A rated | $3 | Amazon |
| Banana jack connectors | For interchangeable coil connection | $5 | Amazon |
| Silicone wire | 12 AWG, high-flex, for coil connections | $8 | Amazon |
| **TOTAL** | | **$195-400** | |

### Professional coil design (Tier 3)

**High-output localized applicator:**
- 12 AWG wire (2.05mm diameter) -- handles high current
- 144 turns (12 rows x 12 layers)
- 8" (20cm) inner diameter
- Expected resistance: ~0.5-2 ohms
- Expected output: 100-300 gauss (depending on power supply current)
- Weight: several pounds (12 AWG wire is heavy)

**Reference:** The ELEMENT Elite commercial device uses 144 turns of 12 AWG wire at 8" diameter and achieves 292 gauss continuous. The AuroraSky open-source project uses 168 feet of 12-gauge wire and achieves "many hundreds of gauss."

**Full body mat coil:**
- Use 18-20 AWG wire for lighter weight
- 6-8 separate coils wired in series or parallel
- Mounted on a yoga mat or flexible substrate
- Coils spaced evenly along the mat (head, shoulders, mid-back, lower back, hips, legs)
- Contact-cement the wire to the mat substrate
- Total mat size: ~2' x 6'
- Lower gauss per coil (distributed), but full-body coverage

### Safety features (Tier 3)

The Arduino code should implement:

1. **Temperature monitoring:** Read thermistors on coil and MOSFETs. Auto-shutoff at 60C (as in AuroraSky design)
2. **Session timer:** Configurable 1-60 minutes, auto-stop
3. **Overheat LED:** Warning indicator
4. **Current limiting:** Monitor via low-side shunt resistor (optional)
5. **Protocol presets:** Store 5-10 common protocols in EEPROM
6. **Ramped start:** Gradually increase duty cycle over first 30 seconds (gentler onset)

### Protocol presets (program into Arduino)

| Preset | Frequency | Duty cycle | Duration | Application |
|--------|-----------|------------|----------|-------------|
| Sleep | 3 Hz | 8% | 30 min | Pre-sleep relaxation |
| Schumann | 7.83 Hz | 10% | 20 min | General wellness |
| NASA | 10 Hz | 10% | 30 min | Cellular repair (NASA-validated) |
| Bone | 15 Hz | 12% | 30 min | Fracture/bone healing |
| Pain | 25 Hz | 15% | 20 min | Pain relief |
| Inflammation | 40 Hz | 10% | 20 min | Anti-inflammatory |
| Cartilage | 75 Hz | 10% | 30 min | Joint/cartilage repair |

---

## 8. Coil design deep dive

### Flat pancake coil vs. solenoid coil

| Feature | Flat pancake coil | Solenoid coil |
|---------|-------------------|---------------|
| **Shape** | Flat spiral, like a cinnamon roll | Cylindrical, like a spring |
| **Field pattern** | Concentrated at center, rapid falloff | More uniform along axis |
| **Best for** | Localized treatment (joints, specific areas) | Larger area coverage, body wrapping |
| **Ease of winding** | Easier (wind on flat surface) | Requires a form/mandrel |
| **Penetration** | Good at close range | Better at distance |
| **Use in mats** | Common in commercial PEMF mats | Less common in mats |
| **DIY difficulty** | Easy | Easy-moderate |

### Wire gauge selection

| AWG | Diameter (mm) | Max current (A) | Resistance per 100ft (ohms) | Best for |
|-----|---------------|-----------------|----------------------------|----------|
| 12 | 2.05 | 20+ | 0.16 | Tier 3, high-power, professional |
| 14 | 1.63 | 15 | 0.25 | Tier 3, good balance power/weight |
| 16 | 1.29 | 10 | 0.40 | Tier 2-3, moderate power |
| 18 | 1.02 | 7 | 0.64 | Tier 2, mat coils |
| 20 | 0.81 | 5 | 1.02 | Tier 1-2, general purpose |
| 22 | 0.64 | 3 | 1.61 | Tier 1, basic builds |
| 24 | 0.51 | 2 | 2.57 | Portable/low-power only |
| 28 | 0.32 | 0.5 | 6.39 | Very low power/portable |

**Rule of thumb:** Going from 12 AWG to 18 AWG cuts current capacity in half. Less current = weaker field (if you keep turns constant).

**Thicker wire (lower AWG number) = lower resistance = higher current = stronger magnetic field** but heavier and more expensive.

### Coil diameter considerations

The magnetic field formula for a simple coil: **B = (N x u0 x I) / (2R)**

Where:
- B = magnetic field strength (Tesla)
- N = number of turns
- u0 = permeability of free space (4pi x 10^-7 T*m/A)
- I = current in amps
- R = coil radius in meters

**Key relationships:**
- More turns (N up) = stronger field
- More current (I up) = stronger field
- Larger radius (R up) = weaker field (inverse relationship)
- A smaller coil produces a stronger field at its center, but covers less area

### Recommended coil designs by application

**Joint/knee/elbow applicator:**
- Diameter: 15-20 cm (6-8")
- Wire: 20-22 AWG
- Turns: 150-200
- Wrap around the joint

**Back/torso pad:**
- Diameter: 25-30 cm (10-12")
- Wire: 18-20 AWG
- Turns: 100-150
- Flat pancake style, embed in cushion

**Full body mat (multiple coils):**
- 6-8 coils, each 15-20 cm diameter
- Wire: 20 AWG
- Turns: 80-120 per coil
- Wired in series (same current through all) or parallel (higher current per coil)
- Spacing: 15-20 cm between coil centers
- Substrate: yoga mat or foam pad

**Helmet/head applicator (use with extreme caution):**
- Helmholtz coil pair: two identical coils separated by distance = radius
- Produces the most uniform field between coils
- Diameter: 20 cm
- Wire: 22-24 AWG (lower power for head)
- Turns: 100 per coil

### Helmholtz coil design

Two identical coils placed parallel, separated by a distance equal to the coil radius. Produces the most uniform magnetic field in the space between them.

**Helmholtz field formula:**
```
B = (8 / (5 * sqrt(5))) * (u0 * N * I) / R
B = 0.7155 * (u0 * N * I) / R
```

Where u0 = 4pi x 10^-7 T*m/A

**Example calculation:**
- N = 100 turns per coil
- I = 2 amps
- R = 0.1 m (10 cm radius, 20 cm diameter)
- B = 0.7155 * (4pi x 10^-7 * 100 * 2) / 0.1
- B = 0.7155 * (2.513 x 10^-4) / 0.1
- B = 0.7155 * 2.513 x 10^-3
- B = 1.8 x 10^-3 Tesla = 18 Gauss

**Online calculator:** Accel Instruments Helmholtz Coil Calculator (accelinstruments.com/Helmholtz-Coil/Helmholtz-coil-calculator.html) -- input your wire gauge, turns, diameter, and current to get precise field strength.

---

## 9. Gauss targeting

### How to achieve specific gauss levels

The magnetic field strength depends on three variables you can control:

**1. Current (I):** Determined by voltage / coil resistance (Ohm's law: I = V/R)
**2. Turns (N):** How many times the wire wraps around the coil form
**3. Radius (R):** Coil diameter / 2

To INCREASE gauss:
- Use thicker wire (lower AWG) to reduce resistance and allow more current
- Add more turns (but this also increases resistance, so use thicker wire)
- Use a smaller diameter coil (concentrates the field)
- Use a higher voltage power supply (more current through same resistance)

### Gauss targets by tier

| Target gauss | Turns | Wire gauge | Coil diameter | Power supply | Approx. cost |
|-------------|-------|------------|---------------|-------------|-------------|
| 1-5 G | 100-150 | 24-22 AWG | 15-20 cm | 12V, 1A | $30-50 |
| 10-20 G | 180-200 | 22-20 AWG | 17-20 cm | 19V, 3A or 12V, 5A | $50-100 |
| 20-50 G | 200-300 | 20-18 AWG | 15-20 cm | 12V, 10A | $100-200 |
| 50-100 G | 200-400 | 18-16 AWG | 15-20 cm | 12V, 20A (ATX PSU) | $150-300 |
| 100-300 G | 144+ | 12-14 AWG | 15-20 cm | 12V, 20A + parallel MOSFETs | $250-500 |

### Example calculations

**Tier 1 (10-15 gauss):**
- Coil: 180 turns, 22 AWG, 17cm diameter (8.5cm radius)
- Resistance: ~12 ohms
- With 19V supply: I = 19/12 = 1.58A (but pulsed at 10% duty cycle, so avg much lower)
- Peak B = (180 * 4pi*10^-7 * 1.58) / (2 * 0.085) = ~2.1 mT = ~21 Gauss at center
- Actual measured: 10-15 gauss (losses, imperfect winding, measurement distance)

**Tier 3 (100+ gauss):**
- Coil: 144 turns, 12 AWG, 20cm diameter (10cm radius)
- Resistance: ~0.7 ohms
- With 12V/20A supply: Peak I up to 17A (limited by MOSFET and PSU)
- Peak B = (144 * 4pi*10^-7 * 17) / (2 * 0.1) = ~15.4 mT = ~154 Gauss at center

---

## 10. Measurement and verification

### Gaussmeters / Tesla meters

You need a meter that can measure AC/pulsed fields (not just DC/static fields).

| Meter | Type | Range | Approx. cost | Notes |
|-------|------|-------|-------------|-------|
| Generic handheld gauss meter (Amazon) | DC + AC | 0-2000 mT | $20-35 | Search "digital gauss meter" or "tesla meter." Cheap ones may not respond fast enough for PEMF pulses |
| WT10A Tesla Meter | DC + AC | 0-2000 mT | $35-50 | Common budget option, has Hall probe |
| TriField TF2 EMF Meter | AC magnetic, electric, RF | 0-100 mT magnetic | $170 | High quality, measures AC magnetic fields well |
| Phone-based (phyphox app) | Uses phone's magnetometer | Limited range | Free | OK for basic verification (yes/no field present), not accurate for gauss measurement |

**DIY gaussmeter option:** Use an A1302 or SS49E linear Hall effect sensor ($2) with Arduino. Read analog voltage, calibrate against a known magnet. Not laboratory-grade but good enough to compare builds and verify output.

### Verification steps

1. **Compass test (free):** Hold a compass 10cm from the energized coil. The needle should deflect rhythmically at your pulse frequency. Confirms field is present
2. **Hall sensor test:** Place Hall sensor at coil center, read with Arduino/multimeter. Peak voltage corresponds to peak gauss
3. **Gaussmeter measurement:** Measure at coil center (strongest), then at 5cm, 10cm, 15cm distances to map falloff
4. **Frequency verification:** Use oscilloscope or Arduino to verify the actual output frequency and duty cycle match settings

---

## 11. Safety

### Absolute contraindications (DO NOT USE)

- **Pacemaker or implanted electronic device** -- PEMF can interfere with device function. This is the #1 risk
- **Pregnancy** -- Insufficient safety data
- **Active bleeding/hemorrhage** -- PEMF may increase blood flow
- **Organ transplant with immunosuppressants** -- Theoretical concern about immune stimulation
- **Near insulin pumps** -- Electromagnetic interference risk

### Relative contraindications (consult doctor first)

- Epilepsy/seizure history (especially for head applications)
- Active cancer/tumors (PEMF stimulates cell growth -- could theoretically promote tumor growth)
- Children/adolescents still growing
- Metal implants (screws, plates) -- generally OK per most sources, but check with doctor
- Hyperthyroidism
- Active tuberculosis

### Electrical safety

1. **ALWAYS include flyback diode across the coil.** Back-EMF from an inductive load (coil) can spike to hundreds of volts and destroy components or cause shock/fire
2. **Use a fuse.** A 10-15A fuse between the power supply and the circuit prevents runaway current
3. **Heat management.** MOSFETs and coils generate heat under load. Use heat sinks. Monitor temperature. Auto-shutoff at 60C
4. **Insulate connections.** Use heat shrink tubing on all solder joints. No exposed live connections
5. **Grounding.** If using a metal enclosure, ground it to the power supply ground
6. **Power supply quality.** Use a proper switching power supply with overcurrent protection. Do NOT use unregulated transformers directly
7. **Wire gauge for connections.** High-current connections (coil to MOSFET, PSU to circuit) must use appropriately thick wire. 2.5mm2 cross-section minimum for 10A+
8. **Capacitors.** Add a 100uF electrolytic capacitor across the power supply input for voltage smoothing and spike absorption
9. **Do NOT operate unattended** until you've verified thermal stability over multiple sessions
10. **Do NOT immerse in water** or use in wet environments

### Component quality -- do not cheap out on these

| Component | Why it matters |
|-----------|---------------|
| **MOSFETs** | Cheap counterfeits have lower current ratings than labeled. Buy from reputable sellers (Amazon brand-name listings, Mouser, DigiKey) |
| **Flyback diode** | Must be rated for the voltage spike. 1N5408 (1000V, 3A) is a safe choice. Using a weak diode = it fails = MOSFET dies |
| **Power supply** | Cheap unbranded PSUs may not have proper overcurrent protection. Use a known-brand ATX PSU or laptop charger |
| **Wire** | Must be actual copper magnet wire with proper insulation. Copper-clad aluminum (CCA) has higher resistance and may overheat |
| **Connectors** | High-current connections need proper terminals, not just twisted wire. Use screw terminals or soldered connections |

### EMF exposure limits

- ICNIRP guidelines for general public: 200 uT (2 gauss) for continuous exposure at power frequencies
- PEMF is pulsed and intermittent (not continuous), which is a different exposure profile
- Session duration: 20-30 minutes, 1-2x daily is the standard used in clinical studies
- No evidence of harm from PEMF at therapeutic levels in the published literature
- Always start with lower intensity and shorter sessions

### What can actually go wrong

| Risk | Cause | Prevention |
|------|-------|------------|
| **Electrical shock** | Exposed wiring, no grounding | Insulate everything, use enclosure, add fuse |
| **Fire** | MOSFET overheating, no flyback diode, wire too thin | Flyback diode, fuse, heat sink, proper wire gauge |
| **Component explosion** | Voltage spike from coil back-EMF | Flyback diode (non-negotiable) |
| **Burns** | Hot coil or MOSFET touching skin | Heat sink, temperature monitoring, insulated coil |
| **Pacemaker interference** | Using near implanted device | Absolute contraindication -- never use with pacemaker |
| **No effect** | Frequency/intensity wrong, coil wound wrong | Verify with gaussmeter, follow proven protocols |

---

## 12. Community projects and resources

### Maker projects (with schematics and instructions)

| Project | Platform | Description | Output | Cost | Link |
|---------|----------|-------------|--------|------|------|
| **Simplest PEMF (ZK-PP2K)** | Hackaday.io | ZK-PP2K module + coil, minimal parts | 10-15 gauss | ~$20 | hackaday.io/project/184563 |
| **High Power PEMF** | Hackster.io / Hackaday.io | ZK-PP1K + 8x MOSFETs + ATX PSU | ~100+ gauss | ~$50 | hackster.io/mircemk/simple-to-build-high-power-pemf-therapy-device-f38d46 |
| **PC-Controlled PEMF** | Hackster.io / DFRobot | PC sound card + MOSFET driver, CHIamp software | Up to 150 gauss | ~$40 | hackster.io/mircemk/diy-pc-controlled-high-power-pemf-therapy-device-212269 |
| **Portable PEMF Pulser** | DFRobot | Bluetooth amp + phone + battery | ~1 gauss | ~$25 | community.dfrobot.com/makelog-314196.html |
| **Schumann Resonance PEMF** | Hackaday.io / Hackster.io | 7.83 Hz generator module + amp + pancake coil | Low power | ~$15 | hackaday.io/project/201954 |
| **PEMF/RIFE Dual Device** | Instructables | Timer relay + PWM + Class D amp, dual channel | Variable | ~$20 | instructables.com/DIY-Multifunctional-Magnetic-Therapy-Device-PEMF-R |
| **AuroraSky High Power** | aurorasky.net | Arduino Nano + SCRs + thermistors, 18 frequencies, auto-shutoff | Hundreds of gauss | $239 (semi-kit) | aurorasky.net/html/high_powered_pemf.html |

### GitHub repositories

| Repo | Description | Hardware | Link |
|------|-------------|----------|------|
| **jakecoffman/pemf** | Arduino sketch for PEMF device | Adafruit Circuit Playground Express | github.com/jakecoffman/pemf |

Note: GitHub has limited PEMF-specific repos. Most projects are on Hackaday, Hackster.io, and Instructables.

### Community forums

| Forum | What to search | URL |
|-------|---------------|-----|
| **All About Circuits** | "PEMF" -- active discussions on coil driver design, ESP32 control | forum.allaboutcircuits.com |
| **Reddit r/PEMF** | DIY builds, device comparisons, frequency protocols | reddit.com/r/PEMF |
| **Hackaday.io** | PEMF projects with full schematics | hackaday.io (search "PEMF") |
| **Electro-Tech Online** | RIFE and PEMF dual circuit discussions | electro-tech-online.com |

### Key builder: mircemk

The user "mircemk" has published the most comprehensive DIY PEMF projects across Hackster.io, Hackaday.io, DFRobot, PCBWay, Instructables, and Electronicwings. Search their profile on any of these platforms for 5+ different PEMF builds at different complexity levels. Their projects include downloadable schematics and PCB files.

### Software tools

| Software | Purpose | Platform | Cost |
|----------|---------|----------|------|
| Signal Generator (XYZ-Apps) | Frequency/waveform generation via phone | Android | Free |
| Frequency Sound Generator (LuxDeLux) | Signal generation with Bluetooth | Android/iOS | Free |
| CHIamp (Ken Uzzell / Spectrotek) | PC-based frequency generator for PEMF | Windows | Free |
| Audacity | Generate tones at any frequency, export as audio | Win/Mac/Linux | Free |
| Online Tone Generator | Generate tones in browser | Web | Free |
| 66pacific.com coil calculator | Calculate coil inductance from dimensions | Web | Free |
| Accel Instruments Helmholtz Calculator | Calculate Helmholtz coil field strength | Web | Free |

---

## 13. Parts sourcing quick reference

### Amazon (fast shipping, moderate prices)

| Part | Search term | Approx. price |
|------|------------|---------------|
| ZK-PP2K PWM module | "ZK-PP2K PWM signal generator" | $5-8 |
| IRF3205 MOSFET (10-pack) | "IRF3205 MOSFET" | $8-10 |
| 1N5408 diode (10-pack) | "1N5408 diode" | $5 |
| 22 AWG magnet wire (1/2 lb) | "22 AWG magnet wire" | $8-12 |
| 20 AWG magnet wire (1 lb) | "20 AWG magnet wire" | $12-18 |
| 12 AWG magnet wire (5 lb) | "12 AWG magnet wire" | $40-60 |
| Arduino Nano | "Arduino Nano V3 ATmega328P" | $5-12 |
| ESP32 DevKit | "ESP32 DevKit V1" | $8-12 |
| TPA3116D2 amplifier board | "TPA3116D2 2x50W amplifier" | $15-25 |
| OLED display 0.96" | "SSD1306 OLED I2C" | $5-8 |
| Gauss meter | "digital gauss meter tesla meter" | $20-50 |
| ATX power supply | "ATX power supply 500W" | $25-35 |

### AliExpress (cheapest, 2-4 week shipping)

Same parts at 30-50% lower cost. Good for bulk or if you're not in a rush.

### Mouser / DigiKey (highest quality, verified components)

Use for MOSFETs, diodes, and ICs if you want guaranteed authentic parts. Slightly higher prices but no counterfeits.

### Free / recycled parts

- **Laptop power supply:** Any 19V laptop charger (HP, Dell, Lenovo -- most are 19V 3.4A+)
- **ATX power supply:** From any old desktop PC. Provides 12V at 20A+
- **Transformer primary winding:** An old E-type transformer (150W) has ~400 turns of 0.4mm copper wire at 16 ohms. You can rewind this or use as-is as a PEMF coil
- **Relay coils:** Old relays contain small coils of thin wire, usable for portable PEMF

---

## 14. Arduino/ESP32 code reference

### Basic Arduino PEMF controller

```cpp
// PEMF Controller - Basic
// Arduino Nano / Uno
// Drives MOSFET on pin D9 at configurable frequency and duty cycle

const int COIL_PIN = 9;        // PWM output to MOSFET gate (via 100 ohm resistor)
const int LED_PIN = 13;        // Built-in LED pulses with coil

// PEMF Parameters - adjust these
float frequency = 10.0;        // Hz (NASA optimal: 10 Hz)
float dutyCycle = 10.0;        // Percent (recommended: 5-15%)
unsigned long sessionTime = 1800000; // 30 minutes in milliseconds

// Calculated timing
unsigned long periodMicros;
unsigned long onTimeMicros;
unsigned long offTimeMicros;
unsigned long sessionStart;

void setup() {
  pinMode(COIL_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(COIL_PIN, LOW);  // Start with coil OFF

  Serial.begin(9600);
  Serial.println("PEMF Controller Starting");
  Serial.print("Frequency: "); Serial.print(frequency); Serial.println(" Hz");
  Serial.print("Duty Cycle: "); Serial.print(dutyCycle); Serial.println("%");
  Serial.print("Session: "); Serial.print(sessionTime / 60000); Serial.println(" minutes");

  // Calculate timing
  periodMicros = (unsigned long)(1000000.0 / frequency);
  onTimeMicros = (unsigned long)(periodMicros * dutyCycle / 100.0);
  offTimeMicros = periodMicros - onTimeMicros;

  Serial.print("Period: "); Serial.print(periodMicros); Serial.println(" us");
  Serial.print("ON time: "); Serial.print(onTimeMicros); Serial.println(" us");
  Serial.print("OFF time: "); Serial.print(offTimeMicros); Serial.println(" us");

  sessionStart = millis();
  delay(1000);  // 1 second delay before starting
}

void loop() {
  // Check session timer
  if (millis() - sessionStart >= sessionTime) {
    digitalWrite(COIL_PIN, LOW);
    digitalWrite(LED_PIN, LOW);
    Serial.println("Session complete.");
    while (1) { delay(1000); }  // Stop
  }

  // Pulse ON
  digitalWrite(COIL_PIN, HIGH);
  digitalWrite(LED_PIN, HIGH);
  delayMicroseconds(onTimeMicros);

  // Pulse OFF
  digitalWrite(COIL_PIN, LOW);
  digitalWrite(LED_PIN, LOW);
  delayMicroseconds(offTimeMicros);
}
```

### Advanced Arduino PEMF controller with presets and display

```cpp
// PEMF Controller - Advanced
// Arduino Nano with OLED display, rotary encoder, and protocol presets
// Requires libraries: Adafruit_SSD1306, Adafruit_GFX, Wire

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <EEPROM.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

// Pins
const int COIL_PIN = 9;
const int LED_PIN = 13;
const int ENCODER_CLK = 2;
const int ENCODER_DT = 3;
const int ENCODER_SW = 4;
const int START_BTN = 5;
const int THERMISTOR_COIL = A0;
const int THERMISTOR_FET = A1;

// Temperature safety
const float MAX_TEMP_C = 60.0;
const int THERMISTOR_NOMINAL = 10000;
const int TEMP_NOMINAL = 25;
const int B_COEFFICIENT = 3950;
const int SERIES_RESISTOR = 10000;

// Protocol presets
struct Protocol {
  const char* name;
  float frequency;
  float dutyCycle;
  unsigned long durationMin;
};

Protocol presets[] = {
  {"Sleep",         3.0,   8.0,  30},
  {"Schumann",      7.83, 10.0,  20},
  {"NASA 10Hz",    10.0,  10.0,  30},
  {"Bone Heal",    15.0,  12.0,  30},
  {"Pain Relief",  25.0,  15.0,  20},
  {"Anti-Inflam",  40.0,  10.0,  20},
  {"Cartilage",    75.0,  10.0,  30}
};
const int NUM_PRESETS = 7;

int currentPreset = 2;  // Default: NASA 10Hz
bool running = false;
unsigned long sessionStart = 0;

// Encoder state
volatile int encoderPos = 2;
int lastEncoderPos = 2;

void encoderISR() {
  if (digitalRead(ENCODER_DT) != digitalRead(ENCODER_CLK)) {
    encoderPos++;
    if (encoderPos >= NUM_PRESETS) encoderPos = 0;
  } else {
    encoderPos--;
    if (encoderPos < 0) encoderPos = NUM_PRESETS - 1;
  }
}

float readTemperature(int pin) {
  int reading = analogRead(pin);
  if (reading == 0) return 0;
  float resistance = SERIES_RESISTOR / (1023.0 / reading - 1.0);
  float steinhart = resistance / THERMISTOR_NOMINAL;
  steinhart = log(steinhart);
  steinhart /= B_COEFFICIENT;
  steinhart += 1.0 / (TEMP_NOMINAL + 273.15);
  steinhart = 1.0 / steinhart;
  steinhart -= 273.15;
  return steinhart;
}

void updateDisplay() {
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);

  // Protocol name
  display.setCursor(0, 0);
  display.setTextSize(2);
  display.println(presets[currentPreset].name);

  display.setTextSize(1);
  // Frequency
  display.setCursor(0, 20);
  display.print("Freq: ");
  display.print(presets[currentPreset].frequency);
  display.println(" Hz");

  // Duty cycle
  display.setCursor(0, 30);
  display.print("Duty: ");
  display.print(presets[currentPreset].dutyCycle);
  display.println("%");

  // Status
  display.setCursor(0, 40);
  if (running) {
    unsigned long elapsed = (millis() - sessionStart) / 60000;
    display.print("RUNNING ");
    display.print(elapsed);
    display.print("/");
    display.print(presets[currentPreset].durationMin);
    display.println("m");
  } else {
    display.println("READY - Press Start");
  }

  // Temperature
  display.setCursor(0, 52);
  float coilTemp = readTemperature(THERMISTOR_COIL);
  display.print("Coil:");
  display.print((int)coilTemp);
  display.print("C  FET:");
  display.print((int)readTemperature(THERMISTOR_FET));
  display.println("C");

  display.display();
}

void setup() {
  pinMode(COIL_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);
  pinMode(ENCODER_CLK, INPUT_PULLUP);
  pinMode(ENCODER_DT, INPUT_PULLUP);
  pinMode(ENCODER_SW, INPUT_PULLUP);
  pinMode(START_BTN, INPUT_PULLUP);

  digitalWrite(COIL_PIN, LOW);

  Serial.begin(9600);
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  display.clearDisplay();

  attachInterrupt(digitalPinToInterrupt(ENCODER_CLK), encoderISR, CHANGE);

  updateDisplay();
}

void loop() {
  // Check encoder for preset change
  if (encoderPos != lastEncoderPos && !running) {
    currentPreset = encoderPos;
    lastEncoderPos = encoderPos;
    updateDisplay();
  }

  // Start/stop button
  if (digitalRead(START_BTN) == LOW) {
    delay(200);  // Debounce
    if (running) {
      running = false;
      digitalWrite(COIL_PIN, LOW);
      digitalWrite(LED_PIN, LOW);
    } else {
      running = true;
      sessionStart = millis();
    }
    updateDisplay();
  }

  if (running) {
    // Temperature safety check
    float coilTemp = readTemperature(THERMISTOR_COIL);
    float fetTemp = readTemperature(THERMISTOR_FET);
    if (coilTemp > MAX_TEMP_C || fetTemp > MAX_TEMP_C) {
      running = false;
      digitalWrite(COIL_PIN, LOW);
      digitalWrite(LED_PIN, HIGH);  // Warning LED
      Serial.println("OVERHEAT SHUTDOWN");
      updateDisplay();
      return;
    }

    // Session timer check
    unsigned long sessionDuration = presets[currentPreset].durationMin * 60000UL;
    if (millis() - sessionStart >= sessionDuration) {
      running = false;
      digitalWrite(COIL_PIN, LOW);
      digitalWrite(LED_PIN, LOW);
      Serial.println("Session complete");
      updateDisplay();
      return;
    }

    // Generate pulse
    float freq = presets[currentPreset].frequency;
    float duty = presets[currentPreset].dutyCycle;
    unsigned long periodUs = (unsigned long)(1000000.0 / freq);
    unsigned long onUs = (unsigned long)(periodUs * duty / 100.0);
    unsigned long offUs = periodUs - onUs;

    digitalWrite(COIL_PIN, HIGH);
    digitalWrite(LED_PIN, HIGH);
    delayMicroseconds(onUs);
    digitalWrite(COIL_PIN, LOW);
    digitalWrite(LED_PIN, LOW);
    delayMicroseconds(offUs);

    // Update display every second
    static unsigned long lastDisplayUpdate = 0;
    if (millis() - lastDisplayUpdate > 1000) {
      updateDisplay();
      lastDisplayUpdate = millis();
    }
  }
}
```

### ESP32 variant (WiFi control)

An ESP32 build adds WiFi/Bluetooth capability. You can create a web interface to control frequency, duty cycle, and presets from any phone/tablet browser on your network. The ESP32's `ledcSetup()` and `ledcWrite()` functions provide hardware PWM with precise frequency control up to 40 MHz and 16-bit duty cycle resolution.

Key ESP32 advantages over Arduino Nano:
- Hardware PWM: more precise frequency generation
- WiFi: control from phone browser (no app needed)
- Bluetooth: pair with phone
- More flash/RAM: store more presets and logging data
- Dual core: run control loop on one core, web server on the other

---

## Summary: Which tier to build

| | Tier 1 | Tier 2A (Phone+Amp) | Tier 2B (Arduino) | Tier 3 |
|---|---|---|---|---|
| **Cost** | $30-80 | $60-120 | $55-130 | $200-600 |
| **Gauss output** | 10-15 | 15-25 | 15-50 | 50-300 |
| **Frequency control** | Module buttons | Phone app (0.01Hz precision) | Code (any frequency) | Code + presets + display |
| **Build difficulty** | Easy | Easy-moderate | Moderate | Moderate-hard |
| **Programming needed** | None | None (use app) | Arduino code | Arduino code |
| **Safety features** | Minimal | Volume limit | Code-based timer | Temp monitoring, auto-shutoff |
| **Comparable to** | $50-100 commercial | $200-500 commercial | $200-500 commercial | $1,000-5,000 commercial |
| **Best for** | First build, testing | Best value, daily use | Hobbyists, makers | Serious use, multiple protocols |

**Recommendation:** Start with Tier 1 to verify the concept works and you can feel/measure the field. Then move to Tier 2A (phone + class D amp) for daily use -- it offers the best value and most flexibility. Build Tier 3 only if you want high-gauss output or multiple coil configurations.

---

## References and sources

- NASA Technical Paper 2003-212054: ntrs.nasa.gov/api/citations/20030075722/downloads/20030075722.pdf
- Hackster.io PEMF projects by mircemk: hackster.io/mircemk
- Hackaday.io PEMF projects: hackaday.io (search "PEMF")
- DFRobot PEMF builds: community.dfrobot.com (search "PEMF")
- AuroraSky High Power PEMF: aurorasky.net/html/high_powered_pemf.html
- GitHub jakecoffman/pemf: github.com/jakecoffman/pemf
- Instructables PEMF/RIFE dual device: instructables.com/DIY-Multifunctional-Magnetic-Therapy-Device-PEMF-R
- Element PEMF coil analysis: elementpemf.wordpress.com
- All About Circuits PEMF forum: forum.allaboutcircuits.com (search "PEMF")
- Accel Instruments Helmholtz Calculator: accelinstruments.com/Helmholtz-Coil/Helmholtz-coil-calculator.html
- ICNIRP EMF exposure guidelines: icnirp.org
- PEMF frequency protocols: pemfsupply.com/pages/frequency, pemfadvisor.com/pemf-therapy/frequency-chart
