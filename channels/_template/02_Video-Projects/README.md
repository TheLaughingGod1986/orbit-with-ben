# Films

One folder per film: `NNN_Short-Title` (`012_How-Does-It-Work`). The studio makes the folder when the film gets
its topic, and keeps a `status.json` in it:

```json
{
  "film": "012",
  "title": "",
  "air": "",
  "stages": {},
  "claims": [],
  "next": ""
}
```

`stages` fills in as work is done (`{"script": {"state": "done", "ref": "<commit>"}}`). Nobody edits it by hand:
the job queue does, so the board always shows what the record proves.
