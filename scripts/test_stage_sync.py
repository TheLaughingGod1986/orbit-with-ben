import json, pathlib, sys, tempfile, unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import jobs  # noqa: E402
import stage_sync  # noqa: E402


def st(**states):
    return {k: {"state": v} for k, v in states.items()}


class Implied(unittest.TestCase):
    def test_upload_done_proves_every_earlier_stage_and_thumbs(self):
        got = stage_sync.implied(st(vo="done", shots="review", picture="review", edit="blocked", thumbs="review",
                                    upload="done"))
        self.assertEqual(set(got), {"topic", "script", "sources", "shots", "picture", "edit", "thumbs"})

    def test_edit_done_does_not_prove_thumbs(self):
        got = stage_sync.implied(st(picture="review", edit="done", thumbs="review"))
        self.assertIn("picture", got)
        self.assertNotIn("thumbs", got)

    def test_thumbs_done_proves_nothing(self):
        self.assertEqual(stage_sync.implied(st(picture="review", edit="review", thumbs="done")), {})

    def test_nothing_done_moves_nothing(self):
        self.assertEqual(stage_sync.implied(st(script="review", picture="doing", edit="review")), {})

    def test_skip_and_done_are_left_alone(self):
        got = stage_sync.implied(st(sources="skip", shots="done", picture="done"))
        self.assertNotIn("sources", got)
        self.assertNotIn("shots", got)

    def test_reason_names_the_proving_stage_and_ref(self):
        got = stage_sync.implied({"edit": {"state": "review"}, "upload": {"state": "done", "ref": "abc123 Private"}})
        self.assertEqual(got["edit"], "upload done (abc123 Private)")

    def test_ben_ok_proves_up_to_edit_not_thumbs_or_upload(self):
        got = stage_sync.implied(st(picture="review", edit="review", thumbs="review", upload="todo"),
                                 "Ben OK v06 (2026-10-22)")
        self.assertEqual(got["edit"], "Ben OK v06 (2026-10-22)")
        self.assertIn("picture", got)
        self.assertNotIn("thumbs", got)
        self.assertNotIn("upload", got)


class BenOks(unittest.TestCase):
    def test_only_owb_ok_verdicts(self):
        oks = stage_sync.ben_oks({"OWB-024": {"verdict": "ok", "version": "v06", "at": "2026-10-22T09:17:55Z"},
                                  "OWB-025": {"verdict": "change", "version": "v02"},
                                  "HOS-S1": {"verdict": "ok", "version": "v01"}})
        self.assertEqual(oks, {"024": "Ben OK v06 (2026-10-22)"})


class Plan(unittest.TestCase):
    def test_plan_and_apply_on_a_film_folder(self):
        with tempfile.TemporaryDirectory() as d:
            films = pathlib.Path(d) / "02_Video-Projects"
            f = films / "099_Test"
            f.mkdir(parents=True)
            (f / "status.json").write_text(json.dumps({"film": "099", "title": "", "air": "", "claims": [], "next": "",
                                                       "stages": st(picture="review", edit="done")}))
            moves = stage_sync.plan(films, {})
            self.assertEqual([(m[1], m[2]) for m in moves if m[2] == "picture"], [("099", "picture")])
            self.assertEqual(stage_sync.plan(films, {"OWB-099": {"verdict": "change"}}), moves)


class AddWarning(unittest.TestCase):
    def test_film_named(self):
        self.assertTrue(jobs.film_named("027 Short: set Related video"))
        self.assertTrue(jobs.film_named("HOS 006: master v01"))
        self.assertFalse(jobs.film_named("Backlog OWB: listing check"))
        self.assertFalse(jobs.film_named("Weekly HOS audit"))


if __name__ == "__main__":
    unittest.main()
