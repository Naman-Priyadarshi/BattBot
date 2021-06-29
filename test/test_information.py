import unittest
import pybamm
from bot.information.information import information


class TestInformation(unittest.TestCase):
    def setUp(self):
        self.chemistry = pybamm.parameter_sets.Chen2020
        self.params = pybamm.ParameterValues(chemistry=self.chemistry)
        self.c_rate = (
            self.params["Nominal cell capacity [A.h]"] /
            self.params["Current function [A]"]
        )
        self.temp = self.params["Ambient temperature [K]"] - 273.15
        self.model = pybamm.lithium_ion.DFN()
        self.is_experiment = True
        self.cycle = [
            (
                "Discharge at C/10 for 10 hours or until 3.3 V",
                "Rest for 1 hour",
                "Charge at 1 A until 4.1 V",
                "Hold at 4.1 V until 50 mA",
                "Rest for 1 hour",
            )
        ]
        self.number = 3
        self.is_comparison = False
        self.param_to_vary = None

    def test_information(self):
        result = information(
            self.chemistry,
            self.model,
            self.is_experiment,
            self.cycle,
            self.number,
            self.is_comparison,
            self.param_to_vary
        )

        self.assertEqual(
            result,
            f"Summary varaibles for {self.model.name} with "
            f"{self.chemistry['citation']} parameters for the following "
            f"experiment: {str(self.cycle)} * {self.number}"
        )

        self.is_comparison = True
        self.model = {
            0: pybamm.lithium_ion.DFN(),
            1: pybamm.lithium_ion.SPM()
        }

        result = information(
            self.chemistry,
            self.model,
            self.is_experiment,
            self.cycle,
            self.number,
            self.is_comparison,
            self.param_to_vary
        )

        self.assertEqual(
            result,
            f"Comparing {self.model[0].name} and {self.model[1].name} "
            f"with {self.chemistry['citation']} parameters for the "
            f"following experiment: {self.cycle} * {self.number}"
        )

        self.model = {
            0: pybamm.lithium_ion.DFN(),
            1: pybamm.lithium_ion.SPM(),
            2: pybamm.lithium_ion.SPMe()
        }

        result = information(
            self.chemistry,
            self.model,
            self.is_experiment,
            self.cycle,
            self.number,
            self.is_comparison,
            self.param_to_vary
        )

        self.assertEqual(
            result,
            f"Comparing {self.model[0].name}, {self.model[1].name}, and "
            f"{self.model[2].name} with {self.chemistry['citation']} "
            "parameters for the following experiment: "
            f"{self.cycle} * {self.number}"
        )

        self.param_to_vary = "Current function [A]"

        result = information(
            self.chemistry,
            self.model,
            self.is_experiment,
            self.cycle,
            self.number,
            self.is_comparison,
            self.param_to_vary
        )

        self.assertEqual(
            result,
            f"{self.model[0].name} with {self.chemistry['citation']} "
            "parameters "
            f"varying {self.param_to_vary} for the following experiment: "
            f"{self.cycle} * {self.number}"
        )

        self.is_experiment = False
        self.param_to_vary = None
        self.model = {
            0: pybamm.lithium_ion.DFN(),
            1: pybamm.lithium_ion.SPM()
        }

        result = information(
            self.chemistry,
            self.model,
            self.is_experiment,
            self.cycle,
            self.number,
            self.is_comparison,
            self.param_to_vary
        )

        self.assertEqual(
            result,
            f"Comparing {self.model[0].name} and {self.model[1].name} with "
            f"{self.chemistry['citation']} parameters for a {self.c_rate} C "
            f"discharge at {self.temp}°C"
        )

        self.model = {
            0: pybamm.lithium_ion.DFN(),
            1: pybamm.lithium_ion.SPM(),
            2: pybamm.lithium_ion.SPMe()
        }

        result = information(
            self.chemistry,
            self.model,
            self.is_experiment,
            self.cycle,
            self.number,
            self.is_comparison,
            self.param_to_vary
        )

        self.assertEqual(
            result,
            f"Comparing {self.model[0].name}, {self.model[1].name}, and "
            f"{self.model[2].name} with {self.chemistry['citation']} "
            f"parameters for a {self.c_rate} C discharge at {self.temp}°C"
        )

        self.param_to_vary = "Current function [A]"

        result = information(
            self.chemistry,
            self.model,
            self.is_experiment,
            self.cycle,
            self.number,
            self.is_comparison,
            self.param_to_vary
        )

        self.assertEqual(
            result,
            f"{self.model[0].name} with {self.chemistry['citation']} "
            "parameters "
            f"varying {self.param_to_vary} for a {self.c_rate} C discharge "
            "at "
            f"{self.temp}°C"
        )


if __name__ == "__main__":
    unittest.main()
