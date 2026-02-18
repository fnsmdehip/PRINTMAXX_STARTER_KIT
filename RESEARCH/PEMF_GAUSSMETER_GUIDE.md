# PEMF Gaussmeter Guide: How to Actually Measure Pulsed Fields

## Why Your Cheap DC Meter Reads 3 Gauss on a 300+ Gauss Machine

DC gaussmeters sample slowly (a few times per second) and average. PEMF pulses exist for microseconds then drop to zero. The meter catches ~1% of the actual peak. It's not broken -- it's the wrong tool.

Curatronic (PEMF manufacturer) documents this: when a DC meter is placed in a strong pulsing field, the electronics get overloaded and correct measurements are "simply impossible."

**What you need:** AC measurement with sufficient bandwidth, peak hold with millisecond response, or a Hall sensor + oscilloscope.

---

## Recommended Gaussmeters (Ranked by Value)

### Best Budget: Hantek 6022BE + SS49E Hall Sensor (~$75)

This is what DIY PEMF builders actually use. You see the real waveform.

| Component | Price | Source |
|-----------|-------|--------|
| Hantek 6022BE USB oscilloscope (20MHz, 2ch) | ~$65 | Amazon |
| SS49E linear Hall sensors (10-pack) | ~$7 | Amazon |
| Breadboard + wires | ~$5 | Amazon |
| **TOTAL** | **~$77** | |

**Setup:** Power sensor with 5V USB. Connect output to scope Ch1. Sensor outputs 2.5V at zero field. Convert: Gauss = (Vout - 2.5) / 0.0014

**SS49E specs:** Linear range +/-1000 gauss. Sensitivity 1.4 mV/G. Responds in microseconds -- captures ANY PEMF pulse.

**Why this is best:** You see the actual pulse shape, true peak, duration, ringing. No meter limitation. Works at any frequency. The scope is useful for other electronics work too.

### Best Handheld Under $50: HT201 with Peak Hold (~$45)

| Spec | Value |
|------|-------|
| Price | ~$45 (Apex Magnets) / $50-80 (Amazon) |
| AC/DC | Both |
| AC bandwidth | 10-200 Hz |
| Range | 0-20,000 gauss |
| Peak hold | Yes |
| Resolution | 0.01 mT low range |

**Limitation:** 200 Hz AC bandwidth means it can't capture the full peak of very fast pulses. But the peak hold function gives you a much better reading than your current DC meter. Good for relative comparisons.

### Best Used Professional: Lake Shore 410 (~$150-300 eBay)

| Spec | Value |
|------|-------|
| AC/DC | Both (DC, AC peak, AC RMS modes) |
| Bandwidth | DC to 10 kHz |
| Range | 0.1 G to 20,000 G |
| Peak hold | Yes |
| Resolution | 0.1 G lowest range |
| Accuracy | +/-0.2% DC, +/-1% AC |

Set eBay alerts for "Lakeshore 410 gaussmeter." Check that probe is included.

### Best Used Professional (Alt): F.W. Bell 5180 (~$300-800 eBay)

| Spec | Value |
|------|-------|
| AC/DC | Both |
| Bandwidth | DC to 30 kHz (excellent) |
| Range | 0-30,000 G |
| Resolution | 0.1 G low range |

30 kHz bandwidth captures harmonic content of fast pulses. Best value professional meter if you find one under $400.

### Purpose-Built for PEMF: AlphaLab MagWave (~$540 + scope)

Literally designed for measuring PEMF output. Range up to 60,000 gauss. Captures pulses down to 1 microsecond. Requires oscilloscope. Total ~$605 with Hantek.

---

## Meters That DO NOT Work for PEMF (Avoid)

| Model | Price | Problem |
|-------|-------|---------|
| WT10A Tesla Meter | ~$35 | DC only. Same 3 gauss problem you already have |
| TD8620 | ~$60 | DC primarily. "Suitable for DC constant magnetic field" |
| GM3120 EMF Meter | ~$25 | Wrong range entirely -- measures microTesla (milligauss), not gauss |
| Trifield TF2 | ~$186 | Max 100 milligauss. PEMF is hundreds/thousands of gauss |
| Any Alibaba meter under $30 without AC spec | varies | DC only guaranteed |

---

## Summary Table

| Meter | Price | Works for PEMF? | Best For |
|-------|-------|----------------|----------|
| Your Alibaba DC meter | ~$20 | NO | Permanent magnets only |
| WT10A | ~$35 | NO | Permanent magnets only |
| **HT201 Peak Hold** | **$45-80** | **Partial** | Quick relative readings |
| **SS49E + Hantek scope** | **~$75** | **YES** | True waveform, DIY builders |
| **Lake Shore 410 (used)** | **$150-300** | **YES** | Professional handheld |
| **F.W. Bell 5180 (used)** | **$300-800** | **YES** | Professional bench |
| AlphaLab GM2 | $462-902 | YES | Lab grade |
| **AlphaLab MagWave + scope** | **~$605** | **YES** | Built specifically for PEMF |

---

## For Assemblers: Gaussmeter Requirement

Any assembler building your PEMF mat MUST have one of the following:

1. HT201 with peak hold (minimum acceptable -- $45)
2. Hall sensor + oscilloscope setup (preferred -- $75)
3. Any professional AC-capable gaussmeter (Lake Shore, F.W. Bell, AlphaLab)

**If they only have a DC meter (WT10A, cheap Alibaba), they CANNOT verify your mat works properly.** Insist on AC/peak measurement capability.

The QC guide (PEMF_ASSEMBLY_QC_GUIDE.md) requires gauss measurement of each coil at 45-55 gauss. This can only be done with an AC-capable meter or oscilloscope setup.

---

## Quick Buy Links

- HT201: Search Amazon "HT201 gaussmeter peak hold" or Apex Magnets
- Hantek 6022BE: Amazon "Hantek 6022BE USB oscilloscope"
- SS49E sensors: Amazon "SS49E hall effect sensor" (get 10-pack)
- Lake Shore 410: eBay alert "Lakeshore 410 gaussmeter"
- F.W. Bell 5180: eBay alert "FW Bell 5180"
- AlphaLab MagWave: alphalabinc.com/products/magwave/
