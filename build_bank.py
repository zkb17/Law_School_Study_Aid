#!/usr/bin/env python3
"""Reproducibly build original law-school concept/application MCQs from authored seeds.

The output references legal sources for independent verification. These are not
extracted/copy-pasted from commercial question banks or certified exam questions.
"""
from __future__ import annotations
from collections import Counter
from pathlib import Path
import json, re, csv, random
ROOT=Path(__file__).resolve().parent
source=(ROOT/'concepts.txt').read_text(encoding='utf-8')
COURSES=[]
items={}
course=None
for n,raw in enumerate(source.splitlines(),1):
 line=raw.strip()
 if not line or (line.startswith('#') and not line.startswith('## ')):continue
 if line.startswith('## '):
  course=line[3:].strip()
  if course in items:raise ValueError(f'Duplicate course {course}')
  COURSES.append(course)
  items[course]=[]
  continue
 if course is None:raise ValueError(f'Concept without subject line {n}')
 fields=line.split(' | ')
 if len(fields)!=3:raise ValueError(f'Expected 3 columns in line {n}: {line}')
 term,clue,authority=fields
 if len(term)<3 or len(clue)<40 or len(authority)<5:raise ValueError(f'Weak entry line {n}: {line}')
 if any(term==old['term'] for old in items[course]):raise ValueError(f'Duplicate concept {course} {term}')
 items[course].append({'term':term,'clue':clue,'authority':authority})
for name, concepts in items.items():
 if len(concepts)!=10:raise ValueError(f'{name}: expected ten concepts, got {len(concepts)}')
if len(items)!=70:raise ValueError(f'Expected 70 subjects, got {len(items)}')

# A separately identifiable source for each subject when a narrower linked section
# is not available. Statute and rules links are built from citations when possible.
reference_by_course={
 'Administrative Law':'https://www.law.cornell.edu/uscode/text/5/553',
 'Evidence':'https://www.law.cornell.edu/rules/fre',
 'Business Associations':'https://www.law.cornell.edu/wex/corporation',
 'Legal Profession':'https://www.americanbar.org/groups/professional_responsibility/publications/model_rules_of_professional_conduct/',
 'Criminal Procedure':'https://www.law.cornell.edu/wex/criminal_procedure',
 'Constitutional Law II':'https://constitution.congress.gov/',
 'Federal Courts':'https://www.law.cornell.edu/wex/federal_courts',
 'Remedies':'https://www.law.cornell.edu/wex/remedy',
 'Wills & Trusts':'https://www.law.cornell.edu/wex/trust',
 'Family Law':'https://www.law.cornell.edu/wex/family_law',
 'Individual Income Tax':'https://www.law.cornell.edu/uscode/text/26',
 'Secured Transactions':'https://www.law.cornell.edu/ucc/9',
 'Bankruptcy':'https://www.law.cornell.edu/uscode/text/11',
 'Conflict of Laws':'https://www.law.cornell.edu/wex/conflict_of_laws',
 'First Amendment':'https://constitution.congress.gov/browse/amendment-1/',
 'Civil Rights Litigation':'https://www.law.cornell.edu/uscode/text/42/1983',
 'Employment Discrimination':'https://www.law.cornell.edu/uscode/text/42/2000e-2',
 'Election Law':'https://constitution.congress.gov/browse/article-1/section-4/',
 'Prison Law':'https://www.law.cornell.edu/wex/prisoners%27_rights',
 'Native American Law':'https://www.law.cornell.edu/wex/indian_law',
 'Constitutional History':'https://constitution.congress.gov/',
 'State & Local Government':'https://www.law.cornell.edu/wex/local_government',
 'Statutory Interpretation':'https://www.law.cornell.edu/wex/statutory_construction',
 'Equality Before the Law':'https://constitution.congress.gov/browse/amendment-14/',
 'Securities Regulation':'https://www.sec.gov/about/divisions-offices/division-corporation-finance/securities-act-1933',
 'Corporate Finance':'https://www.law.cornell.edu/wex/corporate_finance',
 'Mergers & Acquisitions':'https://www.law.cornell.edu/wex/mergers_and_acquisitions',
 'Business Planning':'https://www.law.cornell.edu/wex/business_organizations',
 'Business Taxation':'https://www.law.cornell.edu/uscode/text/26',
 'Payment Systems':'https://www.law.cornell.edu/ucc/3',
 'Banking & Fintech':'https://www.fdic.gov/resources/deposit-insurance/',
 'Antitrust Law':'https://www.ftc.gov/advice-guidance/competition-guidance/guide-antitrust-laws',
 'Insurance Law':'https://www.law.cornell.edu/wex/insurance',
 'Nonprofit Organizations':'https://www.irs.gov/charities-non-profits/charitable-organizations',
 'Real Estate Transactions':'https://www.law.cornell.edu/wex/real_property',
 'Pretrial Litigation':'https://www.law.cornell.edu/rules/frcp',
 'Trial Advocacy':'https://www.law.cornell.edu/rules/fre',
 'Appellate Advocacy':'https://www.law.cornell.edu/rules/frap',
 'Advanced Legal Research':'https://www.law.cornell.edu/wex',
 'Negotiation':'https://www.law.cornell.edu/wex/negotiation',
 'Mediation':'https://www.law.cornell.edu/wex/mediation',
 'Arbitration':'https://www.law.cornell.edu/uscode/text/9',
 'Client Counseling':'https://www.americanbar.org/groups/professional_responsibility/publications/model_rules_of_professional_conduct/',
 'Legal Citation & Bluebook':'https://www.law.cornell.edu/citation/',
 'Alternative Dispute Resolution':'https://www.law.cornell.edu/wex/alternative_dispute_resolution',
 'Environmental Law':'https://www.epa.gov/laws-regulations',
 'Agricultural Law':'https://www.usda.gov/topics/farming',
 'Natural Resources & Water Law':'https://www.law.cornell.edu/wex/water_law',
 'Immigration Law':'https://www.uscis.gov/laws-and-policy/legislation',
 'Employment & Labor Law':'https://www.dol.gov/general/aboutdol/majorlaws',
 'Health Law':'https://www.hhs.gov/hipaa/index.html',
 'Mental Health Law':'https://www.law.cornell.edu/wex/civil_commitment',
 'Intellectual Property':'https://www.uspto.gov/ip-policy',
 'Patent Law':'https://www.uspto.gov/web/offices/pac/mpep/',
 'Copyright Law':'https://www.copyright.gov/title17/',
 'Privacy & Cyberlaw':'https://www.ftc.gov/business-guidance/privacy-security',
 'International Law':'https://legal.un.org/ilc/',
 'International Human Rights':'https://www.ohchr.org/en/instruments-and-mechanisms/international-human-rights-law',
 'Space Law':'https://www.unoosa.org/oosa/en/ourwork/spacelaw/treaties.html',
 'National Security Law':'https://constitution.congress.gov/',
 'Sports Law':'https://www.law.cornell.edu/wex/sports_law',
 'Estate Planning':'https://www.law.cornell.edu/wex/estate_planning',
 'Contracts':'https://www.law.cornell.edu/wex/contract',
 'Torts':'https://www.law.cornell.edu/wex/tort',
 'Civil Procedure':'https://www.law.cornell.edu/rules/frcp',
 'Criminal Law':'https://www.law.cornell.edu/wex/criminal_law',
 'Property':'https://www.law.cornell.edu/wex/property',
 'Constitutional Law I':'https://constitution.congress.gov/',
 'Legal Research Foundations':'https://www.law.cornell.edu/wex',
 'MPRE Review':'https://www.americanbar.org/groups/professional_responsibility/publications/model_rules_of_professional_conduct/',
}
assert set(reference_by_course)==set(items),(set(items)-set(reference_by_course),set(reference_by_course)-set(items))

def source_url(citation, course):
    m=re.search(r'\b(\d{1,2})\s+U\.S\.C\.\s*§{1,2}\s*(\d+[a-zA-Z-]*)',citation)
    if m:return f'https://www.law.cornell.edu/uscode/text/{m.group(1)}/{m.group(2)}'
    m=re.search(r'\bFRE\s*(\d{3})',citation)
    if m:return f'https://www.law.cornell.edu/rules/fre/rule_{m.group(1)}'
    m=re.search(r'Fed\. R\. Evid\.\s*(\d{3})',citation)
    if m:return f'https://www.law.cornell.edu/rules/fre/rule_{m.group(1)}'
    m=re.search(r'Fed\. R\. Civ\. P\.\s*(\d+(?:\.\d+)?)',citation)
    if m:return f'https://www.law.cornell.edu/rules/frcp/rule_{m.group(1)}'
    m=re.search(r'Fed\. R\. App\. P\.\s*(\d+)',citation)
    if m:return f'https://www.law.cornell.edu/rules/frap/rule_{m.group(1)}'
    m=re.search(r'\bUCC\s*§{1,2}\s*([1-9])-([0-9]{3})',citation)
    if m:return f'https://www.law.cornell.edu/ucc/{m.group(1)}/{m.group(1)}-{m.group(2)}'
    m=re.search(r'\b11 U\.S\.C\.\s*ch\.\s*(\d+)',citation)
    if m:return f'https://www.law.cornell.edu/uscode/text/11/chapter-{m.group(1)}'
    return reference_by_course[course]

bank=[]
for course in COURSES:
 concepts=items[course]
 for i,target in enumerate(concepts):
  # Deliberately choose close alternatives within each 5-concept cluster.
  cluster=range(0,5) if i<5 else range(5,10)
  others=[j for j in cluster if j!=i]
  rnd=random.Random(95173 + COURSES.index(course)*101+i)
  rivals=rnd.sample(others,3)
  options=[target]+[concepts[j] for j in rivals]
  correctSlot=(i+COURSES.index(course))%4
  if correctSlot:
   options.insert(correctSlot,options.pop(0))
  # Multiple stem phrasings with no answer term in the prompt.
  intros=[
   'Which legal doctrine or rule best addresses this fact pattern?',
   'Identify the most directly relevant legal concept.',
   'Which principle is described most precisely by these facts?',
   'A law-school problem presents the following situation. What is the best issue label?',
   'What doctrine would you analyze first on these facts?'
  ]
  stem=f'{intros[(i+COURSES.index(course))%len(intros)]} {target["clue"]}'
  answer=next(k for k,x in enumerate(options) if x is target)
  feedback=[]
  for k,x in enumerate(options):
   if x is target:
    fb=(f'Correct — {x["term"]}. {x["clue"]} '
        f'Authority: {x["authority"]}.')
   else:
    fb=(f'Not this doctrine. {x["term"]} concerns a different issue: {x["clue"]} '
        f'Here, the better fit is {target["term"]} ({target["authority"]}).')
   feedback.append(fb)
  bank.append({
   'id':f'expand-{COURSES.index(course)+1:02}-{i+1:02}',
   'course':course,
   'topic':target['term'],
   'difficulty': [1,1,2,2,2,2,2,3,3,3][i],
   'stem':stem,
   'options':[x['term'] for x in options],
   'answer':answer,
   'feedback':feedback,
   'authority':target['authority'],
   'sourceUrl':source_url(target['authority'],course),
   'source':'builtin',
   'kind':'mcq',
   'questionStyle':'original_concept_application',
   'reviewStatus':'draft-not-faculty-reviewed',
   'ruleSystem':'U.S. federal/model rules or general common law; jurisdiction differences may apply',
  })

assert len(bank)==700
assert len({q['id'] for q in bank})==len(bank)
assert len({q['stem'] for q in bank})==len(bank)
assert all(len(set(q['options']))==4 for q in bank)
assert all(0<=q['answer']<4 and len(q['feedback'])==4 for q in bank)
assert all(q['sourceUrl'].startswith('https://') for q in bank)
assert all(len(q['stem'])>75 for q in bank)
json_text=json.dumps(bank,ensure_ascii=False,indent=2)
(ROOT/'expanded-question-bank.json').write_text(json_text+'\n',encoding='utf-8')
(ROOT/'expanded-bank.js').write_text('/* 700 original supplemental MCQs. Source citations are verification starting points, not faculty review. */\n'
  'BUILTIN_QUESTIONS.push(...'+json.dumps(bank,ensure_ascii=False,separators=(',',':'))+');\n',encoding='utf-8')
with (ROOT/'expanded-question-bank.csv').open('w',newline='',encoding='utf-8-sig') as h:
 w=csv.writer(h)
 w.writerow(['ID','Course','Topic','Difficulty','Question','Choice A','Choice B','Choice C','Choice D','Correct choice','Explanation A','Explanation B','Explanation C','Explanation D','Authority','Reference URL','Review status'])
 for q in bank:
  w.writerow([q['id'],q['course'],q['topic'],q['difficulty'],q['stem'],*q['options'],'ABCD'[q['answer']],*q['feedback'],q['authority'],q['sourceUrl'],q['reviewStatus']])
print('Built',len(bank),'supplemental original MCQs across',len(COURSES),'courses.')
print('Citation references by host:',Counter(re.match(r'https://([^/]+)',q['sourceUrl']).group(1) for q in bank))
print('Difficulty:',Counter(q['difficulty'] for q in bank))
