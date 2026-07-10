# tpc-tools

Plugin marketplace for The Prompting Company.

## Plugins

- **geo-report**: Generate a GEO (answer-engine visibility) baseline report from
  promptingco `prompts` and `cited-sources` exports, in the two-page template.

## Install

Run:

```
/plugin marketplace add spovalova/tpc-tools
/plugin install geo-report@tpc-tools
```

To get updates later:

```
/plugin marketplace update
```

## Use

Provide a product's two CSV exports (the `prompts` export and the
`cited-sources` export) and ask for a GEO report. Before the citation mix is
trusted, edit the `OWNED` / `COMPETITOR` domain lists at the top of
`plugins/geo-report/skills/geo-report/analyze.py` for that client.
