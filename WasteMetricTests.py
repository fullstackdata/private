import unittest
from WasteMetric import *

class WasteMetricTests(unittest.TestCase):

    def test_is_invalid(self):
        wmObj = WasteMetric()
        invBatch = ["2H"]
        validBatch = {'10C','10D','10H','10S', '2C', '2D', '2H', '2S', '3C', '3D',
                      '3H', '3S', '4C', '4D', '4H', '4S', '5C', '5D', '5H', '5S', '6C',
                      '6D', '6H', '6S', '7C', '7D', '7H', '7S', '8C', '8D', '8H', '8S',
                      '9C', '9D', '9H', '9S', 'AC', 'AD', 'AH', 'AS', 'JC', 'JD', 'JH',
                      'JS', 'KC', 'KD', 'KH', 'KS', 'QC', 'QD', 'QH', 'QS'}
        self.assertTrue(wmObj.isInvalid(invBatch))
        self.assertFalse(wmObj.isInvalid(validBatch))

    def test_wmDiff(self):
        wmObj = WasteMetric()
        self.assertEqual(0, wmObj.wmDiff("2H", "2H"))
        self.assertEqual(1, wmObj.wmDiff("2H", "3H"))
        self.assertEqual(2, wmObj.wmDiff("2H", "3D"))
        self.assertEqual(3, wmObj.wmDiff("2H", "3C"))
        self.assertEqual(3, wmObj.wmDiff("2H", "3S"))

    def test_wasteMetric(self):
        wmObj = WasteMetric()
        validBatch = ['AC', 'AD', 'AH', 'AS', '2C', '2D', '2H', '2S', '3C', '3D',
                      '3H', '3S', '4C', '4D', '4H', '4S', '5C', '5D', '5H', '5S', '6C',
                      '6D', '6H', '6S', '7C', '7D', '7H', '7S', '8C', '8D', '8H', '8S',
                      '9C', '9D', '9H', '9S',  '10C','10D','10H','10S','JC', 'JD', 'JH',
                      'JS', 'KC', 'KD', 'KH', 'KS', 'QC', 'QD', 'QH', 'QS']
        wm = wmObj.listWasteMetric(validBatch)[1]
        self.assertEqual(18, sum(wm))

    def test_oneSwap(self):
        wmObj = WasteMetric()
        validBatch = ['AC', 'AD', '10C', 'AS', '2C', '2D', '2H', '3C', '2S', '3D',
                  '3H', '3S', '4C', '4D', '4H', '4S', '5C', '5D', '5H', '5S', '6C',
                  '6D', '6H', '6S', '7C', '7D', '7H', '7S', '8C', '8D', '8H', '8S',
                  '9C', '9D', '9H', '9S',  'AH','10D','10H','10S','JC', 'JD', 'JH',
                  'JS', 'KC', 'KD', 'KH', 'KS', 'QC', 'QD', 'QH', 'QS']
        min_tmp_list, wm, min_wm_sum, swap1, swap2 = wmObj.oneSwap(validBatch)
        self.assertEqual(109, sum(wm))
        self.assertEqual(24, min_wm_sum)
        self.assertEqual('10C', swap1)
        self.assertEqual('AH', swap2)

    def test_twoSwap(self):
        wmObj = WasteMetric()
        validBatch = ['AC', 'AD', '10C', 'AS', '2C', '2D', '2H', '3C', '2S', '3D',
                  '3H', '3S', '4C', '4D', '4H', '4S', '5C', '5D', '5H', '5S', '6C',
                  '6D', '6H', '6S', '7C', '7D', '7H', '7S', '8C', '8D', '8H', '8S',
                  '9C', '9D', '9H', '9S',  'AH','10D','10H','10S','JC', 'JD', 'JH',
                  'JS', 'KC', 'KD', 'KH', 'KS', 'QC', 'QD', 'QH', 'QS']
        swap1, swap2, swap3, swap4 , wm, min_wm_sum_2 = wmObj.twoSwap(validBatch)
        self.assertEqual(109, wm)
        self.assertEqual(18, min_wm_sum_2)
        self.assertEqual('10C', swap1)
        self.assertEqual('AH', swap2)
        self.assertEqual('3C', swap3)
        self.assertEqual('2S', swap4)


if __name__ == '__main__':
    unittest.main()
