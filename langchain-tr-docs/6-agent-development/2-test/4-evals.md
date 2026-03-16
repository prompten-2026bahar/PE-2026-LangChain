# Evals

Evaluations veya kısaca **evals**, ajanın ne kadar iyi performans gösterdiğini yürütme izini değerlendirerek ölçer. Integration test'ler temel doğruluğu kontrol ederken evals; prompt, tool veya model değişikliklerinden sonra kalite düşüşlerini yakalamakta kullanılır.

Bir evaluator, ajan çıktısını ve gerekirse referans çıktıyı alıp bir skor döndürür:

```python
def evaluator(*, outputs: dict, reference_outputs: dict):
    output_messages = outputs["messages"]
    reference_messages = reference_outputs["messages"]
    score = compare_messages(output_messages, reference_messages)
    return {"key": "evaluator_score", "score": score}
```

## AgentEvals kurulumu

```bash
pip install agentevals
```

## İki temel yaklaşım

### Trajectory match

Beklenen tool call sıraları biliniyorsa hızlı, deterministik ve maliyetsiz doğrulamalar sağlar.

Desteklenen modlar:

- `strict`
- `unordered`
- `subset`
- `superset`

Örnek kullanım:

```python
evaluator = create_trajectory_match_evaluator(
    trajectory_match_mode="strict",
)
```

### LLM-as-judge

Katı bir referans beklemeden genel kaliteyi ve akıl yürütmeyi niteliksel olarak değerlendirmek için kullanılır.

## Kullanım alanı

Evals özellikle şu durumlarda yararlıdır:

- prompt değişikliklerinden sonra regresyon yakalama
- tool kullanım davranışını karşılaştırma
- ajanın yürütme yolunu kalite açısından puanlama

Bu sayfa, entegrasyon testlerinin ötesine geçip ajan davranışını daha bütünsel biçimde ölçmek için evals kullanımını anlatır.
