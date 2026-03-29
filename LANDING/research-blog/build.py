#!/usr/bin/env python3
"""Build script for fnsmdehip research blog."""
import os

BASE = '/Users/macbookpro/Documents/research-blog'
os.makedirs(BASE, exist_ok=True)

NAV = """<nav><div class="nav-inner">
<a href="index.html" class="site-name">fnsmdehip</a>
<a href="index.html">Home</a>
<a href="uaf.html">UAF</a>
<a href="pemf.html">PEMF</a>
<a href="wifi-sensing.html">WiFi Sensing</a>
<a href="projects.html">Projects</a>
<a href="health.html">Health</a>
</div></nav>"""

FOOTER = """<footer>fnsmdehip &middot; <a href="https://github.com/fnsmdehip">github.com/fnsmdehip</a> &middot; 2026</footer>"""

def page(title, body, active=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
{NAV}
{body}
{FOOTER}
</body>
</html>"""

CSS = r""":root{--bg:#0d1117;--bg-secondary:#161b22;--text:#c9d1d9;--text-muted:#8b949e;--text-bright:#e6edf3;--accent:#58a6ff;--border:#30363d;--code-bg:#161b22;--serif:Georgia,'Times New Roman',serif;--mono:'JetBrains Mono','Fira Code','SF Mono',Consolas,monospace;--sans:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;--content-width:720px;--toc-width:220px}
*,*::before,*::after{box-sizing:border-box}
html{font-size:17px;scroll-behavior:smooth}
body{margin:0;padding:0;background:var(--bg);color:var(--text);font-family:var(--serif);line-height:1.7;-webkit-font-smoothing:antialiased}
nav{position:sticky;top:0;z-index:100;background:var(--bg-secondary);border-bottom:1px solid var(--border);padding:.6rem 1.5rem;font-family:var(--sans);font-size:.82rem;letter-spacing:.02em}
nav .nav-inner{max-width:960px;margin:0 auto;display:flex;align-items:center;gap:1.5rem;flex-wrap:wrap}
nav a{color:var(--text-muted);text-decoration:none;transition:color .15s}
nav a:hover,nav a.active{color:var(--accent)}
nav .site-name{color:var(--text-bright);font-weight:600;margin-right:auto;font-size:.9rem}
.page-wrapper{display:flex;max-width:calc(var(--content-width) + var(--toc-width) + 80px);margin:0 auto;padding:2rem 1.5rem 4rem;gap:3rem}
.content{flex:1;max-width:var(--content-width);min-width:0}
.toc{width:var(--toc-width);flex-shrink:0;position:sticky;top:4rem;max-height:calc(100vh - 5rem);overflow-y:auto;font-family:var(--sans);font-size:.78rem;line-height:1.5;padding-right:.5rem}
.toc-title{color:var(--text-muted);text-transform:uppercase;letter-spacing:.08em;font-size:.7rem;font-weight:600;margin-bottom:.75rem}
.toc ol{list-style:none;padding:0;margin:0}
.toc li{margin-bottom:.4rem}
.toc a{color:var(--text-muted);text-decoration:none;transition:color .15s}
.toc a:hover{color:var(--accent)}
.toc ol ol{padding-left:1rem;margin-top:.3rem}
h1{font-family:var(--sans);font-size:2rem;font-weight:700;color:var(--text-bright);line-height:1.2;margin:0 0 .5rem;letter-spacing:-.02em}
h2{font-family:var(--sans);font-size:1.35rem;font-weight:600;color:var(--text-bright);margin:2.5rem 0 .75rem;padding-bottom:.3rem;border-bottom:1px solid var(--border)}
h3{font-family:var(--sans);font-size:1.1rem;font-weight:600;color:var(--text-bright);margin:2rem 0 .5rem}
h4{font-family:var(--sans);font-size:.95rem;font-weight:600;color:var(--text);margin:1.5rem 0 .4rem}
p{margin:0 0 1.2rem}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
strong{color:var(--text-bright);font-weight:600}
.meta{font-family:var(--sans);font-size:.82rem;color:var(--text-muted);margin-bottom:2rem}
.tagline{font-size:1rem;color:var(--text-muted);font-style:italic;margin-bottom:2rem}
blockquote,.note{border-left:3px solid var(--accent);background:var(--bg-secondary);margin:1.5rem 0;padding:.8rem 1.2rem;font-size:.92rem}
blockquote p:last-child,.note p:last-child{margin-bottom:0}
code{font-family:var(--mono);font-size:.85em;background:var(--code-bg);padding:.15em .4em;border-radius:3px;color:var(--text-bright)}
pre{background:var(--code-bg);border:1px solid var(--border);border-radius:4px;padding:1rem 1.2rem;overflow-x:auto;font-size:.85rem;line-height:1.5;margin:1.5rem 0}
pre code{background:none;padding:0;font-size:inherit}
ul,ol{padding-left:1.5rem;margin:0 0 1.2rem}
li{margin-bottom:.4rem}
li>ul,li>ol{margin-top:.3rem;margin-bottom:0}
.tier-label{font-family:var(--sans);font-weight:600;font-size:.85rem;display:inline-block;padding:.1em .5em;border-radius:3px;margin-right:.5em}
.tier-1{background:#238636;color:#fff}
.tier-2{background:#1f6feb;color:#fff}
.tier-3{background:#9e6a03;color:#fff}
.tier-4{background:#6e4006;color:#fff}
table{width:100%;border-collapse:collapse;margin:1.5rem 0;font-size:.9rem}
th,td{text-align:left;padding:.5rem .75rem;border-bottom:1px solid var(--border)}
th{font-family:var(--sans);font-weight:600;color:var(--text-bright);font-size:.82rem;text-transform:uppercase;letter-spacing:.04em;border-bottom:2px solid var(--border)}
.footnote-ref{font-family:var(--sans);font-size:.75em;vertical-align:super;color:var(--accent);cursor:pointer;text-decoration:none}
.footnotes{margin-top:3rem;padding-top:1.5rem;border-top:1px solid var(--border);font-size:.88rem;color:var(--text-muted)}
.footnotes ol{padding-left:1.2rem}
.footnotes li{margin-bottom:.6rem}
.project-list{list-style:none;padding:0}
.project-list li{padding:.75rem 0;border-bottom:1px solid var(--border)}
.project-list li:last-child{border-bottom:none}
.project-name{font-family:var(--sans);font-weight:600;color:var(--text-bright);font-size:1rem}
.project-desc{color:var(--text-muted);font-size:.9rem;margin-top:.15rem}
.article-list{list-style:none;padding:0}
.article-list li{padding:1rem 0;border-bottom:1px solid var(--border)}
.article-list li:last-child{border-bottom:none}
.article-list a{font-family:var(--sans);font-weight:600;font-size:1.05rem;color:var(--text-bright);text-decoration:none}
.article-list a:hover{color:var(--accent)}
.article-list .date{font-family:var(--sans);font-size:.78rem;color:var(--text-muted);display:block;margin-bottom:.15rem}
.article-list .desc{font-size:.9rem;color:var(--text-muted);margin-top:.2rem}
.killswitch{background:#1a1208;border:1px solid #6e4006;border-left:3px solid #d29922;border-radius:3px;padding:.7rem 1rem;margin:1rem 0;font-size:.88rem;font-family:var(--sans)}
.killswitch strong{color:#d29922}
footer{border-top:1px solid var(--border);padding:1.5rem;text-align:center;font-family:var(--sans);font-size:.78rem;color:var(--text-muted)}
footer a{color:var(--text-muted)}
footer a:hover{color:var(--accent)}
@media(max-width:900px){.page-wrapper{flex-direction:column;padding:1.5rem 1rem 3rem}.toc{position:static;width:100%;max-height:none;border:1px solid var(--border);border-radius:4px;padding:1rem;margin-bottom:1.5rem;background:var(--bg-secondary)}.content{max-width:100%}h1{font-size:1.6rem}h2{font-size:1.2rem}nav .nav-inner{gap:.8rem}}
@media(max-width:600px){html{font-size:16px}nav{padding:.5rem 1rem}.page-wrapper{padding:1rem .75rem 2rem}pre{font-size:.8rem;padding:.75rem}}
.hero{margin-bottom:2.5rem}
.hero h1{font-size:1.6rem;margin-bottom:.3rem}
.hero .subtitle{font-family:var(--sans);font-size:.85rem;color:var(--text-muted);margin-bottom:1.5rem}
hr{border:none;border-top:1px solid var(--border);margin:2.5rem 0}
"""

INDEX_BODY = """<div class="page-wrapper">
<div class="content">
<div class="hero">
<h1>fnsmdehip &mdash; research notes</h1>
<div class="subtitle">cross-domain theory, health experiments, signal intelligence, autonomous systems</div>
</div>
<p>This site collects research notes, technical writeups, and experiment logs from an independent researcher working across physics, biology, software architecture, and signal processing. The throughline: finding structural patterns that repeat across domains, then building systems that exploit them.</p>
<p>Everything here is written to be falsifiable. Claims come with kill switches. Predictions come with breakpoints. If the data kills an idea, the idea stays dead.</p>
<h2 id="articles">Articles</h2>
<ul class="article-list">
<li>
<span class="date">2026-03-28</span>
<a href="uaf.html">The Unified Aetheric Framework</a>
<div class="desc">A cross-domain mathematical framework generating testable predictions across biology, addiction, cancer, social dynamics, and consciousness. Plain english version.</div>
</li>
<li>
<span class="date">2026-03-28</span>
<a href="pemf.html">PEMF Therapy: Vindication of a Marginalized Modality</a>
<div class="desc">Pulsed electromagnetic field therapy has strong preclinical data but remains sidelined by institutional inertia, regulatory capture, and the Flexner Report's long shadow.</div>
</li>
<li>
<span class="date">2026-03-28</span>
<a href="wifi-sensing.html">ESPectre: Privacy-Preserving Motion Detection via Wi-Fi CSI</a>
<div class="desc">Using channel state information from commodity ESP32 hardware for room-level presence detection. No cameras. No microphones. 10 euro per sensor.</div>
</li>
<li>
<span class="date">2026-03-28</span>
<a href="health.html">Health Experiments &amp; Longevity Notes</a>
<div class="desc">Ongoing experiments in biohacking, longevity interventions, and a framework for ranking what actually moves biological age markers.</div>
</li>
<li>
<span class="date">2026-03-28</span>
<a href="projects.html">Project Index</a>
<div class="desc">A catalog of active and shipped projects across autonomous systems, signal intelligence, music production, iOS apps, and open-source tools.</div>
</li>
</ul>
</div>
</div>"""

UAF_BODY = """<div class="page-wrapper">
<aside class="toc">
<div class="toc-title">Contents</div>
<ol>
<li><a href="#one-idea">The one idea</a></li>
<li><a href="#tipping-point">Repair force tipping point</a></li>
<li><a href="#cancer-addiction">Cancer and addiction</a></li>
<li><a href="#fascia">Fascia as body-wide telegraph</a></li>
<li><a href="#breathing">Breathing and tumor chemistry</a></li>
<li><a href="#bryan-johnson">Why Bryan Johnson's pills hit ceilings</a></li>
<li><a href="#presentiment">Pre-stimulus response</a></li>
<li><a href="#flock-math">Flock math and whistleblowers</a></li>
<li><a href="#kill-switches">Kill switches</a></li>
<li><a href="#status">What this is and isn't</a></li>
</ol>
</aside>
<div class="content">
<h1>The Unified Aetheric Framework</h1>
<div class="meta"><span class="date">2026-03-28</span> &middot; Plain english version</div>
<div class="note">
<p>This is the accessible version of the UAF. The full manuscript with mathematical formalism (v51, 248KB, 4400+ paragraphs, 10 appendices) is available at <a href="https://github.com/fnsmdehip/uaf">github.com/fnsmdehip/uaf</a>.</p>
</div>
<p>The name sounds weird. The math doesn't care what you call it. Read the predictions before judging the label.</p>
<h2 id="not-crackpot">Why this isn't another theory-of-everything crackpot document</h2>
<p>Theories that explain everything usually explain nothing. UAF handles this with kill switches: every single prediction specifies the exact experimental result that would destroy it. The framework is designed to be killed by data. It has survived so far because the data keeps landing where it predicted, including null results it called before the trials reported (PEARL rapamycin, NAD+ supplementation).</p>
<h2 id="one-idea">The one idea</h2>
<p>Every living thing is in a constant tug of war. One side pulls toward health and order. The other pulls toward breakdown. When the breakdown side wins long enough, you get sick, addicted, burned out, or dead.</p>
<p>That tug of war is the same tug of war at every scale. A cancer cell losing control of its metabolism runs the same pattern as an addict losing control of their dopamine. A corrupt organization eating itself alive runs the same pattern as a body that stopped repairing its DNA. Not as a metaphor. As the same math.</p>
<h2 id="tipping-point">Your body's repair force has a tipping point</h2>
<p>You have a repair force. The framework calls it sigma. Sleep restores it. Coherent heartbeats strengthen it. Chronic stress, bad food, toxic environments drain it. As long as sigma is stronger than the damage hitting you, you stay healthy.</p>
<p>But there's a cliff. Once sigma drops below a critical threshold, the slide becomes self-reinforcing. Being sick makes you sicker. Being addicted makes quitting harder. Being burned out makes recovery feel impossible. You've crossed into a trap that actively holds you there.</p>
<p>Every disease, every addiction, every systemic collapse is this same cliff at a different scale.</p>
<h2 id="cancer-addiction">Cancer and addiction are the same trap</h2>
<p>In addiction: your brain's reward thermostat breaks. You need more drug for less effect. Eventually you're not chasing pleasure; you're running from withdrawal. Your brain fights anything trying to fix the thermostat.</p>
<p>In cancer: a cell's metabolism thermostat breaks. It switches to a wasteful sugar-burning mode. It needs more fuel for less function. Eventually it's not growing because it's healthy; it can't stop. Your immune system tries to kill it and the tumor fights back.</p>
<p>Same pattern. Same trap. Different size. The framework predicts that interventions fixing one should show measurable effects on the other, and early evidence (low-dose naltrexone showing anti-tumor effects) lines up.</p>
<h2 id="fascia">Your fascia is a body-wide telegraph</h2>
<p>Under your skin there's a web of connective tissue called fascia. It carries tiny electrical signals through its collagen fibers: actual piezoelectric currents, measurable with instruments.</p>
<p>Where that web gets knotted up (old injuries, chronic tension, scar tissue), the telegraph goes dark. Research from 2025 shows that stiff connective tissue activates the exact molecular switches (YAP/TAZ, integrin-FAK) that push cells toward cancer.</p>
<div class="killswitch">
<strong>Kill switch:</strong> Map someone's fascial damage and you can predict WHERE in their body cancer is most likely to start. Not just IF, but WHERE. Predicted accuracy: AUC of 0.65+ on a prospective cohort (controlling for smoking, BMI, genetics). Testable with existing imaging (shear-wave elastography). No new technology needed.
</div>
<h2 id="breathing">Breathing exercises can physically change tumor chemistry</h2>
<p>If you train your heartbeat into a coherent rhythm (HRV biofeedback), that rhythm travels through the fascial telegraph to distant tissues. At those tissues, the connective web loosens, the cancer-promoting molecular switches deactivate, and the local chemistry shifts: more oxygen, less acid, less sugar-burning.</p>
<p>This isn't meditation-heals-cancer woo. It's a specific physical chain: heart rhythm to fascial electrical signal to tissue stiffness change to molecular switch deactivation to tumor microenvironment shift. Each link is independently measurable.</p>
<div class="killswitch">
<strong>Kill switch:</strong> The framework predicts this only works for tumors near the chest (where the heart's signal is strongest): breast and lung tumors more than, say, ankle tumors. That anatomical specificity is what separates this from placebo. If breathing exercises change tumors equally everywhere, the fascial propagation model is wrong.
</div>
<h2 id="bryan-johnson">Why Bryan Johnson's pills hit ceilings</h2>
<p>Bryan Johnson spends $2M/year on longevity supplements. His manifesto says: repair has to beat damage or you die. He's right about the principle.</p>
<p>But his protocol is mostly pills that block individual damage pathways one at a time: rapamycin blocks one, NAD+ targets another. The framework predicts this hits a ceiling because blocking one pathway doesn't restore sigma. The damage just reroutes through other channels. A $6M rapamycin trial (PEARL, 114 people, 48 weeks) came back null in healthy humans. NAD+ supplements showed null results across multiple trials on every major endpoint. The framework predicted both nulls before the data came in.</p>
<p>What actually moves the needle: restoring sigma directly. The framework ranks interventions in tiers:</p>
<div class="tier">
<span class="tier-label tier-1">Tier 1</span> <strong>Restore sigma itself:</strong> HRV coherence training, optimized sleep architecture
</div>
<div class="tier">
<span class="tier-label tier-2">Tier 2</span> <strong>Clear accumulated damage:</strong> senolytics (clearing zombie cells), gut microbiome repair
</div>
<div class="tier">
<span class="tier-label tier-3">Tier 3</span> <strong>Slow new damage:</strong> caloric restriction, fasting
</div>
<div class="tier">
<span class="tier-label tier-4">Tier 4</span> <strong>Block individual pathways:</strong> rapamycin, NAD+, metformin &mdash; necessary but insufficient alone
</div>
<div class="killswitch">
<strong>Kill switch:</strong> Bryan Johnson's protocol is heavy on Tier 3-4. The framework predicts he won't reverse biological age until he prioritizes Tier 1-2. Specifically: HRV coherence quality (not just practice time) should predict GrimAge reversal better than any pharmacological variable in his dataset.
</div>
<h2 id="presentiment">Your body might detect threats before they arrive</h2>
<p>This is the part that sounds crazy. Keep reading anyway.</p>
<p>26 studies across 7 independent labs found that people's heart rate and skin conductance shift 1-10 seconds BEFORE a random emotional image appears on screen. Effect size 0.21, p-value less than one in a trillion. Higher-quality studies showed LARGER effects. This isn't fringe; it's published in peer-reviewed journals and the statistical signal is enormous.</p>
<p>The framework models this as: when a big disruption is coming, the tension it will create propagates backward in time like a wave. Your autonomic nervous system picks it up as a faint signal. But only if you're calm enough internally (high sigma) and the electromagnetic environment is quiet (low geomagnetic noise).</p>
<div class="killswitch">
<strong>Kill switch:</strong> Presentiment effect size should correlate inversely with the Kp index (Earth's magnetic activity). Testable by re-analyzing existing datasets with geomagnetic timestamps. If it doesn't correlate across 500+ sessions, this module gets cut from the framework entirely.
</div>
<h2 id="flock-math">Honest people in corrupt systems get attacked by flock math</h2>
<p>When one honest person enters a corrupt organization, opposition doesn't scale with org size the way you'd expect. In a flock of birds, you only need the square root of the flock to change direction to redirect everyone. Same math applies to social pressure against whistleblowers: in a 100-person company, roughly 10 people actively oppose the whistleblower. In a 10,000-person company, roughly 100, not 10,000. Square root scaling, not linear.</p>
<p>This means the resistance isn't a coordinated conspiracy. It's an emergent swarm behavior: the same dynamics that let a school of fish move as one.</p>
<div class="killswitch">
<strong>Kill switch:</strong> The framework predicts that when an organization flips from corrupt to healthy culture, the attacks drop suddenly (phase transition), not gradually. Testable by tracking whistleblower retaliation rates across institutional reforms.
</div>
<h2 id="kill-switches">Every prediction has a kill switch</h2>
<p>Each claim above comes with a specific condition that would prove it wrong. If fascial stiffness doesn't predict cancer location, that section is dead. If breathing exercises change tumors equally everywhere (not just near the chest), the fascial propagation model is wrong. If the rapamycin null turns out to be a dosing issue rather than a pathway issue, the hierarchy needs revision.</p>
<p>No sacred cows. The theory is built to be killed by data. If it survives, it earned it.</p>
<h2 id="status">What this is and isn't</h2>
<p><strong>Is:</strong> A formal mathematical framework that generates testable predictions across biology, medicine, social dynamics, and consciousness from one equation. Every prediction has a specific kill condition.</p>
<p><strong>Isn't:</strong> A religion. A wellness brand. A completed science. It's a hypothesis with engineering drawings and self-destruct buttons.</p>
<p><strong>Status:</strong> v51 manuscript (248KB, 4400+ paragraphs), 10 appendices, 23+ discriminating predictions with breakpoints. Open source. Built by one person over 7 years of thinking, formalized with autonomous AI research agents running daily.</p>
<p>The framework is public. The kill switches are public. Knock it down or build on it.</p>
</div>
</div>"""

PEMF_BODY = """<div class="page-wrapper">
<aside class="toc">
<div class="toc-title">Contents</div>
<ol>
<li><a href="#mechanisms">How PEMF works</a></li>
<li><a href="#evidence">Clinical evidence</a></li>
<li><a href="#critical-care">Beyond joints: critical care</a></li>
<li><a href="#nutrition">Synergy with nutrition</a></li>
<li><a href="#flexner">The Flexner Report</a></li>
<li><a href="#groupthink">Institutional groupthink</a></li>
<li><a href="#barriers">Financial and regulatory barriers</a></li>
<li><a href="#forward">Path forward</a></li>
</ol>
</aside>
<div class="content">
<h1>PEMF Therapy: Vindication of a Marginalized Modality</h1>
<div class="meta"><span class="date">2026-03-28</span></div>
<p>Pulsed Electromagnetic Field (PEMF) therapy has been marginalized for decades despite compelling preclinical and early clinical data. It shows clear benefits in bone healing, osteoarthritis, pain relief, and even sepsis, yet remains sidelined in mainstream medicine due to lack of standardization, limited reimbursement, and entrenched paradigms.</p>
<h2 id="mechanisms">How PEMF works</h2>
<p>PEMF induces electrical currents in tissues, enhancing cell membrane function, mitochondrial ATP production, and nitric oxide signaling to reduce inflammation and promote regeneration. The mechanism is straightforward biophysics: time-varying magnetic fields induce electric fields in conductive tissue. The induced currents are small (microampere range) but sufficient to influence cellular signaling cascades.</p>
<p>Three primary pathways:</p>
<ul>
<li><strong>Membrane potential modulation:</strong> PEMF alters transmembrane voltage, affecting ion channel gating and calcium signaling</li>
<li><strong>Mitochondrial activation:</strong> Enhanced electron transport chain activity increases ATP production</li>
<li><strong>NO signaling:</strong> Nitric oxide release improves local blood flow and reduces inflammatory mediators</li>
</ul>
<h2 id="evidence">Clinical evidence</h2>
<p>Clinical studies demonstrate significant pain reduction and functional gains in knee osteoarthritis across 17 RCTs covering 1,197 patients. Systematic reviews confirm positive outcomes across anatomical districts. The evidence base is substantial but fragmented: no two trials use the same protocol, making meta-analysis difficult and giving skeptics easy ammunition.</p>
<h2 id="critical-care">Beyond joints: critical care potential</h2>
<p>The most interesting PEMF data comes from applications nobody expected:</p>
<p><strong>Sepsis:</strong> In LPS-induced septic shock mouse models, PEMF reduced pro-inflammatory cytokines, nitric oxide levels, and organ damage, markedly improving survival rates. The effect sizes are large enough that the failure to run human trials looks more like institutional inertia than scientific caution.</p>
<p><strong>Neurocritical care:</strong> Repetitive transcranial magnetic stimulation (rTMS), a focused PEMF application, yielded meaningful Coma Recovery Scale improvements in vegetative and minimally conscious patients over multi-week protocols. This is a patient population with essentially zero approved interventions.</p>
<p><strong>Neurodegeneration:</strong> Pilot studies in Alzheimer's and Parkinson's disease report slowed cognitive decline and motor improvements, though large RCTs remain pending.</p>
<h2 id="nutrition">Synergy with nutritional support</h2>
<p>PEMF's bioenergizing signals elevate mitochondrial metabolism and ion-channel dynamics, implying that cells might better utilize amino acids, electrolytes, and mitochondrial cofactors when co-administered. Integrative use of PEMF with targeted parenteral nutrition could jump-start failing organs, mirroring early mobilization and physiotherapy practices in critical care. This hypothesis remains untested in formal ICU nutrition protocols.</p>
<h2 id="flexner">The Flexner Report: standardization as weapon</h2>
<p>The 1910 Flexner Report, commissioned by the Carnegie Foundation and funded by the Rockefeller philanthropies, closed or consolidated nearly half of North American medical schools. This included nearly all that taught electrotherapy, homeopathy, naturopathy, and related modalities.</p>
<p>The irony: many device-based therapies later demonstrated efficacy. FDA clearance for noninvasive bone growth stimulators (PEMF devices) solidified bone healing benefits. Medicare covers adjunctive electrical stimulation for wound healing. Systematic reviews affirm PEMF's anti-inflammatory effects on mesenchymal stem cells and macrophages.</p>
<p>The Flexner Report was right that medical education needed rigor. It was wrong in conflating "not yet proven" with "disproven," and the institutional apparatus it created has perpetuated that conflation for over a century.</p>
<h2 id="groupthink">Institutional groupthink</h2>
<p>Modern healthcare teams exhibit conformity pressures that stifle dissent and delay adoption of non-pharmaceutical interventions. Scoping reviews identify pervasive groupthink in hospital decision-making, with only four empirical studies examining these biases in clinical settings. Hierarchical structures, liability concerns, and lack of PEMF education reinforce a "stay in textbook" mindset, rendering off-protocol innovation ethically and professionally risky.</p>
<h2 id="barriers">Financial and regulatory barriers</h2>
<ul>
<li><strong>Reimbursement gap:</strong> Outside orthopedics and wound care, PEMF lacks Medicare or major insurer coverage, offering no clear billing path for hospitals</li>
<li><strong>Regulatory hurdles:</strong> Expanding PEMF indications demands costly FDA trials; device patents are narrow, limiting ROI and deterring large-scale studies</li>
<li><strong>Research funding void:</strong> The absence of a patentable drug-style revenue model means few industry-sponsored RCTs, trapping PEMF in small pilots and preclinical research</li>
</ul>
<p>The core problem is economic, not scientific. Nobody can patent electromagnetic fields. Without patent protection, nobody funds the $50M Phase III trials needed to change clinical guidelines.</p>
<h2 id="forward">Path forward</h2>
<ol>
<li><strong>Standardize protocols:</strong> Develop consensus guidelines on PEMF frequency, intensity, waveform, and dosing</li>
<li><strong>Pilot integrative trials:</strong> Test PEMF with tailored nutritional support in septic shock and organ-failure protocols</li>
<li><strong>Educate and advocate:</strong> Integrate PEMF science into medical curricula, secure CPT codes for reimbursement</li>
<li><strong>Combat groupthink:</strong> Form multidisciplinary teams including engineers, integrative physicians, and critical-care specialists</li>
</ol>
</div>
</div>"""

WIFI_BODY = """<div class="page-wrapper">
<aside class="toc">
<div class="toc-title">Contents</div>
<ol>
<li><a href="#overview">Overview</a></li>
<li><a href="#how-it-works">How CSI sensing works</a></li>
<li><a href="#pipeline">Processing pipeline</a></li>
<li><a href="#mvs">MVS algorithm</a></li>
<li><a href="#ml">ML neural network detector</a></li>
<li><a href="#nbvi">Automatic subcarrier selection</a></li>
<li><a href="#filters">Signal processing filters</a></li>
<li><a href="#privacy">Privacy architecture</a></li>
<li><a href="#applications">Applications</a></li>
</ol>
</aside>
<div class="content">
<h1>ESPectre: Privacy-Preserving Motion Detection via Wi-Fi CSI</h1>
<div class="meta"><span class="date">2026-03-28</span> &middot; Technical writeup</div>
<h2 id="overview">Overview</h2>
<p>ESPectre is a motion detection system that uses Wi-Fi Channel State Information (CSI) from commodity ESP32 hardware. No cameras, no microphones, no wearables. A single ESP32 board (roughly 10 euros) placed 3-8 meters from any standard 2.4GHz router can detect human presence and movement through walls.</p>
<p>The system integrates natively with Home Assistant via ESPHome, making it accessible to non-programmers through YAML configuration. Two detection algorithms are available: MVS (Moving Variance Segmentation) for general use, and an experimental ML detector using a compact neural network.</p>
<h2 id="how-it-works">How CSI sensing works</h2>
<p>Channel State Information represents the physical characteristics of the wireless channel between transmitter and receiver. Unlike simple RSSI (a single signal strength number), CSI provides per-subcarrier amplitude and phase data across 64 OFDM subcarriers in HT20 mode. This captures multipath propagation, Doppler shifts from movement, and temporal variations in the channel response.</p>
<p>When a person moves in a room, they alter the multipath reflections, changing signal amplitude and phase patterns. These changes are detectable even through walls. The key insight: you don't need to decode the WiFi data. You just need to measure how the channel itself changes over time.</p>
<h2 id="pipeline">Processing pipeline</h2>
<p>The system runs a calibration sequence at boot (roughly 10.5 seconds), then processes packets in real-time:</p>
<ol>
<li><strong>Gain Lock</strong> (3 seconds, 300 packets): Locks AGC and FFT gain values using median of collected samples to eliminate hardware-induced amplitude variations</li>
<li><strong>Band Calibration</strong> (7.5 seconds, 750 packets): NBVI algorithm selects 12 optimal subcarriers from the 64 available</li>
<li><strong>Per-packet processing:</strong> Raw I/Q values to amplitude extraction to spatial turbulence (coefficient of variation across selected subcarriers) to optional filtering to moving variance to threshold comparison to IDLE/MOTION state</li>
</ol>
<p>The spatial turbulence metric uses the Coefficient of Variation (CV = standard deviation / mean), which is mathematically gain-invariant. If the receiver AGC scales all amplitudes by factor k, the CV remains unchanged.</p>
<h2 id="mvs">MVS: Moving Variance Segmentation</h2>
<p>The core detection algorithm. Human movement causes multipath interference that manifests as fluctuating CSI amplitudes (high turbulence variance), while idle states produce stable amplitudes (low turbulence variance).</p>
<p>The algorithm computes a two-pass moving variance over a sliding window (default 75 packets, 0.75 seconds at 100 pps), then compares against an adaptive threshold calculated from baseline noise. The threshold uses the 95th percentile of baseline moving variance multiplied by 1.1, which minimizes false positives while maintaining recall above 98%.</p>
<h2 id="ml">ML: Neural network detector</h2>
<p>The experimental ML detector uses a compact Multi-Layer Perceptron: 12 input features through two hidden layers (16 and 8 neurons, ReLU activation) to a single sigmoid output. Total: 353 parameters, 1.4 KB of weights embedded directly in the firmware.</p>
<p>The 12 input features are statistical measures extracted from the turbulence buffer: mean, standard deviation, max, min, zero-crossing rate, skewness, kurtosis, Shannon entropy, lag-1 autocorrelation, median absolute deviation, linear regression slope, and start-to-end delta.</p>
<p>Architecture was validated through 5-fold stratified cross-validation on 13,711 samples, achieving 98.3% F1 score. ML uses fixed subcarriers (no calibration needed), reducing boot time to roughly 3 seconds.</p>
<h2 id="nbvi">Automatic subcarrier selection (NBVI)</h2>
<p>Not all 64 subcarriers are useful for motion detection. Some have low SNR, some are too noisy at rest, some sit in guard bands or the DC zone.</p>
<p>NBVI (Normalized Baseline Variability Index) selects 12 non-consecutive subcarriers automatically. For each candidate subcarrier, it computes a weighted combination of stability and signal strength:</p>
<pre><code>NBVI = alpha * (sigma/mu^2) + (1-alpha) * (sigma/mu)</code></pre>
<p>Where alpha = 0.5 balances stability and signal strength. Calibration runs in 30-50ms, fast enough for real-time use on embedded hardware.</p>
<h2 id="filters">Signal processing filters</h2>
<h3>Low-pass filter</h3>
<p>A 1st-order Butterworth IIR filter with 11 Hz cutoff. Human movement generates signal variations in the 0.5-10 Hz range; RF noise is typically above 15 Hz. Disabled by default.</p>
<h3>Hampel filter</h3>
<p>Removes statistical outliers using Median Absolute Deviation. If a turbulence value deviates from the local median by more than 4 times the scaled MAD, it's replaced with the median. Disabled by default.</p>
<h2 id="privacy">Privacy architecture</h2>
<p>The system collects anonymous data about the physical characteristics of the Wi-Fi radio channel: subcarrier amplitudes, phases, and statistical variances. No personal identities, no communication contents, no images, no audio. The fundamental advantage over camera-based systems: there is no visual data to leak, no recordings to subpoena, no facial recognition to misuse.</p>
<h2 id="applications">Applications</h2>
<ul>
<li><strong>Home security:</strong> Alert when someone enters while you're away</li>
<li><strong>Elderly care:</strong> Monitor activity to detect falls or prolonged inactivity</li>
<li><strong>Smart automation:</strong> Lights and climate control only when someone is present</li>
<li><strong>Energy savings:</strong> Automatically power down unoccupied rooms</li>
</ul>
<p>Future directions include gesture recognition, human activity recognition, people counting, and 3D indoor localization.</p>
<p>Source code: <a href="https://github.com/francescopace/espectre">github.com/francescopace/espectre</a></p>
</div>
</div>"""

PROJECTS_BODY = """<div class="page-wrapper">
<div class="content">
<h1>Project Index</h1>
<div class="meta"><span class="date">2026-03-28</span> &middot; Active and shipped projects</div>
<p>A catalog of major projects across autonomous systems, signal intelligence, music production, iOS apps, and open-source infrastructure. Most are actively maintained. All are built by one person with AI agent assistance.</p>
<h2 id="autonomous">Autonomous systems</h2>
<ul class="project-list">
<li><div class="project-name">PRINTMAXX</div><div class="project-desc">Autonomous revenue operating system. 33 coordinated agents, 363 scripts, handling content creation, distribution, analytics, and monetization across multiple platforms without human intervention.</div></li>
<li><div class="project-name">sovrun</div><div class="project-desc">Agent OS. 20 modules for building, orchestrating, and deploying autonomous agent systems. Open source. The infrastructure layer underneath PRINTMAXX and other agent-driven projects.</div></li>
</ul>
<h2 id="intelligence">Signal intelligence</h2>
<ul class="project-list">
<li><div class="project-name">SIGCRAFT</div><div class="project-desc">Cross-domain signal intelligence engine. 22+ data sources, real-time signal extraction, pattern matching across financial, social, and alternative datasets. Built for prediction and trading.</div></li>
</ul>
<h2 id="sensing">Sensing and hardware</h2>
<ul class="project-list">
<li><div class="project-name">ESPectre</div><div class="project-desc">Privacy-preserving Wi-Fi motion detection using CSI on ESP32 hardware. Home Assistant integration. MVS and ML detection algorithms. Open source, featured on Hackaday. <a href="wifi-sensing.html">Technical writeup.</a></div></li>
</ul>
<h2 id="research">Research</h2>
<ul class="project-list">
<li><div class="project-name">UAF (Unified Aetheric Framework)</div><div class="project-desc">Cross-domain mathematical framework. v51, 248KB manuscript, 23+ discriminating predictions. <a href="uaf.html">Plain english version.</a></div></li>
</ul>
<h2 id="music">Music production</h2>
<ul class="project-list">
<li><div class="project-name">soundgrep</div><div class="project-desc">Multi-agent music production tool. Agents handle composition, arrangement, mixing, and mastering collaboratively.</div></li>
</ul>
<h2 id="developer-tools">Developer tools</h2>
<ul class="project-list">
<li><div class="project-name">devprint</div><div class="project-desc">Developer provenance system. 174 projects cataloged with full dependency graphs, build histories, and contribution metrics.</div></li>
</ul>
<h2 id="apps">iOS and web applications</h2>
<ul class="project-list">
<li><div class="project-name">NutriSnap</div><div class="project-desc">iOS nutrition tracking via photo recognition. Point camera at food, get macros.</div></li>
<li><div class="project-name">Scripture Streak</div><div class="project-desc">iOS daily Bible reading tracker with streak mechanics and reading plans.</div></li>
<li><div class="project-name">Pocket Alexandria</div><div class="project-desc">iOS personal knowledge library. Save, organize, and search across books, articles, and notes.</div></li>
<li><div class="project-name">ConsentVault</div><div class="project-desc">iOS consent and permissions management. Tracks what you've agreed to and when.</div></li>
<li><div class="project-name">AutoReplyAI</div><div class="project-desc">Web SaaS for automated intelligent email responses. AI-powered reply generation with customizable tone and rules.</div></li>
</ul>
<h2 id="personal">Personal and family</h2>
<ul class="project-list">
<li><div class="project-name">ancestry-research / Before You</div><div class="project-desc">Family history research platform. Genealogical records, DNA analysis integration, and narrative generation from historical data.</div></li>
</ul>
</div>
</div>"""

HEALTH_BODY = """<div class="page-wrapper">
<aside class="toc">
<div class="toc-title">Contents</div>
<ol>
<li><a href="#framework">The framework</a></li>
<li><a href="#tier-system">Intervention tier system</a></li>
<li><a href="#hrv">HRV coherence training</a></li>
<li><a href="#sleep">Sleep architecture</a></li>
<li><a href="#senolytics">Senolytics</a></li>
<li><a href="#cr">Caloric restriction and fasting</a></li>
<li><a href="#pemf-health">PEMF therapy</a></li>
<li><a href="#pharma">Pharmacological interventions</a></li>
<li><a href="#bryan">The Bryan Johnson problem</a></li>
<li><a href="#tracking">What to track</a></li>
</ol>
</aside>
<div class="content">
<h1>Health Experiments &amp; Longevity Notes</h1>
<div class="meta"><span class="date">2026-03-28</span> &middot; Ongoing research notes</div>
<p>These are working notes on health interventions, longevity strategies, and the theoretical framework connecting them. Not medical advice. Not a protocol recommendation. A record of what the research says, what the framework predicts, and what the experiments show.</p>
<h2 id="framework">The framework</h2>
<p>The UAF longevity model reduces aging to a single dynamic: sigma (your body's aggregate repair capacity) versus accumulated damage. As long as sigma exceeds the damage rate, you stay biologically young. When damage overtakes sigma, you enter a self-reinforcing decline: damage impairs repair, which allows more damage, which further impairs repair.</p>
<p>This is not a metaphor. The math produces specific, testable predictions about which interventions should work, which should fail, and in what order they should be applied.</p>
<h2 id="tier-system">Intervention tier system</h2>
<div class="tier"><span class="tier-label tier-1">Tier 1: Restore sigma directly</span></div>
<p>Interventions that increase your body's repair capacity itself. Highest theoretical ceiling. Prioritize first.</p>
<ul>
<li><strong>HRV coherence training:</strong> Directly strengthens autonomic nervous system regulation, which coordinates repair processes across organ systems</li>
<li><strong>Optimized sleep architecture:</strong> Sleep is when sigma regenerates. Not just duration but structure: sufficient deep sleep, REM, and minimal fragmentation</li>
</ul>
<div class="tier"><span class="tier-label tier-2">Tier 2: Clear accumulated damage</span></div>
<p>Removing the damage backlog so sigma can catch up.</p>
<ul>
<li><strong>Senolytics:</strong> Clearing senescent cells that secrete inflammatory signals. Dasatinib + quercetin is the most studied combination</li>
<li><strong>Gut microbiome repair:</strong> Dysbiosis drives systemic inflammation. Targeted probiotics, prebiotics, and elimination of gut barrier disruptors</li>
</ul>
<div class="tier"><span class="tier-label tier-3">Tier 3: Slow new damage</span></div>
<ul>
<li><strong>Caloric restriction:</strong> Robust evidence across species. Mechanism is partly reduced metabolic waste, partly enhanced autophagy</li>
<li><strong>Intermittent fasting:</strong> Triggers autophagy and metabolic flexibility</li>
</ul>
<div class="tier"><span class="tier-label tier-4">Tier 4: Block individual pathways</span></div>
<ul>
<li><strong>Rapamycin:</strong> mTOR inhibition. PEARL trial (114 healthy humans, 48 weeks, $6M) showed null results. Framework predicted this</li>
<li><strong>NAD+ precursors (NMN/NR):</strong> Null results across multiple human trials. Framework predicted this null</li>
<li><strong>Metformin:</strong> AMPK activation. TAME trial ongoing. Framework predicts modest effects insufficient for meaningful age reversal alone</li>
</ul>
<h2 id="hrv">HRV coherence training</h2>
<p>Heart rate variability coherence is the Tier 1 intervention with the most immediate, measurable signal. When your heartbeat falls into a coherent pattern (smooth sinusoidal oscillation at roughly 0.1 Hz), the autonomic nervous system enters a state that enhances baroreflex sensitivity, reduces cortisol, and improves vagal tone.</p>
<p>The framework predicts that HRV coherence quality (not just practice time) should be the single best predictor of biological age reversal. Testable: coherence quality during training sessions should predict changes in GrimAge, PhenoAge, or DunedinPACE better than any pharmacological variable.</p>
<h2 id="sleep">Sleep architecture optimization</h2>
<ul>
<li>Deep sleep (N3): 90+ minutes per night for adequate glymphatic clearance</li>
<li>REM sleep: adequate duration for neural consolidation and emotional processing</li>
<li>Sleep continuity: minimal awakenings. Fragmented sleep impairs glymphatic flow even if total duration is adequate</li>
<li>Circadian alignment: consistent sleep-wake timing within a 30-minute window</li>
</ul>
<h2 id="senolytics">Senolytics</h2>
<p>Senescent cells accumulate with age and secrete a toxic cocktail of inflammatory signals (the SASP). Clearing them with senolytic compounds removes a major source of chronic inflammation. Dasatinib plus quercetin is the most studied combination, dosed intermittently (2-3 days of treatment followed by weeks off).</p>
<p>Classified as Tier 2 because they clear accumulated damage but don't restore sigma itself. Most effective when combined with Tier 1 interventions.</p>
<h2 id="cr">Caloric restriction and fasting</h2>
<p>Caloric restriction (20-30% below ad libitum intake) is the most replicated longevity intervention across species. Intermittent fasting (16:8, 5:2, or periodic multi-day fasts) captures some of these benefits without sustained caloric restriction.</p>
<h2 id="pemf-health">PEMF therapy</h2>
<p>Pulsed electromagnetic field therapy sits at the intersection of the UAF framework and biophysical medicine. The framework predicts PEMF should enhance sigma by improving fascial conductivity and tissue-level signaling coherence. See the <a href="pemf.html">full PEMF writeup</a> for mechanisms and evidence.</p>
<p>Key prediction: PEMF combined with HRV coherence training should show synergistic effects on biological age markers, since PEMF improves the physical substrate (fascial tissue) through which the heart's coherent signal propagates.</p>
<h2 id="pharma">Pharmacological interventions and their ceilings</h2>
<p>The framework makes a strong claim: no single-pathway pharmacological intervention will produce meaningful age reversal in healthy humans. Rapamycin, NMN, NR, metformin, and similar compounds are necessary components of a comprehensive protocol but insufficient when used alone or even in combination without addressing Tier 1-2 priorities.</p>
<p>The reasoning is structural. Blocking one damage pathway doesn't reduce total damage; it reroutes the damage through other channels. Only restoring sigma itself (Tier 1) or clearing the damage backlog (Tier 2) can break the self-reinforcing decline loop.</p>
<h2 id="bryan">The Bryan Johnson problem</h2>
<p>Bryan Johnson spends $2M/year on a protocol heavy on Tier 3-4 interventions. His open-data approach is admirable and his systematic measurement is world-class.</p>
<p>The framework predicts he'll hit a ceiling. The prescription: prioritize HRV coherence quality and sleep architecture (Tier 1), add senolytics (Tier 2), and treat his current supplement stack as the baseline rather than the primary strategy.</p>
<p>Specific prediction: if Johnson adds structured HRV coherence training (not just measurement, but active biofeedback), his GrimAge trajectory should inflect within 6-12 months. If it doesn't, the Tier 1 claims need revision.</p>
<h2 id="tracking">What to track</h2>
<table>
<thead><tr><th>Marker</th><th>What it measures</th><th>Frequency</th></tr></thead>
<tbody>
<tr><td>Epigenetic clocks (GrimAge, DunedinPACE)</td><td>Biological age, rate of aging</td><td>Every 6-12 months</td></tr>
<tr><td>HRV coherence score</td><td>Autonomic regulation quality</td><td>Daily</td></tr>
<tr><td>Deep sleep minutes</td><td>Glymphatic clearance capacity</td><td>Daily</td></tr>
<tr><td>hsCRP</td><td>Systemic inflammation</td><td>Quarterly</td></tr>
<tr><td>Fasting glucose / HbA1c</td><td>Metabolic health</td><td>Quarterly</td></tr>
<tr><td>VO2max</td><td>Cardiovascular fitness</td><td>Every 6 months</td></tr>
<tr><td>Grip strength</td><td>Muscle quality, all-cause mortality predictor</td><td>Monthly</td></tr>
</tbody>
</table>
<p>The framework predicts that HRV coherence score and deep sleep minutes will be the two strongest predictors of favorable changes in epigenetic age clocks. If someone only tracked two things, those would be the two.</p>
</div>
</div>"""

files = {
    'style.css': CSS,
    'index.html': page('fnsmdehip - research notes', INDEX_BODY),
    'uaf.html': page('The Unified Aetheric Framework - fnsmdehip', UAF_BODY),
    'pemf.html': page('PEMF Therapy - fnsmdehip', PEMF_BODY),
    'wifi-sensing.html': page('ESPectre: WiFi CSI Motion Detection - fnsmdehip', WIFI_BODY),
    'projects.html': page('Project Index - fnsmdehip', PROJECTS_BODY),
    'health.html': page('Health Experiments and Longevity Notes - fnsmdehip', HEALTH_BODY),
    'CNAME': 'fnsmdehip-research.surge.sh\n',
}

for fname, content in files.items():
    path = os.path.join(BASE, fname)
    with open(path, 'w') as f:
        f.write(content)
    size = os.path.getsize(path)
    print(f"  {fname}: {size:,} bytes")

total = sum(os.path.getsize(os.path.join(BASE, f)) for f in os.listdir(BASE) if not f.startswith('.'))
print(f"\nTotal site size: {total:,} bytes ({total/1024:.1f} KB)")
print("Build complete.")
