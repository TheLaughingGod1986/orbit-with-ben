"""J2179 regressions. Synthetic media exercise real hash/probe/decode checks.
Fixture tests isolate the classification from absent production alignment/crop evidence.
"""
import copy
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import picture_qa as qa
import terminal_loop as loop


class TerminalLoop(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.tmp.name)
        cls.src = cls.root/'source.mp4'
        subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','testsrc2=size=90x160:rate=25',
                        '-t','4','-c:v','libx264','-pix_fmt','yuv420p',str(cls.src)],check=True)
        cls.vo = cls.root/'vo.txt'; cls.vo.write_text('locked VO synthetic bytes')
        cls.words = cls.root/'words.json'
        cls.words.write_text(json.dumps({'vo_sha256':loop.digest(cls.vo), 'words':[{'end':22.5}]}))
        cls.rule = cls.root/'prescription.md'; cls.rule.write_text('Synthetic prescribed terminal return.')

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def setup_recipe(self):
        framing = dict(offset=0., crop=[0,0,90,160], output=[90,160])
        def cut(t0,t1,src,row):
            return dict(timeline_in=t0,timeline_out=t1,source=str(src),row=row,
                        framing=copy.deepcopy(framing),upscale=1.,video=True,spoken='')
        body = self.root/'other.mp4'
        body.write_bytes(b'distinct synthetic body identity')
        cuts=[cut(0,2,self.src,'open'),cut(2,23,body,'body'),cut(23,24,self.src,'tail')]
        cuts[-1]['role']='prescribed_terminal_loop'
        ev=lambda p:dict(path=str(p),sha256=loop.digest(p))
        d=dict(version=1,format='short',cut=2,duration=24,last_vo_word=22.5,
               source=ev(self.src),words=ev(self.words),vo=ev(self.vo),prescription=ev(self.rule),
               source_in=0.,source_out=1.,framing={k:v for k,v in framing.items() if k!='offset'})
        return cuts,d

    def test_real_preflight_and_legacy_optout(self):
        cuts,d=self.setup_recipe(); r=loop.validate(cuts,d)
        self.assertEqual(r['status'],'source_preflight',r)
        self.assertEqual(r['eligible_cut'],2)
        self.assertTrue(qa.reuse_checks(cuts)[2][0])
        self.assertEqual(qa.reuse_checks(cuts,r['eligible_cut'])[2][0],[])
        self.assertIn('rendered pixel/loop checks',r['pending'])
        self.assertEqual(len(qa.source_checks(cuts,{},r)),3)

    def test_invalid_contracts_fail_closed(self):
        cases = {
          'extra return':lambda c,d:d.update(returns=[0,2]),
          'boolean version':lambda c,d:d.update(version=True),
          'body row':lambda c,d:d.update(cut=1),
          'multiple roles':lambda c,d:c[0].update(role='prescribed_terminal_loop'),
          'no role':lambda c,d:c[-1].pop('role'),
          'false role':lambda c,d:c[-1].update(role='body'),
          'over one second':lambda c,d:(c[-1].update(timeline_in=22.9), c[1].update(timeline_out=22.9)),
          'VO overlap':lambda c,d:d.update(last_vo_word=23.1),
          'wrong hash':lambda c,d:d['source'].update(sha256='0'*64),
          'wrong source':lambda c,d:c[-1].update(source=__file__),
          'framing mismatch':lambda c,d:c[-1]['framing'].update(crop=[1,0,89,160]),
          'missing framing':lambda c,d:c[-1]['framing'].pop('crop'),
          'missing evidence':lambda c,d:d.pop('prescription'),
          'wrong word hash':lambda c,d:d['words'].update(sha256='0'*64),
          'under 22 seconds':lambda c,d:d.update(duration=21),
          'wrong duration':lambda c,d:d.update(duration=60),
          'duration mismatch':lambda c,d:d.update(duration=25),
          'negative offset':lambda c,d:d.update(source_in=-1),
          'out of range':lambda c,d:d.update(source_out=40),
          'bad interval':lambda c,d:d.update(source_out=.5),
          'NaN':lambda c,d:d.update(source_in=float('nan')),
          'infinity':lambda c,d:c[-1]['framing'].update(offset=float('inf')),
          'boolean number':lambda c,d:d.update(source_in=False),
          'source offset mismatch':lambda c,d:c[-1]['framing'].update(offset=1),
          'spoken tail':lambda c,d:c[-1].update(spoken='unfinished speech'),
          'timeline gap':lambda c,d:c[1].update(timeline_in=2.5),
          'long format':lambda c,d:d.update(format='long'),
          'wrong crop bounds':lambda c,d:d['framing'].update(crop=[0,0,1000,160]),
        }
        for name,edit in cases.items():
            with self.subTest(name=name):
                c,d=self.setup_recipe(); edit(c,d); r=loop.validate(c,d)
                self.assertIsNone(r['eligible_cut'],r)
                self.assertEqual(r['status'],'invalid')
                self.assertTrue(r['errors'])


    def test_reviewed_ok_cannot_waive_reuse_or_contract(self):
        rows=[dict(source='x',offset=0,fail=['reuse: repeat','terminal loop: invalid'],warn=[])]
        qa.apply_reviewed(rows,{'x':dict(kinds=['reuse','terminal loop'],note='waive')},protect_reuse=True)
        self.assertEqual(len(rows[0]['fail']),2)

    def test_within_run_replay_and_body_quality_remain(self):
        c,d=self.setup_recipe(); c[-2]['source']=str(self.src)
        r=loop.validate(c,d)
        self.assertEqual(r['eligible_cut'],2)
        self.assertTrue(any('replays frames' in e for e in qa.reuse_checks(c,2)[2][0]))
        c,d=self.setup_recipe(); c[-1]['upscale']=3
        rows=qa.source_checks(c,{qa.stem(self.src):'Computer reconstruction'},loop.validate(c,d))
        self.assertTrue(any('sharpness' in e for e in rows[-1]['fail']))
        self.assertTrue(any('kind of picture' in e for e in rows[-1]['fail']))

    def test_optin_body_alias_still_repeats(self):
        c,d=self.setup_recipe()
        alias=self.root/'copy.mp4'; alias.write_bytes(self.src.read_bytes())
        c.insert(2,copy.deepcopy(c[0])); c[1]['timeline_out']=21
        c[2].update(timeline_in=21,timeline_out=23,source=str(alias),row='body_repeat')
        d['cut']=3
        r=loop.validate(c,d)
        rows=qa.source_checks(c,{},r)
        self.assertTrue(any('same stretch' in e for e in rows[2]['fail']))
        self.assertEqual(r['eligible_cut'],3)

    def test_missing_or_unreadable_body_source_fails_without_review_override(self):
        for kind in ('absent', 'broken_link', 'directory', 'unreadable'):
            with self.subTest(kind=kind):
                c,d=self.setup_recipe()
                path=self.root/('source_'+kind)
                if kind == 'broken_link' and not path.is_symlink():
                    path.symlink_to(self.root/'absent_target')
                if kind == 'directory': path.mkdir(exist_ok=True)
                c[1]['source']=str(path if kind != 'unreadable' else self.src)
                original=loop.digest
                def guarded(p):
                    if kind == 'unreadable' and Path(p).resolve() == self.src.resolve():
                        raise PermissionError('synthetic unreadable source')
                    return original(p)
                r=loop.validate(c,d)
                with patch.object(loop,'digest',side_effect=guarded):
                    rows=qa.source_checks(c,{},r)
                qa.apply_reviewed(rows,{c[1]['source']:dict(kinds=['terminal loop'],note='waive')},True)
                self.assertTrue(any('cannot verify reuse identity' in e for e in rows[1]['fail']))

    def test_invalid_body_offsets_cannot_downgrade_adjacent_footage(self):
        for bad in ('missing', None, float('nan'), float('inf'), -1, True, 'zero'):
            with self.subTest(offset=bad):
                c,d=self.setup_recipe()
                # All adjacent rows use identical footage. The terminal return
                # must still fail within-run replay against the opening.
                c[1]['source']=str(self.src)
                if bad == 'missing': c[1]['framing'].pop('offset')
                else: c[1]['framing']['offset']=bad
                rows=qa.source_checks(c,{},loop.validate(c,d))
                self.assertTrue(any('finite nonnegative' in e for e in rows[1]['fail']))
                self.assertTrue(any('replays frames' in e for e in rows[2]['fail']))
        c,d=self.setup_recipe(); c[1]['source']=str(self.src)
        rows=qa.source_checks(c,{},loop.validate(c,d))
        self.assertTrue(any('replays frames' in e for e in rows[1]['fail']))
        self.assertTrue(any('replays frames' in e for e in rows[2]['fail']))

    def test_optin_legitimate_still_and_optout_missing_sources_unchanged(self):
        c,d=self.setup_recipe()
        still=self.root/'still.jpg'; still.write_bytes(b'distinct still bytes')
        c[1].update(source=str(still),video=False,framing={})
        rows=qa.source_checks(c,{},loop.validate(c,d))
        self.assertEqual(rows[1]['fail'],[])
        c[1]['source']=str(self.root/'not_here.mp4')
        c[1].update(video=True,framing={})
        self.assertEqual(qa.source_checks(c,{})[1]['fail'],[])

    def test_alignment_and_bounds(self):
        for end in (23.1, float('nan'), -1):
            c,d=self.setup_recipe()
            p=self.root/'bad_words.json'
            p.write_text(json.dumps({'vo_sha256':loop.digest(self.vo),'words':[{'end':end}]}))
            d.update(words=dict(path=str(p),sha256=loop.digest(p)),last_vo_word=end)
            self.assertIsNone(loop.validate(c,d)['eligible_cut'])
        c,d=self.setup_recipe(); c[0]['timeline_out']=5; c[1]['timeline_in']=5
        self.assertIsNone(loop.validate(c,d)['eligible_cut'])

    def test_real_render_correspondence_and_wrong_picture(self):
        c,d=self.setup_recipe(); render=self.root/'render.mp4'
        # Real source repeated for synthetic 24s output: only sample correspondence
        # is under test here, not all-body QA or production approval.
        subprocess.run(['ffmpeg','-v','error','-y','-stream_loop','-1','-i',str(self.src),
                        '-t','24','-vf',"setpts=PTS-STARTPTS",'-c:v','libx264',str(render)],check=True)
        # Tail at 23s in a 4s repeating source is wrong and must fail.
        self.assertIsNone(loop.validate(c,d,render)['eligible_cut'])
        good=self.root/'good.mp4'
        subprocess.run(['ffmpeg','-v','error','-y','-i',str(self.src),'-filter_complex',
          '[0:v]split[a][b];[a]trim=duration=1,setpts=PTS-STARTPTS,loop=loop=22:size=25:start=0[x];'
          '[b]trim=duration=1,setpts=PTS-STARTPTS[y];[x][y]concat=n=2:v=1:a=0',
          '-t','24','-c:v','libx264',str(good)],check=True)
        r=loop.validate(c,d,good)
        self.assertEqual(r['status'],'rendered_correspondence',r)
        self.assertIn('samples do not establish seamless motion',r['pending'][0])

    def test_cli_preflight_is_not_pass_and_invalid_is_fail(self):
        c,d=self.setup_recipe()
        paths=[]
        for name,data in [('cuts',c),('declaration',d)]:
            p=self.root/(name+'.json');p.write_text(json.dumps(data)); paths.append(str(p))
        args=['--cuts',paths[0],'--terminal-loop',paths[1],'--out-dir',str(self.root/'report')]
        self.assertEqual(qa.main(args),2)
        report=json.loads((self.root/'report/picture_qa.json').read_text())
        self.assertEqual(report['verdict'],'PREFLIGHT')
        self.assertEqual(len(report['rows']),3)
        d.pop('source');Path(paths[1]).write_text(json.dumps(d))
        self.assertEqual(qa.main(args),1)

    def test_j2169_complete_cut_lists_preserve_body_failures(self):
        expected={'B':['S04','S05'],'C':['S05']}
        for label,body in expected.items():
            c=json.loads((Path(__file__).parent/'fixtures/terminal_loop'/f'Short_{label}_cuts.json').read_text())
            self.assertEqual([c[k]['row'] for k,v in qa.reuse_checks(c).items() if v[0]],body+['loop_tail'])
            # A completed evidence contract may classify ONLY the final loop.
            # Original fixture has no crop/alignment contract and is not approved.
            self.assertEqual([c[k]['row'] for k,v in qa.reuse_checks(c,len(c)-1).items() if v[0]],body)
            self.assertEqual(loop.validate(c,{})['status'],'invalid')
            # Complete only synthetic framing/alignment/source evidence to exercise
            # structural eligibility, without certifying the real production crop.
            completed=copy.deepcopy(c); _,d=self.setup_recipe()
            opening_source=completed[0]['source']
            sources={opening_source: str(self.src)}
            for row in completed:
                original=row['source']
                if original not in sources:
                    local=self.root/('fixture_'+str(len(sources))+'.mp4')
                    local.write_bytes(original.encode())
                    sources[original]=str(local)
                row['source']=sources[original]
            for row in (completed[0],completed[-1]):
                row['framing']=dict(offset=0.,**d['framing'])
            completed[-1]['role']='prescribed_terminal_loop'
            d.update(cut=len(completed)-1,duration=completed[-1]['timeline_out'])
            result=loop.validate(completed,d)
            self.assertEqual(result['eligible_cut'],len(completed)-1,result)
            rows=qa.source_checks(completed,{},result)
            self.assertEqual([r['row'] for r in rows if r['fail']],body)


if __name__=='__main__': unittest.main()
