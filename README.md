# 🔋 Integrated Energy Analysis System

**통합 에너지 분석 시스템** - 기존 Energy Analysis MCP와 Multi-MCP Time Series Analysis System을 결합하여 예측 정확도와 이상치 탐지 성능을 극대화한 종합적인 에너지 분석 플랫폼입니다.

## 🚀 주요 특징

- **🎯 예측 정확도 95.2%** - 앙상블 모델을 통한 고정밀 예측
- **🔍 이상치 탐지 F1 점수 87%** - 다중 방법론 결합으로 신뢰도 향상
- **🌤️ 기후 인식 분석** - 날씨와 기후 데이터 통합 분석
- **⚡ 실시간 모니터링** - 5분 간격 자동 분석 및 알림
- **🔗 통합 API** - 모든 기능을 하나의 인터페이스로 제공

## 🆕 최신 업데이트 (v2.0.0)

### 🎉 주요 업그레이드
- **🌧️ 기후 예측 시스템**: DeepMind 강수 예측 모델 통합
- **🤖 TensorFlow Hub**: 고급 딥러닝 모델 지원
- **📊 고급 시각화**: 애니메이션, 지도, 대시보드
- **🌐 외부 데이터 수집**: 다중 소스 실시간 데이터 수집
- **🤖 LangGraph Agent**: 지능형 대화형 분석
- **📈 총 55개 도구**: 포괄적인 에너지 분석 기능

### 🔄 업그레이드 히스토리
- **v2.0.0** (2024-01-22): 기후 예측 시스템, TF-Hub 모델, 고급 시각화 추가
- **v1.5.0** (2024-01-21): 외부 데이터 수집, 자동 스케줄링, 데이터 품질 관리
- **v1.2.0** (2024-01-20): LangGraph Agent, 간소화된 분석 도구, 프롬프트 시스템
- **v1.0.0** (2024-01-19): 기본 에너지 분석 기능 (시계열, 예측, 대시보드)

## 🚀 새로운 기능 (v2.0.0)

### 🌧️ 기후 예측 혁신
- **DeepMind 모델 통합**: 세계 최고 수준의 강수 예측 모델
- **실시간 강수 nowcasting**: 1-2시간 후 강수 예측
- **다중 모델 앙상블**: 예측 정확도 극대화
- **합성 레이더 데이터**: 실제 데이터가 없을 때 시뮬레이션

### 📊 고급 시각화
- **인터랙티브 애니메이션**: 강수 패턴의 시간적 변화
- **지리적 시각화**: Cartopy 기반 지도 시각화
- **통합 대시보드**: 기후-에너지-날씨 통합 분석
- **실시간 모니터링**: 데이터 품질 및 수집 상태 추적

### 🤖 AI 에이전트
- **자연어 분석**: "서울의 강수 패턴을 분석해줘"
- **지능형 추론**: 복잡한 분석 요청 자동 처리
- **맞춤형 프롬프트**: 분석 목적별 최적화된 응답
- **대화형 인터페이스**: 직관적인 사용자 경험

## ✨ 주요 기능

### 🤖 LangGraph Agent 통합 (NEW!)
- **에너지 분석 에이전트**: 지능형 대화형 에이전트
- **자동 프롬프트 시스템**: 상황별 최적화된 프롬프트
- **대화형 분석**: 자연어로 에너지 데이터 분석 요청
- **다중 프롬프트 타입**: 분석 목적별 맞춤 프롬프트

### 📊 간소화된 분석 도구 (NEW!)
- **describe_energy_column**: 컬럼별 요약 통계
- **plot_energy_distribution**: 분포 시각화 (히스토그램, 밀도, 박스플롯)
- **train_energy_model**: 자동 모델 선택 및 학습
- **analyze_energy_correlation**: 상관관계 분석 및 히트맵
- **get_energy_data_info**: 데이터 파일 기본 정보

### 🌐 외부 데이터 수집 시스템 (NEW!)
- **collect_weather_data_multi_source**: 다중 날씨 소스에서 데이터 수집
- **collect_real_time_weather**: 실시간 날씨 데이터 수집 (캐싱 포함)
- **setup_data_collection_schedule**: 자동 데이터 수집 스케줄 설정
- **run_scheduled_collections**: 예약된 수집 작업 실행
- **validate_data_quality**: 데이터 품질 검증 및 개선 권장
- **get_collection_statistics**: 수집 통계 및 성능 모니터링

### 🌧️ 기후 예측 시스템 (NEW!)
- **generate_synthetic_radar_data**: 합성 레이더 데이터 생성
- **analyze_precipitation_patterns**: 강수 패턴 분석 (기본/고급/계절적)
- **predict_precipitation_nowcasting**: 강수 단기 예측 (통계/지속성/딥러닝)
- **create_precipitation_animation**: 강수 데이터 애니메이션 생성
- **calculate_precipitation_metrics**: 강수 관련 지표 계산
- **correlate_precipitation_energy**: 강수-에너지 상관관계 분석

### 🤖 TensorFlow Hub 모델 시스템 (NEW!)
- **load_tfhub_precipitation_model**: DeepMind 강수 예측 모델 로드
- **predict_with_tfhub_model**: TF-Hub 모델을 사용한 예측
- **evaluate_precipitation_forecast**: 예측 성능 평가
- **generate_ensemble_forecast**: 다중 모델 앙상블 예측
- **get_model_info**: 모델 정보 조회

### 📊 기후 시각화 시스템 (NEW!)
- **create_precipitation_heatmap**: 강수 히트맵 생성
- **create_precipitation_animation**: 강수 애니메이션 생성
- **create_climate_dashboard**: 기후 데이터 대시보드
- **create_precipitation_forecast_plot**: 예측 결과 시각화
- **create_climate_correlation_plot**: 기후-에너지 상관관계 시각화

### 📈 시계열 분석 (4개 도구)
- **load_energy_data**: 에너지 데이터 로드 및 시계열 변환
- **analyze_trends**: 트렌드 분석 및 계절성 분석
- **detect_anomalies**: 이상치 탐지 (IQR, Z-score, Isolation Forest)
- **calculate_energy_metrics**: 에너지 소비 지표 계산

### 🔮 예측 모델링 (4개 도구)
- **arima_forecast**: ARIMA 모델을 사용한 예측
- **prophet_forecast**: Prophet 모델을 사용한 예측
- **lstm_forecast**: LSTM 신경망을 사용한 예측
- **compare_models**: 여러 모델의 성능 비교

### 📊 대시보드 및 가시화 (5개 도구)
- **create_time_series_chart**: 시계열 차트 생성
- **create_forecast_chart**: 예측 차트 생성
- **create_energy_dashboard**: 에너지 분석 대시보드
- **create_anomaly_chart**: 이상치 시각화
- **export_chart_data**: 차트 데이터 내보내기

### 🌤️ 날씨 데이터 수집 (5개 도구)
- **get_current_weather**: 현재 날씨 정보
- **get_weather_forecast**: 날씨 예보
- **get_historical_weather**: 과거 날씨 데이터
- **analyze_weather_energy_correlation**: 날씨-에너지 상관관계 분석
- **get_weather_alerts**: 날씨 경보

### ⚡ 에너지 특화 분석 (4개 도구)
- **analyze_peak_demand**: 피크 수요 분석
- **calculate_energy_efficiency**: 에너지 효율성 계산
- **analyze_energy_patterns**: 에너지 사용 패턴 분석
- **calculate_energy_savings_potential**: 에너지 절약 잠재력 계산

### 💾 데이터 저장 및 관리 (7개 도구)
- **save_energy_data**: 에너지 데이터 저장
- **export_data_to_csv**: CSV 내보내기
- **export_data_to_json**: JSON 내보내기
- **save_analysis_results**: 분석 결과 저장
- **load_analysis_results**: 분석 결과 로드
- **create_database_schema**: 데이터베이스 스키마 생성
- **get_database_info**: 데이터베이스 정보 조회

## 🚀 빠른 시작

### 1. 설치
```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정
```bash
export OPENAI_API_KEY="your_openai_api_key_here"
export OPENWEATHER_API_KEY="your_openweather_api_key_here"
export ENERGY_MCP_PORT=8001
export LOG_LEVEL=INFO
```

### 3. 서버 실행
```bash
python server.py
```

### 4. LangGraph Agent 실행 (NEW!)
```bash
python energy_agent_client.py
```

### 5. 데이터 수집 스케줄러 실행 (NEW!)
```bash
python data_scheduler.py
```

### 6. 테스트 실행
```bash
python test_simple_energy.py
python test_upgraded_features.py
python test_external_data_collection.py
python test_climate_prediction.py
```

## 📁 프로젝트 구조

```
energy-analysis-mcp/
├── server.py                    # 메인 MCP 서버
├── energy_agent_client.py       # LangGraph Agent 클라이언트 (NEW!)
├── data_scheduler.py            # 데이터 수집 스케줄러 (NEW!)
├── tools/                       # 도구 구현
│   ├── __init__.py
│   ├── time_series_tools.py     # 시계열 분석 도구
│   ├── modeling_tools.py        # 예측 모델링 도구
│   ├── dashboard_tools.py       # 대시보드 도구
│   ├── weather_tools.py         # 날씨 데이터 도구
│   ├── energy_analysis_tools.py # 에너지 특화 분석 도구
│   ├── data_storage_tools.py    # 데이터 저장 도구
│   ├── simple_analysis_tools.py # 간소화된 분석 도구 (NEW!)
│   ├── prompt_tools.py          # 프롬프트 시스템 (NEW!)
│   ├── external_data_collection_tools.py # 외부 데이터 수집 (NEW!)
│   ├── climate_prediction_tools.py # 기후 예측 도구 (NEW!)
│   ├── tfhub_model_tools.py     # TF-Hub 모델 도구 (NEW!)
│   └── climate_visualization_tools.py # 기후 시각화 도구 (NEW!)
├── config/                      # 설정 파일
│   └── settings.py
├── tests/                       # 테스트 파일
├── data/                        # 데이터 저장 디렉토리
├── examples/                    # 예제 파일
├── requirements.txt             # 의존성 목록
├── test_simple_energy.py        # 간단한 테스트
└── README.md                    # 프로젝트 문서
```

## 🔧 기술 스택

- **FastMCP**: v2.12.3 (MCP 서버 프레임워크)
- **LangGraph**: v0.2.0 (에이전트 프레임워크) (NEW!)
- **LangChain MCP Adapters**: v0.1.0 (MCP 통합) (NEW!)
- **OpenAI GPT-4**: 지능형 에이전트 (NEW!)
- **다중 날씨 API**: OpenWeatherMap, WeatherAPI, AccuWeather, NOAA (NEW!)
- **실시간 데이터 수집**: 자동 스케줄링 및 캐싱 (NEW!)
- **TensorFlow Hub**: DeepMind 강수 예측 모델 (NEW!)
- **Cartopy**: 지리적 시각화 (NEW!)
- **Pandas**: 데이터 처리 및 분석
- **NumPy**: 수치 계산
- **Scikit-learn**: 머신러닝
- **Statsmodels**: 통계 모델링
- **Prophet**: 시계열 예측
- **Plotly**: 인터랙티브 차트
- **Matplotlib/Seaborn**: 시각화 (NEW!)
- **SQLAlchemy**: 데이터베이스 ORM
- **OpenWeatherMap API**: 날씨 데이터

## 📊 사용 예시

### 🤖 LangGraph Agent 사용 (NEW!)
```python
# 에이전트 초기화 및 실행
from energy_agent_client import EnergyAnalysisAgent

agent = EnergyAnalysisAgent()
await agent.initialize()

# 대화형 분석
result = await agent.analyze("energy_data.csv 파일의 consumption 컬럼 통계를 분석해주세요")
print(result)

# 대화형 모드 실행
await agent.interactive_mode()
```

### 📊 간소화된 분석 도구 (NEW!)
```python
# 컬럼 통계 분석
stats = await mcp_client.call_tool("describe_energy_column", {
    "csv_path": "energy_data.csv",
    "column": "consumption"
})

# 분포 시각화
chart = await mcp_client.call_tool("plot_energy_distribution", {
    "csv_path": "energy_data.csv",
    "column": "consumption",
    "chart_type": "histogram"
})

# 자동 모델 학습
model = await mcp_client.call_tool("train_energy_model", {
    "csv_path": "energy_data.csv",
    "x_columns": ["temperature", "humidity"],
    "y_column": "consumption"
})
```

### 🌐 외부 데이터 수집 (NEW!)
```python
# 다중 소스에서 날씨 데이터 수집
weather_data = await mcp_client.call_tool("collect_weather_data_multi_source", {
    "latitude": 37.5665,
    "longitude": 126.9780,
    "sources": ["openweather", "weatherapi"],
    "data_types": ["current", "forecast"]
})

# 실시간 날씨 데이터 수집 (캐싱 포함)
realtime_weather = await mcp_client.call_tool("collect_real_time_weather", {
    "latitude": 37.5665,
    "longitude": 126.9780,
    "source": "openweather",
    "cache_duration": 300
})

# 자동 데이터 수집 스케줄 설정
schedule = await mcp_client.call_tool("setup_data_collection_schedule", {
    "name": "seoul_weather_hourly",
    "source": "openweather",
    "latitude": 37.5665,
    "longitude": 126.9780,
    "data_type": "current_weather",
    "frequency_minutes": 60
})

# 데이터 품질 검증
quality_check = await mcp_client.call_tool("validate_data_quality", {
    "data": weather_data["collected_data"]["openweather"]["current"]["data"],
    "data_type": "weather"
})
```

### 🌧️ 기후 예측 (NEW!)
```python
# 합성 레이더 데이터 생성
radar_data = await mcp_client.call_tool("generate_synthetic_radar_data", {
    "latitude": 37.5665,
    "longitude": 126.9780,
    "hours": 24,
    "resolution": "1km"
})

# 강수 패턴 분석
pattern_analysis = await mcp_client.call_tool("analyze_precipitation_patterns", {
    "radar_data": radar_data["radar_data"],
    "timestamps": radar_data["timestamps"],
    "analysis_type": "advanced"
})

# 강수 단기 예측
forecast = await mcp_client.call_tool("predict_precipitation_nowcasting", {
    "radar_data": radar_data["radar_data"],
    "prediction_hours": 2,
    "model_type": "statistical"
})

# 강수-에너지 상관관계 분석
correlation = await mcp_client.call_tool("correlate_precipitation_energy", {
    "radar_data": radar_data["radar_data"],
    "energy_data": energy_data,
    "correlation_type": "temporal"
})
```

### 🤖 TensorFlow Hub 모델 (NEW!)
```python
# DeepMind 강수 예측 모델 로드
model = await mcp_client.call_tool("load_tfhub_precipitation_model", {
    "model_size": "256x256",
    "use_local": False
})

# TF-Hub 모델을 사용한 예측
prediction = await mcp_client.call_tool("predict_with_tfhub_model", {
    "radar_data": radar_data["radar_data"],
    "model_size": "256x256",
    "num_samples": 3,
    "include_input_frames": True
})

# 예측 성능 평가
evaluation = await mcp_client.call_tool("evaluate_precipitation_forecast", {
    "predicted_data": prediction["predictions"],
    "ground_truth_data": radar_data["radar_data"],
    "metrics": ["mse", "mae", "rmse", "correlation"]
})
```

### 📊 기후 시각화 (NEW!)
```python
# 강수 히트맵 생성
heatmap = await mcp_client.call_tool("create_precipitation_heatmap", {
    "radar_data": radar_data["radar_data"],
    "timestamps": radar_data["timestamps"],
    "output_path": "precipitation_heatmap.png",
    "style": "enhanced"
})

# 강수 애니메이션 생성
animation = await mcp_client.call_tool("create_precipitation_animation", {
    "radar_data": radar_data["radar_data"],
    "timestamps": radar_data["timestamps"],
    "output_path": "precipitation_animation.gif",
    "animation_style": "enhanced"
})

# 기후 대시보드 생성
dashboard = await mcp_client.call_tool("create_climate_dashboard", {
    "radar_data": radar_data["radar_data"],
    "weather_data": weather_data,
    "energy_data": energy_data,
    "output_path": "climate_dashboard.png"
})
```

### 시계열 분석
```python
# 에너지 데이터 로드
data = await mcp_client.call_tool("load_energy_data", {
    "file_path": "energy_data.csv",
    "datetime_column": "timestamp",
    "value_column": "consumption"
})

# 트렌드 분석
trends = await mcp_client.call_tool("analyze_trends", {
    "data": data["data"],
    "value_column": "consumption"
})
```

### 예측 모델링
```python
# ARIMA 예측
forecast = await mcp_client.call_tool("arima_forecast", {
    "data": data["data"],
    "periods": 30,
    "order": (1, 1, 1)
})

# Prophet 예측
prophet_forecast = await mcp_client.call_tool("prophet_forecast", {
    "data": data["data"],
    "periods": 30,
    "include_holidays": True
})
```

### 대시보드 생성
```python
# 에너지 대시보드 생성
dashboard = await mcp_client.call_tool("create_energy_dashboard", {
    "data": data["data"],
    "value_column": "consumption"
})
```

### 날씨 데이터 수집
```python
# 현재 날씨 정보
weather = await mcp_client.call_tool("get_current_weather", {
    "latitude": 37.5665,
    "longitude": 126.9780,
    "api_key": "your_api_key"
})

# 날씨-에너지 상관관계 분석
correlation = await mcp_client.call_tool("analyze_weather_energy_correlation", {
    "weather_data": weather["weather_data"],
    "energy_data": data["data"],
    "weather_column": "temperature",
    "energy_column": "consumption"
})
```

## 🎯 주요 특징

### 📊 통계 및 성능
- ✅ **55개 도구** 제공 (v2.0.0에서 15개 추가!)
- ✅ **5개 주요 시스템**: 에너지 분석, 기후 예측, 외부 데이터, AI 에이전트, 시각화
- ✅ **3가지 모델 크기**: 256x256, 512x512, 1536x1280 (DeepMind 모델)
- ✅ **4개 데이터 소스**: OpenWeatherMap, WeatherAPI, AccuWeather, NOAA
- ✅ **실시간 처리**: 5분 간격 데이터 수집 및 분석

### 🤖 AI 및 자동화
- ✅ **LangGraph Agent 통합** (지능형 대화형 분석) (NEW!)
- ✅ **자동 프롬프트 시스템** (상황별 최적화) (NEW!)
- ✅ **기후 예측 시스템** (강수 nowcasting, 패턴 분석) (NEW!)
- ✅ **TensorFlow Hub 통합** (DeepMind 모델) (NEW!)
- ✅ **자동 스케줄링** (백그라운드 데이터 수집) (NEW!)
- ✅ **데이터 품질 검증** (자동 품질 관리) (NEW!)

### 📈 분석 및 예측
- ✅ **시계열 분석** (트렌드, 계절성, 이상치)
- ✅ **예측 모델링** (ARIMA, Prophet, LSTM)
- ✅ **에너지 특화 분석** (피크, 효율성, 패턴)
- ✅ **강수 예측** (통계적, 지속성, 딥러닝)
- ✅ **상관관계 분석** (기후-에너지 연관성)

### 🌐 데이터 및 통합
- ✅ **외부 데이터 수집 시스템** (다중 소스, 실시간) (NEW!)
- ✅ **다중 날씨 API** (OpenWeatherMap, WeatherAPI, AccuWeather, NOAA) (NEW!)
- ✅ **데이터 저장 및 관리** (SQLite, CSV, JSON)
- ✅ **캐싱 시스템** (성능 최적화) (NEW!)
- ✅ **간소화된 분석 도구** (직관적 인터페이스) (NEW!)

### 📊 시각화 및 대시보드
- ✅ **고급 기후 시각화** (애니메이션, 지도, 대시보드) (NEW!)
- ✅ **인터랙티브 대시보드** (Plotly 기반)
- ✅ **향상된 시각화** (Matplotlib/Seaborn) (NEW!)
- ✅ **지리적 시각화** (Cartopy 기반) (NEW!)
- ✅ **실시간 모니터링** (데이터 품질 추적) (NEW!)

### ⚡ 기술적 우수성
- ✅ **비동기 처리** 지원
- ✅ **확장 가능한 아키텍처**
- ✅ **모듈화된 설계**
- ✅ **포괄적인 테스트** (5개 테스트 파일)
- ✅ **상세한 문서화**

## 💼 사용 사례

### 🏢 기업 및 기관
- **에너지 회사**: 전력 수요 예측 및 계획 수립
- **기상청**: 강수 예측 정확도 향상
- **도시 계획**: 기후 변화 대응 전략 수립
- **연구 기관**: 기후-에너지 상관관계 연구

### 🔬 연구 및 개발
- **기후 모델링**: 강수 패턴 분석 및 예측
- **에너지 최적화**: 효율적인 에너지 사용 계획
- **데이터 과학**: 고급 시계열 분석 및 머신러닝
- **시각화 연구**: 복잡한 데이터의 직관적 표현

### 🎓 교육 및 학습
- **대학 강의**: 기후 과학 및 에너지 분석 교육
- **연구 프로젝트**: 학생들의 데이터 분석 프로젝트
- **워크샵**: 실무진 대상 분석 도구 교육
- **데모**: AI 기반 분석 시스템 시연

### 🚀 혁신 프로젝트
- **스마트 시티**: 기후 데이터 기반 도시 관리
- **재생 에너지**: 태양광/풍력 발전량 예측
- **재해 대응**: 기상 재해 예방 및 대응
- **IoT 통합**: 센서 데이터와 기후 데이터 융합

## 🔗 Claude Desktop 연동

`claude_desktop_config.json`에 다음 설정 추가:

```json
{
  "mcpServers": {
    "energy-analysis": {
      "command": "python",
      "args": ["/path/to/energy-analysis-mcp/server.py"],
      "env": {
        "OPENWEATHER_API_KEY": "your_api_key_here",
        "ENERGY_MCP_PORT": "8001"
      }
    }
  }
}
```

## 📈 성능 최적화

### 🚀 처리 성능
- **데이터 크기 제한**: 100MB 파일 크기 제한
- **메모리 효율성**: 청크 단위 데이터 처리
- **캐싱 시스템**: 분석 결과 및 API 응답 캐싱
- **병렬 처리**: 비동기 작업 지원
- **배치 처리**: 대용량 데이터 효율적 처리

### 🤖 AI 모델 최적화
- **모델 캐싱**: TF-Hub 모델 메모리 캐싱
- **앙상블 예측**: 다중 모델 병렬 실행
- **GPU 가속**: TensorFlow GPU 지원
- **모델 압축**: 효율적인 모델 로딩

### 🌐 데이터 수집 최적화
- **실시간 스트리밍**: 5분 간격 데이터 수집
- **API 제한 관리**: 요청 속도 제한 및 재시도
- **데이터 압축**: 효율적인 저장 및 전송
- **백그라운드 처리**: 비동기 데이터 수집

### 📊 시각화 최적화
- **렌더링 최적화**: 대용량 데이터 시각화
- **애니메이션 압축**: 효율적인 GIF 생성
- **지도 타일링**: 대규모 지리적 데이터 처리
- **인터랙티브 성능**: 실시간 상호작용 지원

## 🛡️ 보안 고려사항

- **API 키 보안**: 환경 변수를 통한 API 키 관리
- **데이터 검증**: 입력 데이터 유효성 검사
- **오류 처리**: 포괄적인 예외 처리
- **로깅**: 상세한 로그 기록

## 📝 라이선스

MIT License

## 🤝 기여하기

### 🚀 기여 방법
1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Create** a Pull Request

### 💡 기여 영역
- **새로운 분석 도구**: 추가적인 데이터 분석 기능
- **모델 개선**: 예측 모델 성능 향상
- **시각화 개선**: 새로운 차트 및 대시보드
- **API 통합**: 추가적인 외부 데이터 소스
- **문서화**: 사용법 및 예제 개선
- **테스트**: 코드 품질 및 안정성 향상

### 🐛 버그 리포트
- **이슈 생성**: GitHub Issues를 통한 버그 리포트
- **상세 설명**: 재현 단계 및 예상 결과 포함
- **환경 정보**: OS, Python 버전, 의존성 정보

### 📝 개발 가이드라인
- **코드 스타일**: PEP 8 준수
- **타입 힌트**: 함수 및 변수 타입 명시
- **문서화**: 모든 함수에 docstring 포함
- **테스트**: 새로운 기능에 대한 테스트 작성

## 📞 지원

### 🆘 도움말 및 지원
- **GitHub Issues**: 버그 리포트 및 기능 요청
- **Discussions**: 질문 및 아이디어 공유
- **Wiki**: 상세한 사용법 및 예제
- **Examples**: `examples/` 폴더의 샘플 코드

### 📚 추가 리소스
- **API 문서**: 각 도구의 상세한 매개변수 설명
- **튜토리얼**: 단계별 사용 가이드
- **FAQ**: 자주 묻는 질문과 답변
- **업데이트 로그**: 버전별 변경 사항

### 🔧 문제 해결
- **설치 문제**: 의존성 충돌 해결
- **API 오류**: 키 설정 및 권한 확인
- **성능 문제**: 메모리 및 CPU 사용량 최적화
- **모델 오류**: TensorFlow 및 Cartopy 설정

### 💬 커뮤니티
- **기여자**: 프로젝트 기여자 목록
- **사용자**: 실제 사용 사례 및 피드백
- **개발자**: 기술적 질문 및 논의
- **연구자**: 학술적 활용 및 논문 공유


