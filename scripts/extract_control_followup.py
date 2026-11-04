#!/usr/bin/env python3
"""Validate released archive digests, safely extract, verify member hashes."""
import argparse,hashlib,json,pathlib,tarfile
def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 return h.hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--destination',required=True);a=p.parse_args();dest=pathlib.Path(a.destination);repo=pathlib.Path(__file__).resolve().parents[1];art=repo/'artifacts/control_followup_20261104';manifest=json.loads((art/'PUBLIC_ARCHIVES.json').read_text())
 for archive in manifest['archives']:
  if not archive.get('needed_for_reproduction',True):continue
  path=repo/archive['repository_path'];assert digest(path)==archive['sha256'];members=None;count=0
  with tarfile.open(path,'r:gz') as t:
   for m in t:
    rel=pathlib.PurePosixPath(m.name);assert not rel.is_absolute() and '..' not in rel.parts
    if m.isdir():continue
    assert m.isfile(),m.name
    if m.name=='ARCHIVE_SHA256_MANIFEST.json':members=json.load(t.extractfile(m));continue
    out=dest.joinpath(*rel.parts);out.parent.mkdir(parents=True,exist_ok=True);data=t.extractfile(m).read()
    if out.exists():assert out.read_bytes()==data,m.name
    else:
     with out.open('xb') as f:f.write(data)
    count+=1
  if members:
   for rel,h in members.items():assert digest(dest/rel)==h,rel
  print(path.name,count,'files PASS',flush=True)
if __name__=='__main__':main()
