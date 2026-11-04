#!/usr/bin/env python3
import pathlib,sys
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from experiments.control_study_202611.independent import audit
from experiments.control_study_202611.analysis import analyze
from experiments.control_study_202611.report import report
if __name__=='__main__':audit(sys.argv[1]);analyze(sys.argv[1]);report(sys.argv[1])
