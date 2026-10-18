import concurrent.futures, datetime, json, pathlib, urllib.request, urllib.parse
ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = 'https://raw.githubusercontent.com/gablilli/chocomilkyX/main/'

def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'AppdbAggregate/1.0'})
    with urllib.request.urlopen(req, timeout=45) as r:
        return json.load(r), r.url

def run():
    sources, _ = fetch(BASE + 'static/global-repos.json')
    proxy = {'fastsign':'https://fastsign.dev/repo.json','stikdebug':'https://stikdebug.xyz/index.json','ish':'https://ish.app/altstore.json','oatmealdome':'https://altstore.oatmealdome.me/','thatsella':'https://alt.thatstel.la/','crystall1ne':'https://alt.crystall1ne.dev/'}
    def process(entry):
        url = entry['url']
        if url.startswith('/api/proxy?'):
            url = proxy[urllib.parse.parse_qs(urllib.parse.urlsplit(url).query)['repo'][0]]
        try:
            data, final = fetch(url)
            apps = data.get('apps', [])
            if not isinstance(apps, list) or not apps:
                raise ValueError('No apps in source')
            result = []
            for original in apps:
                app = dict(original)
                if not app.get('name') or not app.get('bundleIdentifier'):
                    continue
                for key in ['downloadURL','iconURL']:
                    if app.get(key): app[key] = urllib.parse.urljoin(final, app[key])
                app['screenshotURLs'] = [urllib.parse.urljoin(final, s) for s in app.get('screenshotURLs', []) if isinstance(s,str)]
                versions = []
                for v in app.get('versions', []):
                    v = dict(v)
                    if v.get('downloadURL') and v.get('version'):
                        v['downloadURL'] = urllib.parse.urljoin(final,v['downloadURL'])
                        versions.append(v)
                if versions:
                    app['versions'] = versions
                    latest = versions[0]
                    for key in ['version','versionDate','versionDescription','downloadURL','size']:
                        sourcekey = {'versionDate':'date','versionDescription':'localizedDescription'}.get(key,key)
                        if latest.get(sourcekey) is not None: app[key] = latest[sourcekey]
                if not app.get('downloadURL') or not app.get('version'): continue
                app.setdefault('developerName', data.get('name','Unknown'))
                app.setdefault('localizedDescription', app['name'])
                result.append(app)
            return {'url':url,'name':data.get('name',url),'apps':len(result)}, result
        except Exception as e:
            return {'url':url,'error':str(e)}, []
    apps, report, seen = [], [], set()
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
        for status, items in pool.map(process, sources['repos']):
            report.append(status)
            for app in items:
                identity = app['bundleIdentifier']
                if identity in seen: continue
                seen.add(identity)
                apps.append(app)
    if not apps: raise RuntimeError('No usable apps; refusing to overwrite repository')
    output = {'name':'Kamil — zbiorcze repo','identifier':'pl.kamil5646.appdb.aggregate','subtitle':'Źródła chocomilkyX w jednym repo','description':'Zbiorczy katalog niezależnych źródeł. Dostępność aplikacji zależy od autorów źródeł.','apps':apps,'news':[]}
    (ROOT/'repo.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
    summary = {'updatedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'appCount':len(apps),'sources':report}
    (ROOT/'status.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(summary, ensure_ascii=False,indent=2))

if __name__ == '__main__': run()
