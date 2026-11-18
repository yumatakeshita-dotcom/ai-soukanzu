import urllib.request,re,sys
sys.stdout.reconfigure(encoding='utf-8')
U={'Sequoia':'https://www.sequoiacap.com/our-companies/','Accel':'https://www.accel.com/relationships','Benchmark':'https://www.benchmark.com/portfolio/','FoundersFund':'https://foundersfund.com/portfolio/','Greylock':'https://greylock.com/portfolio/','Lightspeed':'https://lsvp.com/companies/','GeneralCatalyst':'https://www.generalcatalyst.com/portfolio','Insight':'https://www.insightpartners.com/portfolio/','Thrive':'https://thrivecapital.com/companies','a16z':'https://a16z.com/portfolio/'}
for k,u in U.items():
    try:
        h=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=30).read().decode('utf-8','replace')
        print(k,len(h),len(re.findall(r'<a ',h)),h.count('portfolio'), 'json' if '__NEXT_DATA__' in h else '')
    except Exception as e: print(k,'ERR',str(e)[:60])
