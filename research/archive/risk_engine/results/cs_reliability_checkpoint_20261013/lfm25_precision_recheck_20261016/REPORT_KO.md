# LFM BF16 / FP8 재측정

같은 GPU2, 같은 256개 동결 요청, C128, 각 3회. 맥락 한도131072, 출력·추론8192를 유지했다.
전체 완료·꼬리 구간을 포함한 요청 응답 사용량/실측 시간이다. 별도 MoE 임의 텐서 시험은 본 요청 TPS와 구분한다.

| 설정 | 평균 API tok/s | 평균 출력·추론 tok/s | 형식 유효/응답 |
|---|---:|---:|---:|
| bf16_default | 4400.8 | 2582.7 | 659/768 |
| fp8_default | 4638.6 | 2690.7 | 649/768 |
| fp8_tuned | 4534.1 | 2639.3 | 663/768 |

원래 FP8/BF16 출력 처리량 비: 1.0418. 선택 설정: fp8_tuned.
FP8는 실제 W8A8 block 커널을 사용했다. 일반 Linear는 FlashInfer/DeepGEMM, MoE는 Triton 경로다.
양자화 제외 항목은 lm_head·embedding·router·conv 경로다. 40층 중 conv30층/attention10층이라는 구조만으로 시간 비중을 단정하지 않는다.
기존 기본 MoE 설정과 새 private 설정의 전체 요청 효과를 비교했다. 메모리 절감과 전체 처리량 증가는 별도로 보고한다.
과거 1024개/회 결과와 이번 256개/회 결과는 유한 꼬리·실행 시점이 다른 별도 캠페인이다.
원시 응답·예산·형식 무효·종료 사유를 보존했으며, 업무 성공이나 안전성을 속도 측정으로 대체하지 않는다.

## 별도 GPU 실행 추적

동일 C128 진단 구간이며, 속도 비교 평균에서는 제외했다. 아래 비율은 커널 실행시간 합의 비중이지 전체 응답시간의 비중은 아니다.
| CUDA 커널 | 실행시간 비중 | 호출 수 |
|---|---:|---:|
| fused_moe_kernel | 43.4% | 608 |
| void cutlass::device_kernel<flash::enable_sm90_or_later<flash::FlashAttnFwdSm90<flash::CollectiveMainloopFwdSm90<2, cute::tuple<cute::C<1>, cute::C<1> | 19.5% | 80 |
| void vllm::moe::moe_align_block_size_small_batch_expert_kernel<int, 256>(int const*, int*, int*, int*, int*, int, int, unsigned long, int, int, bool) | 3.9% | 304 |
| void at::native::(anonymous namespace)::distribution_elementwise_grid_stride_kernel<float, 4, at::native::templates::cuda::uniform_and_transform<float | 3.0% | 1024 |
| nvjet_sm90_tst_96x64_64x10_1x2_h_bz_TNN | 2.5% | 240 |
| void per_token_group_quant_8bit_kernel<c10::BFloat16, c10::Float8_e4m3fn, false, true, float>(c10::BFloat16 const*, void*, float*, int, int, int, floa | 2.0% | 608 |
| std::enable_if<(((8)>(0)))&&vllm::_typeConvert<c10::BFloat16>::exists, void>::type vllm::fused_add_rms_norm_kernel<c10::BFloat16, 8, true>(c10::BFloat | 1.9% | 640 |
| _topk_topp_kernel | 1.9% | 8 |
| nvjet_sm90_tst_64x8_64x16_1x4_h_bz_TNT | 1.8% | 304 |
| nvjet_sm90_tst_48x64_64x15_4x2_h_bz_TNN | 1.8% | 240 |
| void at::native::elementwise_kernel<128, 4, at::native::gpu_kernel_impl_nocast<at::native::BinaryFunctor<c10::BFloat16, c10::BFloat16, c10::BFloat16,  | 1.4% | 480 |
| nvjet_sm90_tst_256x128_64x4_2x1_v_bz_coopA_TNT | 1.3% | 8 |

실행 추적 결과: True; 오류 기록: None.

짧은 계측 구간의 커널 시간: FP8 MoE GEMM 43.4%, BF16 FlashAttention 19.9%.
FP8 적용은 실제 가중치 dtype 및 커널 선택으로 확인됐다. 전체 경로는 비양자화 attention·라우팅·활성 양자화·샘플링 등을 함께 수행한다.
이 분포와 짧은 GPU 활동 공백은 진단 자료이며, 계측하지 않은 전체 코호트의 CPU 병목이나 인과적 시간 비중으로 대체하지 않는다.
