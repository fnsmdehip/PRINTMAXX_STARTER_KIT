# C14 Remotion Video Templates, 5 Production-Ready Designs

Each template: complete component code + usage + output specs + batch-render example.

---

## Template 1: ShortClip, Hook + Steps Reveal

**What it produces:** 30-second vertical video. Bold hook text, numbered steps animate in one by one, CTA at end. Designed for TikTok, YouTube Shorts, Instagram Reels.

**Output specs:** 1080x1920, 30fps, 900 frames (30s), H264

**Use cases:** Money method walkthroughs, tool tutorials, "how I did X" content

```typescript
// src/compositions/ShortClip.tsx
import { AbsoluteFill, interpolate, useCurrentFrame, spring, Sequence } from "remotion";
import { TOKENS } from "../tokens";

interface Props {
  title: string;
  steps: string[];
  accent: string;
}

export const ShortClip: React.FC<Props> = ({ title, steps, accent }) => {
  const frame = useCurrentFrame();

  // Title fades + slides up in first 30 frames
  const titleOpacity = interpolate(frame, [0, 30], [0, 1], { extrapolateRight: "clamp" });
  const titleY = interpolate(frame, [0, 30], [40, 0], { extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ background: TOKENS.colors.bg, padding: TOKENS.spacing.xl }}>
      {/* Hook line */}
      <div style={{
        opacity: titleOpacity,
        transform: `translateY(${titleY}px)`,
        fontSize: 72,
        fontFamily: TOKENS.fonts.heading,
        fontWeight: 900,
        color: TOKENS.colors.text,
        lineHeight: 1.1,
        marginBottom: TOKENS.spacing.lg,
        borderLeft: `8px solid ${accent}`,
        paddingLeft: TOKENS.spacing.md,
      }}>
        {title}
      </div>

      {/* Steps, each appears at 60-frame intervals */}
      {steps.map((step, i) => (
        <Sequence from={60 + i * 60} key={i}>
          <StepItem text={step} index={i} accent={accent} />
        </Sequence>
      ))}

      {/* CTA, appears at frame 720 */}
      <Sequence from={720}>
        <CTABadge accent={accent} />
      </Sequence>
    </AbsoluteFill>
  );
};

const StepItem: React.FC<{ text: string; index: number; accent: string }> = ({ text, index, accent }) => {
  const frame = useCurrentFrame();
  const scale = spring({ frame, fps: 30, config: { stiffness: 200, damping: 20 } });
  const opacity = interpolate(frame, [0, 15], [0, 1], { extrapolateRight: "clamp" });

  return (
    <div style={{
      opacity,
      transform: `scale(${scale})`,
      display: "flex",
      alignItems: "center",
      gap: TOKENS.spacing.md,
      marginBottom: TOKENS.spacing.sm,
      background: TOKENS.colors.bgCard,
      borderRadius: 16,
      padding: `${TOKENS.spacing.sm}px ${TOKENS.spacing.md}px`,
    }}>
      <span style={{ fontSize: 48, fontWeight: 900, color: accent, minWidth: 60 }}>
        {String(index + 1).padStart(2, "0")}
      </span>
      <span style={{ fontSize: 40, fontFamily: TOKENS.fonts.heading, color: TOKENS.colors.text }}>
        {text}
      </span>
    </div>
  );
};

const CTABadge: React.FC<{ accent: string }> = ({ accent }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: "clamp" });
  return (
    <div style={{
      opacity,
      position: "absolute",
      bottom: 80,
      left: 0,
      right: 0,
      textAlign: "center",
      fontSize: 44,
      fontWeight: 700,
      color: accent,
      fontFamily: TOKENS.fonts.heading,
    }}>
      follow for daily methods
    </div>
  );
};
```

**Batch render example:**
```typescript
const videos = [
  { title: "cold emailed 500 people. here's what happened.", steps: ["Found 500 emails on Hunter.io", "Sent in 3 days via Instantly.ai", "Got 12 replies. Closed 2 deals."], accent: "#FF5733" },
  { title: "I made $900 from one Gumroad product.", steps: ["Wrote a 10-page Notion template", "Listed for $29 on Gumroad", "Posted 3 tweets. 31 sales."], accent: "#6C63FF" },
];
// See batch_pipeline.md for renderMedia() loop
```

---

## Template 2: StatsReveal, Metric Countdown + Breakdown

**What it produces:** 15-second landscape video. Big metric counts up from 0, breakdown bars animate in. Designed for Twitter/X embeds, LinkedIn, YouTube Community posts.

**Output specs:** 1920x1080, 30fps, 450 frames (15s), H264

**Use cases:** Monthly income reports, app download milestones, subscriber counts

```typescript
// src/compositions/StatsReveal.tsx
import { AbsoluteFill, interpolate, useCurrentFrame, Sequence, spring } from "remotion";
import { TOKENS } from "../tokens";

interface Breakdown { label: string; value: number; display: string; }

interface Props {
  metric: string;
  label: string;
  breakdown: Breakdown[];
  accent: string;
}

export const StatsReveal: React.FC<Props> = ({ metric, label, breakdown, accent }) => {
  const frame = useCurrentFrame();

  // Metric text scales up at start
  const metricScale = spring({ frame, fps: 30, config: { stiffness: 80, damping: 12 } });
  const metricOpacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{
      background: TOKENS.colors.bg,
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      padding: TOKENS.spacing.xl,
    }}>
      {/* Big metric */}
      <div style={{
        opacity: metricOpacity,
        transform: `scale(${metricScale})`,
        fontSize: 180,
        fontWeight: 900,
        fontFamily: TOKENS.fonts.heading,
        color: accent,
        lineHeight: 1,
      }}>
        {metric}
      </div>
      <div style={{ fontSize: 48, color: TOKENS.colors.textMuted, marginBottom: 60 }}>
        {label}
      </div>

      {/* Breakdown bars */}
      <div style={{ width: "80%", display: "flex", flexDirection: "column", gap: 20 }}>
        {breakdown.map((item, i) => (
          <Sequence from={60 + i * 45} key={i}>
            <BreakdownBar item={item} accent={accent} />
          </Sequence>
        ))}
      </div>
    </AbsoluteFill>
  );
};

const BreakdownBar: React.FC<{ item: Breakdown; accent: string }> = ({ item, accent }) => {
  const frame = useCurrentFrame();
  const width = interpolate(frame, [0, 45], [0, (item.value / 100) * 100], { extrapolateRight: "clamp" });
  const opacity = interpolate(frame, [0, 15], [0, 1], { extrapolateRight: "clamp" });

  return (
    <div style={{ opacity }}>
      <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 8 }}>
        <span style={{ fontSize: 32, color: TOKENS.colors.text }}>{item.label}</span>
        <span style={{ fontSize: 32, fontWeight: 700, color: accent }}>{item.display}</span>
      </div>
      <div style={{ background: TOKENS.colors.bgCard, borderRadius: 8, height: 12 }}>
        <div style={{ background: accent, width: `${width}%`, height: "100%", borderRadius: 8, transition: "none" }} />
      </div>
    </div>
  );
};
```

---

## Template 3: Listicle, Animated Slide Deck

**What it produces:** 50-second vertical video. Title slide, then numbered items slide in one per 8 seconds with icons. Designed for TikTok, Reels, Shorts.

**Output specs:** 1080x1920, 30fps, 1500 frames (50s), H264

**Use cases:** "5 AI tools I use every day", "Top 10 money methods", "7 mistakes I made"

```typescript
// src/compositions/Listicle.tsx
import { AbsoluteFill, interpolate, useCurrentFrame, Sequence, spring } from "remotion";
import { TOKENS } from "../tokens";

interface ListItem { number: string; text: string; subtext?: string; }

interface Props {
  title: string;
  items: ListItem[];
  accent: string;
}

export const Listicle: React.FC<Props> = ({ title, items, accent }) => {
  const ITEM_DURATION = 240; // 8 seconds per item

  return (
    <AbsoluteFill style={{ background: TOKENS.colors.bg }}>
      {/* Title card, first 60 frames */}
      <Sequence from={0} durationInFrames={90}>
        <TitleCard title={title} accent={accent} />
      </Sequence>

      {/* Items */}
      {items.map((item, i) => (
        <Sequence from={90 + i * ITEM_DURATION} durationInFrames={ITEM_DURATION} key={i}>
          <ItemCard item={item} accent={accent} total={items.length} index={i} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};

const TitleCard: React.FC<{ title: string; accent: string }> = ({ title, accent }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 30], [0, 1], { extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{
      opacity,
      background: accent,
      alignItems: "center",
      justifyContent: "center",
      padding: TOKENS.spacing.xl,
    }}>
      <div style={{ fontSize: 80, fontWeight: 900, textAlign: "center", color: "#000", lineHeight: 1.1 }}>
        {title}
      </div>
    </AbsoluteFill>
  );
};

const ItemCard: React.FC<{ item: ListItem; accent: string; total: number; index: number }> = ({ item, accent, total, index }) => {
  const frame = useCurrentFrame();
  const slideX = interpolate(frame, [0, 30], [100, 0], { extrapolateRight: "clamp" });
  const opacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{
      opacity,
      transform: `translateX(${slideX}px)`,
      background: TOKENS.colors.bg,
      padding: TOKENS.spacing.xl,
      justifyContent: "center",
    }}>
      {/* Progress */}
      <div style={{ color: TOKENS.colors.textMuted, fontSize: 36, marginBottom: 40 }}>
        {index + 1} / {total}
      </div>
      {/* Number */}
      <div style={{ fontSize: 160, fontWeight: 900, color: accent, lineHeight: 1 }}>
        {item.number}
      </div>
      {/* Text */}
      <div style={{ fontSize: 64, fontWeight: 700, color: TOKENS.colors.text, lineHeight: 1.2, marginTop: 24 }}>
        {item.text}
      </div>
      {item.subtext && (
        <div style={{ fontSize: 40, color: TOKENS.colors.textMuted, marginTop: 20 }}>
          {item.subtext}
        </div>
      )}
    </AbsoluteFill>
  );
};
```

---

## Template 4: ColdEmailTutorial, Screen + Text Walkthrough

**What it produces:** 45-second horizontal video. Step-by-step cold email anatomy with animated highlights. Designed for YouTube, LinkedIn.

**Output specs:** 1920x1080, 30fps, 1350 frames (45s), H264

**Use cases:** Cold email breakdowns, sales process walkthroughs, before/after comparisons

```typescript
// src/compositions/ColdEmailTutorial.tsx
import { AbsoluteFill, interpolate, useCurrentFrame, Sequence } from "remotion";
import { TOKENS } from "../tokens";

interface EmailSection {
  label: string;
  text: string;
  color: string;
  startFrame: number;
}

interface Props {
  subject: string;
  sections: EmailSection[];
}

export const ColdEmailTutorial: React.FC<Props> = ({ subject, sections }) => {
  const frame = useCurrentFrame();
  const headerOpacity = interpolate(frame, [0, 30], [0, 1], { extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ background: TOKENS.colors.bg, padding: 80, flexDirection: "row", gap: 60 }}>
      {/* Left: Email preview */}
      <div style={{ flex: 1, background: TOKENS.colors.bgCard, borderRadius: 24, padding: 48, opacity: headerOpacity }}>
        <div style={{ fontSize: 28, color: TOKENS.colors.textMuted, marginBottom: 16 }}>Subject:</div>
        <div style={{ fontSize: 36, fontWeight: 700, color: TOKENS.colors.text, marginBottom: 40 }}>{subject}</div>
        <div style={{ height: 2, background: "#222", marginBottom: 40 }} />
        {sections.map((section, i) => (
          <Sequence from={section.startFrame} key={i}>
            <EmailLine section={section} />
          </Sequence>
        ))}
      </div>

      {/* Right: Annotations */}
      <div style={{ width: 600, display: "flex", flexDirection: "column", gap: 24 }}>
        {sections.map((section, i) => (
          <Sequence from={section.startFrame} key={i}>
            <Annotation label={section.label} color={section.color} />
          </Sequence>
        ))}
      </div>
    </AbsoluteFill>
  );
};

const EmailLine: React.FC<{ section: EmailSection }> = ({ section }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: "clamp" });
  return (
    <div style={{
      opacity,
      borderLeft: `4px solid ${section.color}`,
      paddingLeft: 20,
      marginBottom: 20,
      fontSize: 32,
      color: TOKENS.colors.text,
      lineHeight: 1.5,
    }}>
      {section.text}
    </div>
  );
};

const Annotation: React.FC<{ label: string; color: string }> = ({ label, color }) => {
  const frame = useCurrentFrame();
  const x = interpolate(frame, [0, 25], [40, 0], { extrapolateRight: "clamp" });
  const opacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: "clamp" });
  return (
    <div style={{
      opacity,
      transform: `translateX(${x}px)`,
      background: color + "22",
      border: `2px solid ${color}`,
      borderRadius: 12,
      padding: "16px 24px",
      fontSize: 32,
      color,
      fontWeight: 700,
    }}>
      {label}
    </div>
  );
};
```

**Default props example:**
```typescript
defaultProps: {
  subject: "quick question about [company]'s lead gen",
  sections: [
    { label: "Hook, problem they have", text: "saw your team is hiring 3 BDRs. usually means the current pipeline needs backup.", color: "#FF5733", startFrame: 60 },
    { label: "Social proof", text: "helped a similar SaaS book 40 demos in 6 weeks with cold email.", color: "#6C63FF", startFrame: 150 },
    { label: "CTA, one ask only", text: "worth a 15-min call this week?", color: "#22C55E", startFrame: 240 },
  ]
}
```

---

## Template 5: QuoteCard, Animated Text Pull Quote

**What it produces:** 10-second square or vertical video. Bold quote animates in word by word, author + handle appears, subtle background motion. Designed for Twitter/X, Instagram, LinkedIn.

**Output specs:** 1080x1080 (square) or 1080x1920 (vertical), 30fps, 300 frames (10s), H264

**Use cases:** Hot takes, stats pulled from newsletters, client testimonials, authority quotes

```typescript
// src/compositions/QuoteCard.tsx
import { AbsoluteFill, interpolate, useCurrentFrame, spring } from "remotion";
import { TOKENS } from "../tokens";

interface Props {
  quote: string;
  author: string;
  handle: string;
  accent: string;
  bgStyle: "dark" | "gradient" | "brand";
}

export const QuoteCard: React.FC<Props> = ({ quote, author, handle, accent, bgStyle }) => {
  const frame = useCurrentFrame();

  const words = quote.split(" ");

  // Author slides up
  const authorY = interpolate(frame, [200, 250], [30, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const authorOpacity = interpolate(frame, [200, 250], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  const background = bgStyle === "gradient"
    ? `linear-gradient(135deg, ${accent}22, ${TOKENS.colors.bg})`
    : bgStyle === "brand"
    ? accent
    : TOKENS.colors.bg;

  return (
    <AbsoluteFill style={{
      background,
      padding: TOKENS.spacing.xl,
      justifyContent: "center",
      alignItems: "flex-start",
    }}>
      {/* Accent bar */}
      <div style={{ width: 80, height: 8, background: accent, borderRadius: 4, marginBottom: 40 }} />

      {/* Quote, word by word */}
      <div style={{ fontSize: 68, fontWeight: 800, color: TOKENS.colors.text, lineHeight: 1.2, marginBottom: 60 }}>
        {words.map((word, i) => {
          const wordStart = Math.floor((i / words.length) * 150);
          const wordOpacity = interpolate(frame, [wordStart, wordStart + 20], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          });
          const wordY = interpolate(frame, [wordStart, wordStart + 15], [15, 0], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          });
          return (
            <span key={i} style={{
              opacity: wordOpacity,
              display: "inline-block",
              transform: `translateY(${wordY}px)`,
              marginRight: 14,
            }}>
              {word}
            </span>
          );
        })}
      </div>

      {/* Author */}
      <div style={{ opacity: authorOpacity, transform: `translateY(${authorY}px)` }}>
        <div style={{ fontSize: 40, fontWeight: 700, color: accent }}>{author}</div>
        <div style={{ fontSize: 32, color: TOKENS.colors.textMuted }}>{handle}</div>
      </div>
    </AbsoluteFill>
  );
};
```

**Batch data example (10 quote cards from newsletter issue):**
```typescript
const quotes = [
  { quote: "cold email is still the highest ROI channel in 2026 if you're not buying leads", author: "Dan K", handle: "@printmaxxer", accent: "#FF5733", bgStyle: "dark" },
  { quote: "the guy making $8K/month doesn't have better ideas. he sends 10x more emails.", author: "printmaxx weekly", handle: "issue #14", accent: "#6C63FF", bgStyle: "gradient" },
  { quote: "Hunter.io + Instantly.ai + a good offer = pipeline on demand", author: "Dan K", handle: "@printmaxxer", accent: "#22C55E", bgStyle: "dark" },
];
// renders to out/quote_001.mp4, out/quote_002.mp4 ... etc
```

---

## Template Summary Table

| Template | Dimensions | Duration | Best Platform | Primary Use |
|----------|-----------|----------|---------------|-------------|
| ShortClip | 1080x1920 | 30s | TikTok, Shorts | How-I-did-X walkthroughs |
| StatsReveal | 1920x1080 | 15s | Twitter/X, LinkedIn | Monthly income reports |
| Listicle | 1080x1920 | 50s | TikTok, Reels | Top 5/10 list content |
| ColdEmailTutorial | 1920x1080 | 45s | YouTube, LinkedIn | Tactical breakdowns |
| QuoteCard | 1080x1080 | 10s | Twitter/X, Instagram | Hot takes, testimonials |
