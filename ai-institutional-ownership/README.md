# AI Institutional Ownership · Independent module

Standalone public module for Victor Investment OS. Route: `/ai-institutional-ownership/`.

## Current status
The app renders a transparent **pending verification** state; it does not claim a validated index or current institutional flows. A GitHub Action checks the official SEC 13F bulk archive publication page daily, recording source-check metadata in `data/latest.json`. **It does not compute institutional holdings daily.** Full quarterly ownership history requires the separate 13F ingestion, CUSIP security mapping, deduplication of amendments and other managers, share-split normalization and historical sample construction.

## Overview integration
The module can later be embedded as an iframe:
`<iframe src="https://victorhtsai.github.io/ai-institutional-ownership/" title="AI Institutional Ownership" style="width:100%;height:950px;border:0"></iframe>`

## Notes
13F generally provides quarterly U.S.-reportable long holdings, with up to 45-day filing lag. Gross holdings should never be described as cash inflows or true long-short net exposure. The currently chosen research universe is provisional and will be revisited for IPOs and name changes.

Source: https://www.sec.gov/data-research/sec-markets-data/form-13f-data-sets
