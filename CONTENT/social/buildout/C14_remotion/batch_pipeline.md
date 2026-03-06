# C14 Remotion Batch Pipeline — 50 Videos/Day

## Architecture Overview

```
data/videos.json          <- all video configs (title, steps, accent, template)
        |
        v
scripts/batch_render.ts   <- loops, calls renderMedia() per config
        |
        v
out/{slug}.mp4            <- final rendered videos
        |
        v
scripts/upload_meta.ts    <- generates title/desc/tags per video
        |
        v
upload_queue/{slug}.json  <- ready for Buffer / manual upload
```

---

## Core Batch Render Script

```typescript
// scripts/batch_render.ts
import { renderMedia, selectComposition, bundle } from "@remotion/renderer";
import path from "path";
import fs from "fs";

const CONCURRENCY = 4; // set to CPU core count
const OUT_DIR = path.join(process.cwd(), "out");
const BUNDLE_DIR = path.join(process.cwd(), ".remotion-bundle");

interface VideoConfig {
  id: string;                    // used as filename: out/{id}.mp4
  composition: string;           // e.g. "ShortClip", "Listicle"
  props: Record<string, unknown>; // override defaultProps
  durationInFrames?: number;     // optional override
}

async function buildBundle(): Promise<string> {
  console.log("Bundling Remotion project...");
  const bundleLocation = await bundle({
    entryPoint: path.join(process.cwd(), "src", "index.ts"),
    onProgress: (progress) => process.stdout.write(`\rBundle: ${Math.round(progress * 100)}%`),
  });
  console.log("\nBundle complete:", bundleLocation);
  return bundleLocation;
}

async function renderOne(
  bundleLocation: string,
  config: VideoConfig
): Promise<void> {
  const outPath = path.join(OUT_DIR, `${config.id}.mp4`);

  // Skip if already rendered
  if (fs.existsSync(outPath)) {
    console.log(`[SKIP] ${config.id} already exists`);
    return;
  }

  const composition = await selectComposition({
    serveUrl: bundleLocation,
    id: config.composition,
    inputProps: config.props,
  });

  console.log(`[START] Rendering ${config.id} (${composition.durationInFrames} frames)`);
  const start = Date.now();

  await renderMedia({
    composition: {
      ...composition,
      ...(config.durationInFrames ? { durationInFrames: config.durationInFrames } : {}),
    },
    serveUrl: bundleLocation,
    codec: "h264",
    outputLocation: outPath,
    inputProps: config.props,
    concurrency: 1,              // per-render concurrency (use 1 for batch)
    videoBitrate: "8M",
    onProgress: ({ renderedFrames, totalFrames }) => {
      const pct = Math.round((renderedFrames / totalFrames) * 100);
      process.stdout.write(`\r  [${config.id}] ${pct}% (${renderedFrames}/${totalFrames})`);
    },
  });

  const elapsed = ((Date.now() - start) / 1000).toFixed(1);
  console.log(`\n  [DONE] ${config.id} — ${elapsed}s → ${outPath}`);
}

async function batchRender(configs: VideoConfig[]): Promise<void> {
  if (!fs.existsSync(OUT_DIR)) fs.mkdirSync(OUT_DIR, { recursive: true });

  const bundleLocation = await buildBundle();

  // Process in chunks of CONCURRENCY
  for (let i = 0; i < configs.length; i += CONCURRENCY) {
    const chunk = configs.slice(i, i + CONCURRENCY);
    console.log(`\nRendering chunk ${Math.floor(i / CONCURRENCY) + 1}/${Math.ceil(configs.length / CONCURRENCY)}: ${chunk.map(c => c.id).join(", ")}`);
    await Promise.all(chunk.map(config => renderOne(bundleLocation, config)));
  }

  console.log(`\nBatch complete. ${configs.length} videos in ${OUT_DIR}`);
}

// Load configs and run
const configs: VideoConfig[] = JSON.parse(
  fs.readFileSync(path.join(process.cwd(), "data", "videos.json"), "utf-8")
);

batchRender(configs).catch(console.error);
```

**Run it:**
```bash
npx ts-node scripts/batch_render.ts
# or
node --loader ts-node/esm scripts/batch_render.ts
```

---

## data/videos.json — Example 50-Video Dataset

```json
[
  {
    "id": "short_cold_email_v1",
    "composition": "ShortClip",
    "props": {
      "title": "cold emailed 500 people. here's exactly what happened.",
      "steps": [
        "found 500 emails on Hunter.io ($49/mo)",
        "sent them over 3 days via Instantly.ai ($37/mo)",
        "12 replies. 2 demos booked. 1 closed at $1,500"
      ],
      "accent": "#FF5733"
    }
  },
  {
    "id": "short_gumroad_v1",
    "composition": "ShortClip",
    "props": {
      "title": "$900 from one Notion template. step by step.",
      "steps": [
        "built a Notion CRM template in 3 hours",
        "listed on Gumroad for $29",
        "posted 3 tweets. 31 sales in 5 days"
      ],
      "accent": "#6C63FF"
    }
  },
  {
    "id": "short_newsletter_v1",
    "composition": "ShortClip",
    "props": {
      "title": "0 to 1,000 newsletter subscribers without paid ads.",
      "steps": [
        "posted 3 Reddit threads in r/Entrepreneur",
        "included lead magnet link in bio",
        "900 subscribers in 11 days. zero dollars spent."
      ],
      "accent": "#22C55E"
    }
  },
  {
    "id": "stats_march_2026",
    "composition": "StatsReveal",
    "props": {
      "metric": "$3,200",
      "label": "revenue in 30 days",
      "breakdown": [
        { "label": "Cold email clients", "value": 56, "display": "$1,800" },
        { "label": "Affiliate commissions", "value": 28, "display": "$900" },
        { "label": "Gumroad templates", "value": 16, "display": "$500" }
      ],
      "accent": "#FF5733"
    }
  },
  {
    "id": "listicle_ai_tools_v1",
    "composition": "Listicle",
    "props": {
      "title": "5 AI tools I used to make $3K last month",
      "items": [
        { "number": "01", "text": "Hunter.io", "subtext": "200 leads in 2 hours, $49/mo" },
        { "number": "02", "text": "Instantly.ai", "subtext": "500 emails sent for $37" },
        { "number": "03", "text": "Beehiiv", "subtext": "newsletter at $0 to 1K subs" },
        { "number": "04", "text": "Gumroad", "subtext": "sold 2 templates, $600" },
        { "number": "05", "text": "visualping.io", "subtext": "tracked 200 competitor pages" }
      ],
      "accent": "#F59E0B"
    }
  }
]
```

---

## Upload Metadata Generator

After rendering, auto-generate upload metadata for each video:

```typescript
// scripts/generate_upload_meta.ts
import fs from "fs";
import path from "path";

interface UploadMeta {
  file: string;
  title: string;
  description: string;
  tags: string[];
  platforms: PlatformMeta[];
}

interface PlatformMeta {
  platform: "youtube_shorts" | "tiktok" | "instagram_reels" | "twitter";
  caption: string;
  hashtags: string[];
  scheduledTime?: string;
}

const PLATFORM_HASHTAGS: Record<string, string[]> = {
  youtube_shorts: ["#shorts", "#money", "#sidehustle", "#makemoney", "#solopreneur"],
  tiktok: ["#fyp", "#entrepreneur", "#money", "#sidehustle", "#businesstips"],
  instagram_reels: ["#reels", "#entrepreneur", "#sidehustle", "#passiveincome", "#solopreneur"],
  twitter: [],
};

function generateMeta(config: Record<string, unknown>, videoId: string): UploadMeta {
  const props = config.props as Record<string, unknown>;
  const title = props.title as string;

  return {
    file: `out/${videoId}.mp4`,
    title: title.charAt(0).toUpperCase() + title.slice(1),
    description: `${title}\n\nFollow @printmaxxer for daily money methods.\n\n#solopreneur #makemoney #sidehustle`,
    tags: ["solopreneur", "side hustle", "make money online", "cold email", "passive income"],
    platforms: [
      {
        platform: "youtube_shorts",
        caption: title,
        hashtags: PLATFORM_HASHTAGS.youtube_shorts,
        scheduledTime: getNextSlot("youtube"),
      },
      {
        platform: "tiktok",
        caption: `${title} 👇`,
        hashtags: PLATFORM_HASHTAGS.tiktok,
        scheduledTime: getNextSlot("tiktok"),
      },
      {
        platform: "twitter",
        caption: `${title}\n\nthread below 👇`,
        hashtags: [],
      },
    ],
  };
}

// Simple round-robin scheduler: 3 videos/day at 8am, 12pm, 6pm
const scheduledCounts: Record<string, number> = {};
function getNextSlot(platform: string): string {
  const count = scheduledCounts[platform] || 0;
  scheduledCounts[platform] = count + 1;
  const dayOffset = Math.floor(count / 3);
  const slotIndex = count % 3;
  const slots = ["08:00", "12:00", "18:00"];
  const date = new Date();
  date.setDate(date.getDate() + dayOffset);
  return `${date.toISOString().split("T")[0]}T${slots[slotIndex]}:00`;
}

// Generate for all rendered videos
const configs = JSON.parse(fs.readFileSync("data/videos.json", "utf-8"));
const queueDir = path.join(process.cwd(), "upload_queue");
if (!fs.existsSync(queueDir)) fs.mkdirSync(queueDir);

configs.forEach((config: Record<string, unknown>) => {
  const videoId = config.id as string;
  const outFile = path.join(process.cwd(), "out", `${videoId}.mp4`);
  if (!fs.existsSync(outFile)) return; // only process rendered videos

  const meta = generateMeta(config, videoId);
  fs.writeFileSync(
    path.join(queueDir, `${videoId}.json`),
    JSON.stringify(meta, null, 2)
  );
  console.log(`Generated meta: upload_queue/${videoId}.json`);
});
```

---

## Scheduling: 50 Videos/Day Production Plan

### Machine Requirements

| Target | Machine | Render Speed | Cost |
|--------|---------|-------------|------|
| 10 videos/day | M1 MacBook Pro (local) | ~3 min/video | $0 |
| 50 videos/day | Hetzner CPX31 (4 vCPU) | ~5 min/video | ~$15/mo |
| 100+ videos/day | Hetzner CPX51 (8 vCPU) | ~3 min/video | ~$30/mo |

### Daily Automation (crontab)

```bash
# Render batch every night at 1 AM (runs while sleeping)
0 1 * * * cd /path/to/printmaxx-videos && npx ts-node scripts/batch_render.ts >> logs/render.log 2>&1

# Generate upload metadata at 2 AM (after renders complete)
0 2 * * * cd /path/to/printmaxx-videos && npx ts-node scripts/generate_upload_meta.ts >> logs/meta.log 2>&1

# Optional: Auto-upload to YouTube via yt-dlp or YouTube Data API
0 3 * * * cd /path/to/printmaxx-videos && python3 scripts/upload_youtube.py >> logs/upload.log 2>&1
```

### Content Pipeline: Claude → Remotion → Platform

```
Step 1: Generate video data (5 min)
  claude -p "Generate 10 ShortClip configs for printmaxx money method content.
  Output valid JSON array matching VideoConfig interface." > data/new_batch.json

Step 2: Append to videos.json
  cat data/new_batch.json | jq '.[]' >> data/videos.json

Step 3: Run batch render (overnight or background)
  npx ts-node scripts/batch_render.ts

Step 4: Generate upload metadata
  npx ts-node scripts/generate_upload_meta.ts

Step 5: Upload (manual or via API)
  # YouTube: upload_queue/*.json + out/*.mp4
  # TikTok: manual upload (no public API)
  # Instagram: via Buffer API or manual
```

---

## VPS Setup for Headless Rendering

```bash
# Hetzner CPX31: $15/mo, Ubuntu 22.04
# SSH in and run:

# Install Node 20
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install Chrome dependencies (Remotion uses Chromium internally)
sudo apt-get install -y \
  libnss3 libatk-bridge2.0-0 libdrm2 libxkbcommon0 \
  libgbm1 libasound2 libpangocairo-1.0-0 \
  libxcomposite1 libxcursor1 libxdamage1 libxfixes3 \
  libxi6 libxrandr2 libxtst6 fonts-liberation

# Clone project
git clone <your-repo> printmaxx-videos
cd printmaxx-videos
npm install

# Test render
npx remotion render ShortClip out/test.mp4

# Install PM2 for process management
npm install -g pm2
pm2 start "npx ts-node scripts/batch_render.ts" --name remotion-batch
pm2 logs remotion-batch
```

---

## Quality Checks Before Upload

Run after each batch:

```bash
# Check all renders completed (no 0-byte files)
find out/ -name "*.mp4" -size 0 -delete

# Check duration is correct (requires ffprobe)
for f in out/*.mp4; do
  duration=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$f")
  echo "$f: ${duration}s"
done

# Check file sizes (anything < 1MB is probably broken)
find out/ -name "*.mp4" -size -1M -ls
```

---

## Cost Math

| Scenario | Volume | Machine | Cost | Videos/$ |
|----------|--------|---------|------|----------|
| Local Mac (free tier) | 10/day = 300/mo | M1 MacBook | $0 electricity | infinite |
| VPS batch (nights only) | 50/day = 1,500/mo | Hetzner CPX31 | $15/mo | 100/$ |
| VPS full-time | 200/day = 6,000/mo | Hetzner CPX51 | $30/mo | 200/$ |
| Synthesia equivalent | same volumes | Synthesia | $900/mo minimum | 6.7/$ |

**Summary:** Remotion batch on VPS = 30x cheaper than Synthesia at scale. Break even vs Synthesia at video #1.
