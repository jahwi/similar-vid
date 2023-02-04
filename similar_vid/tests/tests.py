import unittest
from similar_vid.similar_secs import Similar, load

file1 = "videos//inside_job//01_trimmed.mkv"
file2 = "videos//inside_job//03_trimmed.mkv"

class TestVideo(unittest.TestCase):
    def test_load_videos(self):
        inside_job = Similar(ref=file1, comp_arr=[file2])
        comparision = Similar()
        comparision.ref = load("similar_vid//tests//ref.json")
        comparision.comp = load("similar_vid//tests//comp_arr.json")

        assert(inside_job.ref == comparision.ref)
        assert(inside_job.comp == comparision.comp)
    
    def test_matching(self):
        inside_job = Similar(ref=file1, comp_arr=[file2])
        comparision = Similar()
        comparision.ref = load("similar_vid//tests//ref.json")
        comparision.comp = load("similar_vid//tests//comp_arr.json")

        inside_job.match()
        comparision.match()

        assert(inside_job.matches == comparision.matches)


if __name__ == '__main__':
    unittest.main()

