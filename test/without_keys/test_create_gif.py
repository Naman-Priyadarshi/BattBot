import unittest
import pybamm
import os
from bot.plotting.create_gif import create_gif


class TestCreateGIF(unittest.TestCase):
    def setUp(self):
        self.model = {0: pybamm.lithium_ion.DFN()}
        self.batch_study = pybamm.BatchStudy(self.model)
        self.batch_study.solve([0, 3700])

    def tearDown(self):
        os.remove("plot.gif")

    def test_create_gif(self):
        create_gif(self.batch_study)
        path = "plot.gif"
        assert os.path.exists(path)


if __name__ == "__main__":
    unittest.main()