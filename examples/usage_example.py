"""
에너지 분석 MCP 서버 사용 예시

이 파일은 에너지 분석 MCP 서버의 주요 기능들을 사용하는 방법을 보여줍니다.
"""

import asyncio
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

async def example_energy_analysis():
    """에너지 분석 예시"""
    print("🔋 에너지 분석 MCP 서버 사용 예시")
    print("=" * 50)
    
    # 1. 샘플 에너지 데이터 생성
    print("\n1. 📊 샘플 에너지 데이터 생성")
    sample_data = []
    base_time = datetime.now() - timedelta(days=30)  # 30일간의 데이터
    
    for i in range(720):  # 30일 * 24시간
        timestamp = base_time + timedelta(hours=i)
        hour = timestamp.hour
        day_of_week = timestamp.weekday()
        
        # 시간대별 패턴
        hourly_pattern = 50 * np.sin(2 * np.pi * hour / 24)
        # 주간 패턴 (주말에 더 높은 소비)
        weekly_pattern = 20 if day_of_week < 5 else 40
        # 계절성 (여름철 더 높은 소비)
        seasonal_pattern = 30 * np.sin(2 * np.pi * timestamp.timetuple().tm_yday / 365)
        # 노이즈
        noise = np.random.normal(0, 15)
        
        consumption = 100 + hourly_pattern + weekly_pattern + seasonal_pattern + noise
        temperature = 20 + 10 * np.sin(2 * np.pi * hour / 24) + np.random.normal(0, 2)
        humidity = 60 + 20 * np.sin(2 * np.pi * hour / 24) + np.random.normal(0, 5)
        
        sample_data.append({
            "datetime": timestamp.isoformat(),
            "consumption": max(0, consumption),
            "temperature": max(0, min(40, temperature)),
            "humidity": max(0, min(100, humidity))
        })
    
    print(f"✅ {len(sample_data)}개의 샘플 데이터 생성 완료")
    
    # 2. 시계열 분석 예시
    print("\n2. 📈 시계열 분석")
    print("   - 트렌드 분석: 시간에 따른 에너지 소비 패턴 분석")
    print("   - 계절성 분석: 일일/주간/월간 패턴 분석")
    print("   - 이상치 탐지: 비정상적인 소비 패턴 식별")
    print("   - 에너지 지표: 평균, 피크, 효율성 지표 계산")
    
    # 3. 예측 모델링 예시
    print("\n3. 🔮 예측 모델링")
    print("   - ARIMA: 통계적 시계열 모델")
    print("   - Prophet: Facebook의 시계열 예측 모델")
    print("   - LSTM: 딥러닝 기반 예측 모델")
    print("   - 모델 비교: 여러 모델의 성능 비교")
    
    # 4. 대시보드 생성 예시
    print("\n4. 📊 대시보드 및 가시화")
    print("   - 시계열 차트: 시간에 따른 소비량 변화")
    print("   - 예측 차트: 과거 데이터와 예측 결과 비교")
    print("   - 에너지 대시보드: 종합적인 에너지 분석")
    print("   - 이상치 차트: 이상치가 표시된 시계열")
    
    # 5. 날씨 데이터 연동 예시
    print("\n5. 🌤️ 날씨 데이터 연동")
    print("   - 현재 날씨: 실시간 날씨 정보 수집")
    print("   - 날씨 예보: 미래 날씨 예측")
    print("   - 과거 날씨: 과거 날씨 데이터")
    print("   - 상관관계 분석: 날씨와 에너지 소비의 관계")
    
    # 6. 에너지 특화 분석 예시
    print("\n6. ⚡ 에너지 특화 분석")
    print("   - 피크 수요 분석: 최대 수요 시점 및 패턴")
    print("   - 효율성 분석: 에너지 사용 효율성 평가")
    print("   - 패턴 분석: 시간대별/요일별 사용 패턴")
    print("   - 절약 잠재력: 에너지 절약 가능성 계산")
    
    # 7. 데이터 저장 및 관리 예시
    print("\n7. 💾 데이터 저장 및 관리")
    print("   - 데이터베이스 저장: SQLite 데이터베이스에 저장")
    print("   - CSV/JSON 내보내기: 다양한 형식으로 내보내기")
    print("   - 분석 결과 저장: 분석 결과를 파일로 저장")
    print("   - 데이터 로드: 저장된 데이터 불러오기")
    
    # 8. 실제 사용 시나리오
    print("\n8. 🎯 실제 사용 시나리오")
    print("   시나리오 1: 스마트 빌딩 에너지 관리")
    print("   - 실시간 에너지 소비 모니터링")
    print("   - 피크 시간대 최적화")
    print("   - 날씨 기반 에너지 예측")
    print("   - 효율성 개선 권장사항")
    
    print("\n   시나리오 2: 재생 에너지 통합")
    print("   - 태양광/풍력 발전량 예측")
    print("   - 에너지 수요 예측")
    print("   - 그리드 안정성 분석")
    print("   - 에너지 저장 최적화")
    
    print("\n   시나리오 3: 에너지 비용 최적화")
    print("   - 시간대별 요금 분석")
    print("   - 피크 수요 관리")
    print("   - 에너지 절약 계획 수립")
    print("   - ROI 분석")
    
    # 9. MCP 클라이언트 연동 예시
    print("\n9. 🔗 MCP 클라이언트 연동")
    print("   Claude Desktop 설정:")
    print("   ```json")
    print("   {")
    print('     "mcpServers": {')
    print('       "energy-analysis": {')
    print('         "command": "python",')
    print('         "args": ["/path/to/energy-analysis-mcp/server.py"],')
    print('         "env": {')
    print('           "OPENWEATHER_API_KEY": "your_api_key"')
    print("         }")
    print("       }")
    print("     }")
    print("   }")
    print("   ```")
    
    print("\n🎉 에너지 분석 MCP 서버 사용 예시 완료!")
    print("📚 자세한 사용법은 README.md를 참조하세요.")

if __name__ == "__main__":
    asyncio.run(example_energy_analysis())


