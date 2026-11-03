# 평균 보존 Bayesian 갱신의 새 최초 0~10회 검증

실제352회 중 평가구간320회(정상160·적대160), 16개 짝 군집. 이전 실행은 보존했다. 모든 강한 비교군 우위와 반복 연구를 고려한 7개 핵심 질문 Bonferroni 보정을 적용했다.

판정: NOT_SUPPORTED

{
  "no_update": {
    "candidate": {
      "n": 320,
      "brier": 0.11958186008758247,
      "log_loss": 0.39157179469266323
    },
    "comparator": {
      "n": 320,
      "brier": 0.11820772383078479,
      "log_loss": 0.38922655284954316
    },
    "difference": {
      "n": 320,
      "clusters": 16,
      "mean": 0.0023452418431201437,
      "row_mean": 0.0023452418431201454,
      "ci95": [
        -0.007744696682780798,
        0.01251438387629879
      ],
      "p_value": 0.6446776611694153,
      "bootstrap": 2000,
      "unit": "cluster mean, equal weight"
    }
  },
  "global_beta": {
    "candidate": {
      "n": 320,
      "brier": 0.11958186008758247,
      "log_loss": 0.39157179469266323
    },
    "comparator": {
      "n": 320,
      "brier": 0.11904142716107531,
      "log_loss": 0.39069386287818053
    },
    "difference": {
      "n": 320,
      "clusters": 16,
      "mean": 0.0008779318144827714,
      "row_mean": 0.0008779318144827703,
      "ci95": [
        -0.010898805001907133,
        0.012607372041454542
      ],
      "p_value": 0.8785607196401799,
      "bootstrap": 2000,
      "unit": "cluster mean, equal weight"
    }
  },
  "context_beta": {
    "candidate": {
      "n": 320,
      "brier": 0.11958186008758247,
      "log_loss": 0.39157179469266323
    },
    "comparator": {
      "n": 320,
      "brier": 0.11820772383078479,
      "log_loss": 0.38922655284954316
    },
    "difference": {
      "n": 320,
      "clusters": 16,
      "mean": 0.0023452418431201437,
      "row_mean": 0.0023452418431201454,
      "ci95": [
        -0.007744696682780798,
        0.01251438387629879
      ],
      "p_value": 0.6446776611694153,
      "bootstrap": 2000,
      "unit": "cluster mean, equal weight"
    }
  },
  "hier_beta": {
    "candidate": {
      "n": 320,
      "brier": 0.11958186008758247,
      "log_loss": 0.39157179469266323
    },
    "comparator": {
      "n": 320,
      "brier": 0.11904142716107531,
      "log_loss": 0.39069386287818053
    },
    "difference": {
      "n": 320,
      "clusters": 16,
      "mean": 0.0008779318144827729,
      "row_mean": 0.0008779318144827731,
      "ci95": [
        -0.010898805001907137,
        0.012607372041454543
      ],
      "p_value": 0.8785607196401799,
      "bootstrap": 2000,
      "unit": "cluster mean, equal weight"
    }
  },
  "logit_newton": {
    "candidate": {
      "n": 320,
      "brier": 0.11958186008758247,
      "log_loss": 0.39157179469266323
    },
    "comparator": {
      "n": 320,
      "brier": 0.11868695730677481,
      "log_loss": 0.38941448842220316
    },
    "difference": {
      "n": 320,
      "clusters": 16,
      "mean": 0.00215730627046018,
      "row_mean": 0.002157306270460181,
      "ci95": [
        -0.0024218308277940788,
        0.006957789844675399
      ],
      "p_value": 0.3808095952023988,
      "bootstrap": 2000,
      "unit": "cluster mean, equal weight"
    }
  },
  "bayes_calibrator": {
    "candidate": {
      "n": 320,
      "brier": 0.11958186008758247,
      "log_loss": 0.39157179469266323
    },
    "comparator": {
      "n": 320,
      "brier": 0.11805067387647028,
      "log_loss": 0.388464638184597
    },
    "difference": {
      "n": 320,
      "clusters": 16,
      "mean": 0.0031071565080663145,
      "row_mean": 0.0031071565080663145,
      "ci95": [
        -0.005689603830609062,
        0.012315980097314718
      ],
      "p_value": 0.4877561219390305,
      "bootstrap": 2000,
      "unit": "cluster mean, equal weight"
    }
  }
}
