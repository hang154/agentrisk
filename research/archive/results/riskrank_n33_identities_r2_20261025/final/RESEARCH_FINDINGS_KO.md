# N33 실제 운영정책 identity 검증

원래 등록된 N33을 실제 모델 호출로 수행했다. 자연스러운4개 운영 프롬프트를 사전 고정하고, 결과 라벨을 생성기에 심지 않았다. 개발544회와 별도 identity 검증704회를 분리했다. 실제 policy는 최초 RiskRank 입력에 넣지 않았다.

판정: NOT_SUPPORTED

고정4개 운영 템플릿 혼합에서의 실험이며, 미관측 모든 스택·실제 기업에 대한 일반화나 보험요율을 의미하지 않는다. 원래 clone 실험의 N17 판정을 소급 변경하지 않는다. 정상업무 완료와 위험 상태는 별도 파일에 기록했다.

{
  "finding": "NOT_SUPPORTED",
  "cohorts": {
    "persistent": {
      "context_only": {
        "candidate": {
          "n": 320,
          "brier": 0.089535958892617,
          "log_loss": 0.30235121757334654
        },
        "comparator": {
          "n": 320,
          "brier": 0.08921227913722489,
          "log_loss": 0.3016667209086402
        },
        "difference": {
          "n": 320,
          "clusters": 8,
          "mean": 0.0006844966647063568,
          "row_mean": 0.000684496664706357,
          "ci95": [
            0.00021117586541378184,
            0.0011016099925197208
          ],
          "p_value": 0.009995002498750625,
          "bootstrap": 2000,
          "unit": "cluster mean, equal weight"
        },
        "relative_Brier_gain": -0.0036281973571624404,
        "required_relative_gain": 0.0,
        "supported_before_multiplicity": false
      },
      "no_update": {
        "candidate": {
          "n": 320,
          "brier": 0.089535958892617,
          "log_loss": 0.30235121757334654
        },
        "comparator": {
          "n": 320,
          "brier": 0.08921830575399434,
          "log_loss": 0.30167378184839144
        },
        "difference": {
          "n": 320,
          "clusters": 8,
          "mean": 0.0006774357249551115,
          "row_mean": 0.0006774357249551115,
          "ci95": [
            0.0002172146677399961,
            0.001106827134093065
          ],
          "p_value": 0.008995502248875561,
          "bootstrap": 2000,
          "unit": "cluster mean, equal weight"
        },
        "relative_Brier_gain": -0.0035604031699340865,
        "required_relative_gain": 0.0,
        "supported_before_multiplicity": false
      },
      "global_beta_fixed_population": {
        "candidate": {
          "n": 320,
          "brier": 0.089535958892617,
          "log_loss": 0.30235121757334654
        },
        "comparator": {
          "n": 320,
          "brier": 0.09208734538100667,
          "log_loss": 0.31347410289862326
        },
        "difference": {
          "n": 320,
          "clusters": 8,
          "mean": -0.011122885325276671,
          "row_mean": -0.011122885325276671,
          "ci95": [
            -0.012991137341247079,
            -0.009158287124679742
          ],
          "p_value": 0.0009995002498750624,
          "bootstrap": 2000,
          "unit": "cluster mean, equal weight"
        },
        "relative_Brier_gain": 0.027706157429486473,
        "required_relative_gain": 0.0,
        "supported_before_multiplicity": true
      },
      "logit_MAP_fixed_population": {
        "candidate": {
          "n": 320,
          "brier": 0.089535958892617,
          "log_loss": 0.30235121757334654
        },
        "comparator": {
          "n": 320,
          "brier": 0.09642887123450164,
          "log_loss": 0.3195031864610251
        },
        "difference": {
          "n": 320,
          "clusters": 8,
          "mean": -0.017151968887678583,
          "row_mean": -0.017151968887678587,
          "ci95": [
            -0.021600542873901035,
            -0.012518487722377897
          ],
          "p_value": 0.0009995002498750624,
          "bootstrap": 2000,
          "unit": "cluster mean, equal weight"
        },
        "relative_Brier_gain": 0.07148183167178247,
        "required_relative_gain": 0.0,
        "supported_before_multiplicity": true
      }
    },
    "reset_clone": {
      "context_only": {
        "candidate": {
          "n": 320,
          "brier": 0.0885738233027348,
          "log_loss": 0.29800266566772826
        },
        "comparator": {
          "n": 320,
          "brier": 0.0886947021423556,
          "log_loss": 0.2984203485573746
        },
        "difference": {
          "n": 320,
          "clusters": 8,
          "mean": -0.00041768288964631094,
          "row_mean": -0.0004176828896463109,
          "ci95": [
            -0.0026326932956484968,
            0.001129364933708616
          ],
          "p_value": 0.768615692153923,
          "bootstrap": 2000,
          "unit": "cluster mean, equal weight"
        },
        "relative_Brier_gain": 0.0013628642602213491,
        "required_relative_gain": 0.0,
        "supported_before_multiplicity": false
      },
      "no_update": {
        "candidate": {
          "n": 320,
          "brier": 0.0885738233027348,
          "log_loss": 0.29800266566772826
        },
        "comparator": {
          "n": 320,
          "brier": 0.0887402043970755,
          "log_loss": 0.298538402118581
        },
        "difference": {
          "n": 320,
          "clusters": 8,
          "mean": -0.000535736450852781,
          "row_mean": -0.0005357364508527811,
          "ci95": [
            -0.002869251074729548,
            0.0010455147968122414
          ],
          "p_value": 0.7186406796601699,
          "bootstrap": 2000,
          "unit": "cluster mean, equal weight"
        },
        "relative_Brier_gain": 0.0018749234968651746,
        "required_relative_gain": 0.0,
        "supported_before_multiplicity": false
      },
      "global_beta_fixed_population": {
        "candidate": {
          "n": 320,
          "brier": 0.0885738233027348,
          "log_loss": 0.29800266566772826
        },
        "comparator": {
          "n": 320,
          "brier": 0.0913486155543809,
          "log_loss": 0.3095441585650508
        },
        "difference": {
          "n": 320,
          "clusters": 8,
          "mean": -0.011541492897322536,
          "row_mean": -0.011541492897322536,
          "ci95": [
            -0.015453713169882706,
            -0.007185587626972992
          ],
          "p_value": 0.0009995002498750624,
          "bootstrap": 2000,
          "unit": "cluster mean, equal weight"
        },
        "relative_Brier_gain": 0.030375854464857487,
        "required_relative_gain": 0.0,
        "supported_before_multiplicity": true
      },
      "logit_MAP_fixed_population": {
        "candidate": {
          "n": 320,
          "brier": 0.0885738233027348,
          "log_loss": 0.29800266566772826
        },
        "comparator": {
          "n": 320,
          "brier": 0.0908834499153219,
          "log_loss": 0.3027045426817179
        },
        "difference": {
          "n": 320,
          "clusters": 8,
          "mean": -0.004701877013989611,
          "row_mean": -0.0047018770139896126,
          "ci95": [
            -0.01554332401113527,
            0.00972928426915919
          ],
          "p_value": 0.47876061969015493,
          "bootstrap": 2000,
          "unit": "cluster mean, equal weight"
        },
        "relative_Brier_gain": 0.025413060515847834,
        "required_relative_gain": 0.0,
        "supported_before_multiplicity": false
      }
    }
  },
  "paired_persistent_minus_reset": {
    "n": 320,
    "clusters": 8,
    "mean": 0.001102179554352668,
    "row_mean": 0.001102179554352668,
    "ci95": [
      -0.0003324525920494247,
      0.003165144261276293
    ],
    "p_value": 0.2478760619690155,
    "bootstrap": 2000,
    "unit": "cluster mean, equal weight"
  },
  "reproducibility": {
    "observed_covariance": -0.004010695187165776,
    "p_value": 0.782608695652174,
    "development_harm_rates": [
      [
        0.6470588235294118,
        0.6764705882352942,
        0.7058823529411764,
        0.6764705882352942
      ],
      [
        0.2647058823529412,
        0.4117647058823529,
        0.23529411764705882,
        0.2647058823529412
      ]
    ],
    "final_harm_rates": [
      [
        0.6818181818181819,
        0.6818181818181818,
        0.6590909090909091,
        0.7045454545454546
      ],
      [
        0.2727272727272727,
        0.2727272727272727,
        0.3409090909090909,
        0.25
      ]
    ],
    "profile_names": [
      "standard",
      "efficient",
      "inspect_first",
      "plan_verify"
    ],
    "actors": [
      "gemma",
      "gptoss"
    ],
    "permutation_unit": "whole identity profile assignment within actor x seed",
    "permutations": 2000
  },
  "joint_p_value": 0.782608695652174,
  "eight_questions_Bonferroni": 1.0,
  "operating_templates_not_new_enterprises": true,
  "original_N17_outcomes_not_reclassified": true
}
