from BSTestRunner import BSTestRunner
import unittest
from time import strftime



discover = unittest.defaultTestLoader.discover(r'E:\code\python\比赛\传智杯\初赛\接口测试', pattern='test*.py')

if __name__ == '__main__':
    report_dir = r'E:\code\python\比赛\传智杯\初赛\接口测试\测试报告'
    now = strftime('%Y-%m-%d %H-%M-%S')
    filename = report_dir + now + 'result.html'
    fp = open(filename, 'wb')
    runner = BSTestRunner(stream=fp, title='mqt_测试报告', description='mqt_测试用例执行情况')
    runner.run(discover)
    fp.close()
    