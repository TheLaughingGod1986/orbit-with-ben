import datetime as dt
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import channel_scorecard as c
import board_publish as bp

UTC = dt.timezone.utc


def snap(through, videos, numbers):
    return {'takenAt': through+'T09:00Z', 'videos': videos,
            'analytics': {'through': through, 'lifetime': numbers}}


def film(key, fmt, day, privacy='public'):
    return {'id': key, 'format': fmt, 'publishedAt': day+'T18:00Z', 'privacy': privacy}


class CalendarMetrics(unittest.TestCase):
    def setUp(self):
        self.daily = [{'day': f'2026-12-{n:02}', 'views': 100, 'subsNet': 1} for n in range(1,32)]
        self.old = film('old', 'long', '2026-11-01')
        self.long = film('new', 'long', '2026-12-10')
        self.short = film('short', 'short', '2026-12-20')
        self.private = film('private', 'long', '2026-12-01', 'private')
        self.snaps = [snap('2026-11-30',[self.old], {'old': {'views':100,'minutes':120}}),
                      snap('2026-12-31',[self.old,self.long,self.short,self.private],
                           {'old':{'views':110,'minutes':180}, 'new':{'views':50,'minutes':120},
                            'short':{'views':1000,'minutes':10}, 'private':{'views':999,'minutes':9999}})]

    def test_exact_month_public_only_cohorts_and_formula(self):
        m = c.monthly(dt.date(2026,12,1),self.daily,self.snaps)
        self.assertEqual(m['subscribers']['value'],31)
        self.assertEqual(m['longHours']['value'],3)
        self.assertEqual(m['shortViews']['value'],1000)
        self.assertEqual(m['films']['value'],2)
        self.assertEqual(m['returnPerFilm']['value'],17)
        self.assertEqual(m['medianLong']['value'],50)
        self.assertEqual(m['medianShort']['value'],1000)
        self.assertEqual(m['subsPer1000']['value'],10)
        self.assertEqual(m['subsPer1000ShortViews']['value'],31)

    def test_missing_boundary_or_day_or_video_is_unknown(self):
        m = c.monthly(dt.date(2026,12,1), self.daily[:-1], self.snaps[1:])
        self.assertIsNone(m['subscribers']['value'])
        self.assertIsNone(m['longHours']['value'])
        self.assertEqual(m['films']['value'],2)  # independent catalogue coverage
        del self.snaps[1]['analytics']['lifetime']['short']
        m = c.monthly(dt.date(2026,12,1),self.daily,self.snaps)
        self.assertIsNone(m['shortViews']['value'])
        self.assertIsNone(m['medianShort']['value'])
        self.assertIsNone(m['subsPer1000ShortViews']['value'])

    def test_median_and_zero_denominator(self):
        self.snaps[1]['videos'] += [film('s2','short','2026-12-01')]
        self.snaps[1]['analytics']['lifetime']['s2']={'views':100,'minutes':1}
        m=c.monthly(dt.date(2026,12,1),self.daily,self.snaps)
        self.assertEqual(m['medianShort']['value'],550)
        self.assertIsNone(c.ratio(c.measure(0),c.measure(0))['value'])

    def test_real_sources_do_not_relabel_rolling_baseline(self):
        root=Path(__file__).resolve().parents[1]
        result=c.section(root,dt.datetime(2026,11,24,tzinfo=UTC))
        self.assertEqual(result['month'],'2026-10')
        self.assertEqual(result['previousMonth'],'2026-09')
        owb=result['channels'][0]
        self.assertEqual(owb['current']['subscribers']['value'],5)
        self.assertEqual(owb['current']['films']['value'],25)
        self.assertIsNone(owb['current']['longHours']['value'])
        self.assertIn('2027-02-14',owb['protection'])


class Recommendations(unittest.TestCase):
    def plan(self):
        return [{'channel':'owb','steps':[{'name':'Journey','when':'2026-12-08T18:00Z','test':{'days':14,'keep':100,'drop':20},'videoId':'real'}]},
                {'id':'studio-portfolio-2026-12','scope':'studio','steps':[{'id':'owb-counts','when':'2027-02-14T18:00Z'}]}]

    def test_live_date_overrides_plan_full_fourteen_days_and_views(self):
        snapshots=[snap('2026-12-30',[{**film('real','long','2026-12-16'),'views':55}],{})]
        tests, reason=c.protection('owb',self.plan(),dt.datetime(2026,12,30,17,59,tzinfo=UTC),snapshots)
        self.assertEqual(tests[0]['day'],14)
        self.assertEqual(tests[0]['views'],55)
        self.assertTrue(reason)
        tests,_=c.protection('owb',self.plan(),dt.datetime(2026,12,30,18,tzinfo=UTC),snapshots)
        self.assertEqual(tests,[])

    def test_private_upload_time_is_not_actual_air_time(self):
        snapshots=[snap('2026-12-10',[{**film('real','long','2026-11-16','private'),'views':0}],{})]
        tests,_=c.protection('owb',self.plan(),dt.datetime(2026,12,10,tzinfo=UTC),snapshots)
        self.assertEqual(tests[0]['day'],2)

    def test_ranking_unknown_and_ties(self):
        rows=[{'channel':s,'current':{'returnPerFilm':c.measure(v)}} for s,v in [('a',1),('b',2),('c',3)]]
        self.assertEqual(c.ranking(rows,'current'),('a','c'))
        rows[0]['current']['returnPerFilm']=c.measure(None)
        self.assertIsNone(c.ranking(rows,'current'))
        rows[0]['current']['returnPerFilm']=c.measure(2)
        self.assertIsNone(c.ranking(rows,'current'))

    def test_verdicts_protection_and_second_strike(self):
        def month(start,daily,snaps):
            score=len(snaps) or 1
            return {'month':start.strftime('%Y-%m'), 'returnPerFilm':c.measure(score),
                    'shorts':c.measure(4), 'medianShort':c.measure(100 if start.month==2 else 50),
                    'subsPer1000ShortViews':c.measure(2)}
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for n,slug in enumerate(['owb','hos','ww2'],1):
                base=root/('channels/ww2/05_Analytics' if slug=='ww2' else '05_Analytics/'+slug)/'snapshots'
                base.mkdir(parents=True)
                for j in range(n): (base/f'{j}.json').write_text('{"date":"x"}')
            (root/'studio').mkdir()
            (root/'studio/plan.json').write_text(json.dumps([{'id':'studio-portfolio-2026-12','scope':'studio','steps':[]}]))
            with patch.object(c,'monthly',side_effect=month):
                r=c.section(root,dt.datetime(2027,3,1,10,tzinfo=UTC))
                self.assertIn('stopping',r['channels'][0]['channelVerdict'])
                self.assertIn('Keep four',r['channels'][0]['shortsVerdict'])
                (root/'studio/plan.json').write_text(json.dumps(self.plan()))
                r=c.section(root,dt.datetime(2027,2,1,10,tzinfo=UTC))
                self.assertIn('keep schedule',r['channels'][0]['channelVerdict'])
                self.assertIn('while tests',r['channels'][0]['shortsVerdict'])
                r=c.section(root,dt.datetime(2027,3,1,10,tzinfo=UTC))
                self.assertIn('halving',r['channels'][0]['channelVerdict']) # February protected

    def test_publisher_wires_section_and_fails_without_blanking_board(self):
        with patch.object(bp,'wt',return_value=Path('.')), patch.object(c,'section',return_value={'channels':[]}) as call:
            board={'tracker':{'videos':[]}}
            bp.add_scorecard(board,dt.datetime(2027,1,4,tzinfo=UTC))
            self.assertIn('scorecard',board)
            call.assert_called_once()
        with patch.object(c,'section',side_effect=ValueError('bad source')):
            bp.add_scorecard(board,dt.datetime(2027,1,4,tzinfo=UTC))
            self.assertIn('U:',board['scorecard']['note'])


if __name__=='__main__': unittest.main()
