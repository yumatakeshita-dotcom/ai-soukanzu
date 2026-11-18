import json, os
S = os.path.dirname(os.path.abspath(__file__))
rows = [
 ['PalmerLuckey', '2026-11-12', 'China wants Jensen out, so I want him in.', '2120770412741263858'],
 ['PalmerLuckey', '2026-11-11', 'Yes! Finally! The four-wheel-drive Toyota KEI-01 is going to be built in Gibson County, Indiana.', '2120589124793241951'],
 ['mosseri', '2026-10-27', "I'm getting a lot of inbound about Instagram starting to work on longer-form video. A few things to clarify in case it's helpful", '2115195729434272172'],
 ['mosseri', '2026-10-26', 'Really enjoyed my conversation with @ColinandSamir about our recent steps into longer-form video.', '2114765740066869726'],
 ['mosseri', '2026-10-24', 'Very excited about this! Julie and Chandra are two of the very best I’ve had the opportunity to work with over the years.', '2113782944829714888'],
 ['mikeyk', '2026-11-10', 'Very fun to see the team both ship new native artifact types like sheets and whiteboards today', '2120254420105806188'],
 ['mikeyk', '2026-11-09', 'Claude Fable 5.2 and Mythos 5.2 are out today! They’re super sharp to work with.', '2119868632570462674'],
 ['mikeyk', '2026-10-21', "We're opening Claude Duet today as a research preview, starting with a waitlist.", '2112986418503110772'],
 ['karpathy', '2026-11-01', "Weekend hack: HackerTube. I was annoyed with YouTube's recommendations so I had Claude filter down 43M comments over 20 years of H", '2116957135661945283'],
 ['karpathy', '2026-11-07', 'Earlier this week Tristan published his top YouTube channels', '2119114537442189652'],
 ['ylecun', '2026-11-07', 'Reminder from 3 years ago.', '2119184445987287449'],
]
out = [[h, d, t, '/%s/status/%s' % (h, i)] for h, d, t, i in rows]
json.dump(out, open(os.path.join(S, 'xh', 'b_alumni.json'), 'w', encoding='utf-8'), ensure_ascii=False)
# 人物名の対応に足す
p = os.path.join(S, 'x_targets.json')
t = json.load(open(p, encoding='utf-8'))
have = {x['h'].lower() for x in t}
for h, n in (('mikeyk', 'Mike Krieger'), ('mosseri', 'Adam Mosseri'), ('karpathy', 'Andrej Karpathy'), ('ylecun', 'Yann LeCun'), ('kevin', 'Kevin Systrom')):
    if h.lower() not in have:
        t.append({'name': n, 'h': h})
json.dump(t, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
print('saved', len(out), len(t))
