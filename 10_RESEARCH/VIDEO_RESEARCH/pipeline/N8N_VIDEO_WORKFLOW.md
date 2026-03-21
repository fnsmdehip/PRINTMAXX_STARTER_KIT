# n8n Video Autopilot Workflow

n8n orchestrates the full pipeline. when a step needs LLM intelligence,
n8n calls `claude -p` via Execute Command node, gets the result back,
and continues the workflow.

n8n is already running at localhost:5678. autonomous_integrator.py can
deploy workflows via the n8n API.

## workflow: VIDEO_AUTOPILOT

```
trigger: cron (every 6 hours) OR webhook (manual)
  │
  ├─[1] TREND CHECK (n8n HTTP node)
  │     GET TikTok Creative Center trending sounds/hashtags
  │     GET Reddit r/aivideo hot posts
  │     → merge results into $json.trends
  │
  ├─[2] SCRIPT GENERATION (Execute Command node)
  │     claude -p "Generate 5 video scripts for {niche}.
  │     Trending topics: {$json.trends}.
  │     Format: JSON array with hook, body, cta, topic fields.
  │     Each script 15-30 seconds for TikTok/Reels."
  │     → parse JSON output → $json.scripts[]
  │
  ├─[3] TOOL SELECTION (Execute Command node)
  │     python3 AUTOMATIONS/ai_video_content_pipeline.py --select-tool volume
  │     → $json.best_tool (reads from ALL_TOOLS_TRACKER.csv)
  │
  ├─[4] VIDEO GENERATION (branched by tool)
  │     ├─ IF Kling: n8n HTTP node → Kling API ($0.07/sec)
  │     ├─ IF Hailuo: n8n HTTP node → MiniMax API ($0.01/sec)
  │     ├─ IF Veo: n8n HTTP node → Vertex AI API ($0.15/sec)
  │     └─ IF none: save prompt to manual queue
  │     → $json.raw_video_path
  │
  ├─[5] AUTO-EDIT (Execute Command node)
  │     whisper $json.raw_video_path --model small --output_format srt
  │     ffmpeg [caption + hook overlay + resize + music]
  │     OR: remotion render (if template-based content)
  │     → $json.edited_videos = {tiktok: path, reels: path, shorts: path}
  │
  ├─[6] CAPTION GENERATION (Execute Command node)
  │     claude -p "Write platform-specific captions for this video:
  │     Topic: {$json.scripts[i].topic}
  │     Niche: {niche}
  │     Format: JSON with tiktok_caption, ig_caption, yt_title, hashtags"
  │     → $json.captions
  │
  ├─[7] SCHEDULE (n8n HTTP node → Publer API)
  │     POST /api/v1/posts
  │     body: {video, caption, scheduled_at, account_ids}
  │     → $json.post_ids[]
  │
  └─[8] TRACK (Execute Command node)
        python3 -c "append to AI_VIDEO_CONTENT_TRACKER.csv"
        → logged for performance feedback
```

## n8n workflow JSON (deployable via API)

```json
{
  "name": "VIDEO_AUTOPILOT",
  "nodes": [
    {
      "name": "Cron Trigger",
      "type": "n8n-nodes-base.cron",
      "parameters": {"rule": {"interval": [{"field": "hours", "hoursInterval": 6}]}}
    },
    {
      "name": "Check Trends",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "https://www.reddit.com/r/aivideo/hot.json?limit=5",
        "method": "GET",
        "headers": {"User-Agent": "printmaxx/1.0"}
      }
    },
    {
      "name": "Generate Scripts",
      "type": "n8n-nodes-base.executeCommand",
      "parameters": {
        "command": "claude -p 'Generate 3 TikTok video scripts about fitness. Output as JSON array with fields: topic, hook, body, cta. Each 15-30 seconds.' --output-format json"
      }
    },
    {
      "name": "Select Best Tool",
      "type": "n8n-nodes-base.executeCommand",
      "parameters": {
        "command": "cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt && python3 -c \"from AUTOMATIONS.ai_video_content_pipeline import select_tools_for_content; import json; print(json.dumps(select_tools_for_content('volume', 1)[0]))\""
      }
    },
    {
      "name": "Generate Video (Kling API)",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "https://api.klingai.com/v1/videos/text2video",
        "method": "POST",
        "authentication": "genericCredentialType",
        "body": {
          "prompt": "={{$node['Generate Scripts'].json.scripts[0].topic}}",
          "aspect_ratio": "9:16",
          "duration": 10
        }
      }
    },
    {
      "name": "Auto Edit (FFmpeg)",
      "type": "n8n-nodes-base.executeCommand",
      "parameters": {
        "command": "cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt && whisper {{$json.video_path}} --model small --output_format srt && ffmpeg -i {{$json.video_path}} -vf \"subtitles={{$json.srt_path}}:force_style='FontSize=22,Bold=1,Alignment=2'\" -y {{$json.output_path}}"
      }
    },
    {
      "name": "Generate Captions",
      "type": "n8n-nodes-base.executeCommand",
      "parameters": {
        "command": "claude -p 'Write TikTok caption with hashtags for a video about: {{$json.topic}}. Format: just the caption text, nothing else.'"
      }
    },
    {
      "name": "Schedule via Publer",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "https://app.publer.io/api/v1/posts",
        "method": "POST",
        "authentication": "genericCredentialType",
        "body": {
          "account_ids": ["={{$env.PUBLER_TIKTOK_ID}}"],
          "text": "={{$node['Generate Captions'].json.caption}}",
          "media_urls": ["={{$json.edited_video_url}}"],
          "is_video": true
        }
      }
    },
    {
      "name": "Track in CSV",
      "type": "n8n-nodes-base.executeCommand",
      "parameters": {
        "command": "cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt && python3 AUTOMATIONS/ai_video_content_pipeline.py --track-post '{{$json}}'"
      }
    }
  ]
}
```

## claude -p pattern for n8n LLM nodes

whenever n8n needs intelligence (script writing, caption generation, analysis),
use the Execute Command node with:

```bash
claude -p "YOUR_PROMPT_HERE" --output-format json
```

this keeps everything local (no API key needed, runs on Claude Max subscription),
and the output flows back into n8n for the next node.

for longer/complex prompts, write to a temp file and pipe:

```bash
cat /tmp/prompt.txt | claude -p --output-format json
```

## API keys needed

| service | env var | status |
|---------|---------|--------|
| Kling API | KLING_API_KEY | NEEDS SETUP |
| Publer API | PUBLER_API_TOKEN | NEEDS SETUP |
| Hailuo/MiniMax API | MINIMAX_API_KEY | NEEDS SETUP |
| Veo (Vertex AI) | GOOGLE_APPLICATION_CREDENTIALS | NEEDS SETUP |

## deployment

deploy via autonomous_integrator.py:
```bash
python3 AUTOMATIONS/autonomous_integrator.py --deploy-n8n VIDEO_AUTOPILOT
```

or manually via n8n API:
```bash
curl -X POST http://localhost:5678/api/v1/workflows \
  -H "Content-Type: application/json" \
  -d @10_RESEARCH/VIDEO_RESEARCH/pipeline/n8n_video_autopilot.json
```
