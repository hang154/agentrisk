import argparse,concurrent.futures,gzip,hashlib,io,json,os,pathlib,tarfile,time
p=argparse.ArgumentParser();p.add_argument('--root',required=True);p.add_argument('--out',required=True);p.add_argument('--members',nargs='+',required=True);a=p.parse_args();root=pathlib.Path(a.root);dest=pathlib.Path(a.out);os.sched_setaffinity(0,set(sorted(os.sched_getaffinity(0))[:4]));start=time.time()
if dest.exists():raise FileExistsError(dest)
paths=[]
for member in a.members:
 paths.extend(sorted((root/member).rglob('*')) if (root/member).is_dir() else [root/member])
paths=[f for f in paths if f.is_file() and '__pycache__' not in f.parts];manifest={};total=0
# Bounded concurrent ordinary reads; no security/filter/permission changes.
def read(p):
 b=p.read_bytes();return p,b,hashlib.sha256(b).hexdigest()
partial=dest.with_suffix(dest.suffix+'.partial')
with partial.open('xb') as sink,gzip.GzipFile(fileobj=sink,mode='wb',compresslevel=3,mtime=0) as gz,tarfile.open(fileobj=gz,mode='w|') as tar,concurrent.futures.ThreadPoolExecutor(max_workers=16) as pool:
 pending={};it=iter(paths);exhausted=False
 while pending or not exhausted:
  while len(pending)<32 and not exhausted:
   try:q=next(it)
   except StopIteration:exhausted=True;break
   pending[pool.submit(read,q)]=q
  done,_=concurrent.futures.wait(pending,timeout=5,return_when=concurrent.futures.FIRST_COMPLETED)
  for future in done:
   pending.pop(future);q,b,h=future.result();name=str(q.relative_to(root));info=tarfile.TarInfo(name);info.size=len(b);info.mode=0o600;info.mtime=0;tar.addfile(info,io.BytesIO(b));manifest[name]=h;total+=len(b)
  status=dict(files=len(manifest),planned=len(paths),bytes=total,seconds=time.time()-start,read_concurrency=16,security_settings_unchanged=True);hp=dest.with_suffix('.progress.json');tp=hp.with_suffix('.tmp');tp.write_text(json.dumps(status));tp.replace(hp)
 mb=json.dumps(manifest,sort_keys=True).encode();info=tarfile.TarInfo('ARCHIVE_SHA256_MANIFEST.json');info.size=len(mb);tar.addfile(info,io.BytesIO(mb))
partial.rename(dest);h=hashlib.sha256(dest.read_bytes()).hexdigest();dest.with_suffix('.receipt.json').write_text(json.dumps(dict(status,archive_sha256=h,compressed_bytes=dest.stat().st_size,complete=True)))
print(json.dumps(dict(status,archive_sha256=h)))
