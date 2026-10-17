#!/usr/bin/env python3
"""Daily metadata audit for SEC 13F bulk-release availability.
Never invents daily institutional holdings; values remain pending until
a separately validated holdings ETL publishes them.
"""
import json, re, urllib.request
from datetime import datetime, timezone
from pathlib import Path
from html.parser import HTMLParser

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"data/latest.json"
SEC_URL="https://www.sec.gov/data-research/sec-markets-data/form-13f-data-sets"
class Links(HTMLParser):
    def __init__(self): super().__init__(); self.links=[]; self.current=None
    def handle_starttag(self,tag,attrs):
        if tag=="a":self.current=dict(attrs).get("href")
    def handle_data(self,data):
        if self.current and "13F" in data.upper():
            self.links.append({"label":data.strip(),"href":self.current})
    def handle_endtag(self,tag):
        if tag=="a":self.current=None

def main():
    payload=json.loads(DATA.read_text(encoding="utf-8"))
    now=datetime.now(timezone.utc).isoformat(timespec="seconds")
    req=urllib.request.Request(SEC_URL,headers={"User-Agent":"VictorInvestmentOS/0.1 (https://github.com/VictorHTsai/VictorHTsai.github.io)","Accept":"text/html"})
    try:
        with urllib.request.urlopen(req,timeout=30) as res: body=res.read().decode("utf-8","replace")
        parser=Links();parser.feed(body)
        archives=[x for x in parser.links if "13F" in x["label"].upper() and ".zip" in x["href"].lower()]
        if not archives: raise ValueError("SEC page did not expose ZIP archive links")
        payload["sec_archive_check"]={"checked_at":now,"status":"ok","available_archive_count":len(archives),"newest_archive_label":archives[0]["label"],"source_url":SEC_URL}
    except Exception as exc:
        payload["sec_archive_check"]={"checked_at":now,"status":"error","detail":str(exc)[:240],"source_url":SEC_URL}
    payload["checked_at"]=now
    DATA.write_text(json.dumps(payload,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
if __name__=="__main__": main()
