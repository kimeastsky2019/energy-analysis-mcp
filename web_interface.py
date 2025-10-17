#!/usr/bin/env python3
"""
연결된 Digital Experience Intelligence Platform
Health 카드와 메뉴에 기존 페이지들을 연결한 플랫폼
"""

from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from datetime import datetime
import uvicorn

# FastAPI 앱 생성
web_app = FastAPI(title="Digital Experience Intelligence Platform", version="2.0.0")

def get_available_languages():
    """사용 가능한 언어 목록 반환"""
    return ["ko", "en", "ja", "zh"]

def load_translations():
    """번역 파일 로드"""
    import json
    import os
    
    translations = {}
    locales_dir = os.path.join(os.path.dirname(__file__), 'i18n', 'locales')
    
    for lang in get_available_languages():
        try:
            with open(os.path.join(locales_dir, f'{lang}.json'), 'r', encoding='utf-8') as f:
                translations[lang] = json.load(f)
        except FileNotFoundError:
            # 기본 한국어 번역 사용
            translations[lang] = {}
    
    return translations

def t(key, lang='ko', variables=None):
    """번역 함수"""
    if variables is None:
        variables = {}
    
    translations = load_translations()
    lang_data = translations.get(lang, translations.get('ko', {}))
    
    # 점 표기법으로 중첩된 키 탐색
    keys = key.split('.')
    value = lang_data
    
    for k in keys:
        if value and isinstance(value, dict) and k in value:
            value = value[k]
        else:
            # 한국어로 폴백
            ko_data = translations.get('ko', {})
            fallback_value = ko_data
            for fallback_key in keys:
                if fallback_value and isinstance(fallback_value, dict) and fallback_key in fallback_value:
                    fallback_value = fallback_value[fallback_key]
                else:
                    return key  # 키를 찾을 수 없으면 키 자체 반환
            value = fallback_value
            break
    
    # 문자열 보간 처리
    if isinstance(value, str) and variables:
        for var_name, var_value in variables.items():
            value = value.replace(f'{{{{{var_name}}}}}', str(var_value))
    
    return value if value else key

def generate_language_selector(current_lang='ko'):
    """언어 선택기 HTML 생성"""
    languages = {
        'ko': {'name': '한국어', 'flag': '🇰🇷'},
        'en': {'name': 'English', 'flag': '🇺🇸'},
        'ja': {'name': '日本語', 'flag': '🇯🇵'},
        'zh': {'name': '中文', 'flag': '🇨🇳'}
    }
    
    buttons = []
    for code, info in languages.items():
        active_class = 'btn-primary' if code == current_lang else 'btn-outline-primary'
        buttons.append(f'''
            <a href="?lang={code}" 
               class="btn btn-sm {active_class}"
               title="{info['name']}">
                {info['flag']}
            </a>
        ''')
    
    return f'''
        <div class="language-selector">
            <div class="btn-group" role="group">
                {''.join(buttons)}
            </div>
        </div>
    '''

def generate_navigation(current_lang='ko'):
    """네비게이션 메뉴 HTML 생성"""
    return f'''
        <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
            <div class="container-fluid">
                <a class="navbar-brand" href="/?lang={current_lang}">
                    <i class="fas fa-bolt"></i> {t('title', current_lang)}
                </a>
                
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                    <span class="navbar-toggler-icon"></span>
                </button>
                
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav me-auto">
                        <li class="nav-item">
                            <a class="nav-link" href="/?lang={current_lang}">
                                <i class="fas fa-home"></i> {t('navigation.home', current_lang)}
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/data-collection?lang={current_lang}">
                                <i class="fas fa-solar-panel"></i> {t('navigation.energySupply', current_lang)}
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/data-analysis?lang={current_lang}">
                                <i class="fas fa-chart-line"></i> {t('navigation.energyDemand', current_lang)}
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/model-testing?lang={current_lang}">
                                <i class="fas fa-brain"></i> {t('navigation.modelTesting', current_lang)}
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/statistics?lang={current_lang}">
                                <i class="fas fa-cogs"></i> {t('navigation.demandControl', current_lang)}
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/health?lang={current_lang}">
                                <i class="fas fa-heartbeat"></i> {t('navigation.health', current_lang)}
                            </a>
                        </li>
                    </ul>
                    
                    <div class="navbar-nav">
                        {generate_language_selector(current_lang)}
                    </div>
                </div>
            </div>
        </nav>
    '''

@web_app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, lang: str = Query("ko", description="Language code")):
    """메인 대시보드 페이지"""
    # 언어 설정
    if lang not in get_available_languages():
        lang = "ko"
    
    return f"""
    <!DOCTYPE html>
    <html lang="{lang}">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{t('title', lang)}</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <script src="https://cdn.jsdelivr.net/npm/chart.js?v=2.0"></script>
        <style>
            .energy-card {{
                transition: transform 0.2s;
                border: none;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }}
            .energy-card:hover {{
                transform: translateY(-5px);
                box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
            }}
            .status-indicator {{
                width: 12px;
                height: 12px;
                border-radius: 50%;
                display: inline-block;
                margin-right: 8px;
            }}
            .status-online {{ background-color: #28a745; }}
            .status-offline {{ background-color: #dc3545; }}
        </style>
    </head>
    <body class="bg-light">
        {generate_navigation(lang)}

        <div class="container-fluid mt-4">
            <!-- 메인 배너 -->
            <div class="row mb-4">
                <div class="col-12">
                    <div class="card bg-primary text-white">
                        <div class="card-body d-flex align-items-center">
                            <div class="me-4">
                                <i class="fas fa-robot fa-4x"></i>
                            </div>
                            <div class="flex-grow-1">
                                <h1 class="card-title mb-2">LLM SLM Development</h1>
                                <h4 class="card-subtitle mb-3">에너지 특화 언어 모델 개발</h4>
                                <p class="card-text">Advanced AI language model specialized for energy management and analysis</p>
                            </div>
                            <div>
                                <a href="/llm-slm?lang={lang}" class="btn btn-light btn-lg">
                                    <i class="fas fa-arrow-right"></i> LLM SLM
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 5개의 서비스 카드 -->
            <div class="row">
                <!-- System Health 카드 -->
                <div class="col-md-2 mb-4">
                    <div class="card energy-card h-100">
                        <div class="card-body text-center">
                            <div class="mb-3">
                                <i class="fas fa-heartbeat text-success" style="font-size: 2.5rem;"></i>
                            </div>
                            <h6 class="card-title">{t('navigation.health', lang)}</h6>
                            <p class="card-text small text-muted mb-3">
                                {t('common.realTime', lang)} {t('common.monitoring', lang)}
                            </p>
                            <a href="/health?lang={lang}" class="btn btn-success btn-sm w-100">
                                <i class="fas fa-arrow-right"></i> {t('navigation.health', lang)}
                            </a>
                        </div>
                    </div>
                </div>

                <!-- ML/AI Engine 카드 -->
                <div class="col-md-2 mb-4">
                    <div class="card energy-card h-100">
                        <div class="card-body text-center">
                            <div class="mb-3">
                                <i class="fas fa-brain text-primary" style="font-size: 2.5rem;"></i>
                            </div>
                            <h6 class="card-title">{t('navigation.modelTesting', lang)}</h6>
                            <p class="card-text small text-muted mb-3">
                                {t('modelTesting.title', lang)}
                            </p>
                            <a href="/model-testing?lang={lang}" class="btn btn-primary btn-sm w-100">
                                <i class="fas fa-arrow-right"></i> {t('navigation.modelTesting', lang)}
                            </a>
                        </div>
                    </div>
                </div>

                <!-- Energy Demand Monitoring 카드 -->
                <div class="col-md-2 mb-4">
                    <div class="card energy-card h-100">
                        <div class="card-body text-center">
                            <div class="mb-3">
                                <i class="fas fa-chart-bar text-info" style="font-size: 2.5rem;"></i>
                            </div>
                            <h6 class="card-title">{t('navigation.energyDemand', lang)}</h6>
                            <p class="card-text small text-muted mb-3">
                                {t('energyDemand.title', lang)}
                            </p>
                            <a href="/data-analysis?lang={lang}" class="btn btn-info btn-sm w-100">
                                <i class="fas fa-arrow-right"></i> {t('navigation.energyDemand', lang)}
                            </a>
                        </div>
                    </div>
                </div>

                <!-- Energy Supply Monitoring 카드 -->
                <div class="col-md-2 mb-4">
                    <div class="card energy-card h-100">
                        <div class="card-body text-center">
                            <div class="mb-3">
                                <i class="fas fa-sun text-warning" style="font-size: 2.5rem;"></i>
                            </div>
                            <h6 class="card-title">{t('navigation.energySupply', lang)}</h6>
                            <p class="card-text small text-muted mb-3">
                                {t('energySupply.title', lang)}
                            </p>
                            <a href="/data-collection?lang={lang}" class="btn btn-warning btn-sm w-100">
                                <i class="fas fa-arrow-right"></i> {t('navigation.energySupply', lang)}
                            </a>
                        </div>
                    </div>
                </div>

                <!-- Demand Control 카드 -->
                <div class="col-md-2 mb-4">
                    <div class="card energy-card h-100">
                        <div class="card-body text-center">
                            <div class="mb-3">
                                <i class="fas fa-sliders-h text-danger" style="font-size: 2.5rem;"></i>
                            </div>
                            <h6 class="card-title">{t('navigation.demandControl', lang)}</h6>
                            <p class="card-text small text-muted mb-3">
                                {t('demandControl.title', lang)}
                            </p>
                            <a href="/statistics?lang={lang}" class="btn btn-danger btn-sm w-100">
                                <i class="fas fa-arrow-right"></i> {t('navigation.demandControl', lang)}
                            </a>
                        </div>
                    </div>
                </div>

                <!-- CrewAI System 카드 -->
                <div class="col-md-2 mb-4">
                    <div class="card energy-card h-100">
                        <div class="card-body text-center">
                            <div class="mb-3">
                                <i class="fas fa-users-cog text-info" style="font-size: 2.5rem;"></i>
                            </div>
                            <h6 class="card-title">CrewAI System</h6>
                            <p class="card-text small text-muted mb-3">
                                전문화된 에이전트 팀 자동화
                            </p>
                            <a href="/crewai-system?lang={lang}" class="btn btn-info btn-sm w-100">
                                <i class="fas fa-arrow-right"></i> CrewAI System
                            </a>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 실시간 에너지 분석 차트 -->
            <div class="row mt-4">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header">
                            <h5 class="mb-0">
                                <i class="fas fa-chart-line"></i> <span data-translate="realtime_analysis">Real-time Energy Analysis</span>
                                <small class="text-muted ms-2">24시간 실시간 에너지 분석</small>
                            </h5>
                        </div>
                        <div class="card-body">
                            <div class="mb-3">
                                <span class="badge bg-info me-2">○</span> <span data-translate="actual_consumption">실제 에너지 소비 (kWh)</span>
                                <span class="badge bg-warning ms-3 me-2">○</span> <span data-translate="predicted_consumption">예측 에너지 소비 (kWh)</span>
                            </div>
                            <canvas id="energyChart" width="400" height="100"></canvas>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <script>
            // 실시간 에너지 데이터 생성
            function generateEnergyData() {{
                const hours = [];
                const actualData = [];
                const predictedData = [];
                
                for (let i = 0; i < 24; i++) {{
                    hours.push(i.toString().padStart(2, '0') + ':00');
                    // 실제 데이터 (더 불규칙한 패턴)
                    const baseConsumption = 50 + Math.sin(i * Math.PI / 12) * 30;
                    const randomVariation = (Math.random() - 0.5) * 20;
                    actualData.push(Math.max(0, baseConsumption + randomVariation));
                    
                    // 예측 데이터 (더 부드러운 패턴, 14시부터 시작)
                    if (i >= 14) {{
                        const predictedBase = 45 + Math.sin(i * Math.PI / 12) * 25;
                        const predictedVariation = (Math.random() - 0.5) * 10;
                        predictedData.push(Math.max(0, predictedBase + predictedVariation));
                    }} else {{
                        predictedData.push(null);
                    }}
                }}
                
                return {{ hours, actualData, predictedData }};
            }}

            // 차트 초기화
            function initEnergyChart() {{
                const ctx = document.getElementById('energyChart').getContext('2d');
                const data = generateEnergyData();
                
                new Chart(ctx, {{
                    type: 'line',
                    data: {{
                        labels: data.hours,
                        datasets: [{{
                            label: '실제 에너지 소비 (kWh)',
                            data: data.actualData,
                            borderColor: 'rgb(75, 192, 192)',
                            backgroundColor: 'rgba(75, 192, 192, 0.2)',
                            tension: 0.1
                        }}, {{
                            label: '예측 에너지 소비 (kWh)',
                            data: data.predictedData,
                            borderColor: 'rgb(255, 205, 86)',
                            backgroundColor: 'rgba(255, 205, 86, 0.2)',
                            borderDash: [5, 5],
                            tension: 0.1
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        scales: {{
                            y: {{
                                beginAtZero: true,
                                title: {{
                                    display: true,
                                    text: '에너지 소비량 (kWh)'
                                }}
                            }},
                            x: {{
                                title: {{
                                    display: true,
                                    text: '시간 (24시간)'
                                }}
                            }}
                        }},
                        plugins: {{
                            legend: {{
                                display: false
                            }}
                        }}
                    }}
                }});
            }}

            // 페이지 로드 시 차트 초기화
            document.addEventListener('DOMContentLoaded', function() {{
                initEnergyChart();
            }});
        </script>
    </body>
    </html>
    """

@web_app.get("/health", response_class=HTMLResponse)
async def health_page(request: Request, lang: str = Query("ko", description="Language code")):
    """연결된 Digital Experience Intelligence Platform"""
    # 언어 설정
    if lang not in get_available_languages():
        lang = "ko"
    
    return f"""
    <!DOCTYPE html>
    <html lang="{lang}">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{t('health.title', lang)}</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            body {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            }}
            .main-container {{
                max-width: 1400px;
                margin: 0 auto;
                padding: 20px;
            }}
            .header-card {{
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 40px;
                margin-bottom: 30px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                text-align: center;
            }}
            .system-status-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin: 30px 0;
            }}
            .system-card {{
                background: rgba(255, 255, 255, 0.9);
                border-radius: 15px;
                padding: 25px;
                text-align: center;
                box-shadow: 0 10px 25px rgba(0,0,0,0.1);
                transition: all 0.3s ease;
                cursor: pointer;
            }}
            .system-card:hover {{
                transform: translateY(-5px);
                box-shadow: 0 15px 35px rgba(0,0,0,0.15);
            }}
            .status-indicator {{
                width: 12px;
                height: 12px;
                border-radius: 50%;
                display: inline-block;
                margin-right: 8px;
            }}
            .status-online {{ background-color: #28a745; }}
            .status-offline {{ background-color: #dc3545; }}
            .status-warning {{ background-color: #ffc107; }}
            .feature-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
                gap: 25px;
                margin-bottom: 30px;
            }}
            .feature-card {{
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 30px;
                box-shadow: 0 15px 35px rgba(0,0,0,0.1);
                transition: all 0.3s ease;
                border-left: 5px solid #667eea;
                cursor: pointer;
            }}
            .feature-card:hover {{
                transform: translateY(-10px);
                box-shadow: 0 25px 50px rgba(0,0,0,0.15);
            }}
            .feature-icon {{
                font-size: 3rem;
                margin-bottom: 20px;
                background: linear-gradient(135deg, #667eea, #764ba2);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }}
            .interaction-tracker {{
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                color: white;
            }}
            .ai-insights {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }}
            .session-replay {{
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                color: white;
            }}
            .privacy-protection {{
                background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
                color: white;
            }}
            .real-time-monitoring {{
                background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
                color: white;
            }}
            .flexible-deployment {{
                background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
                color: #333;
            }}
            .stats-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin: 20px 0;
            }}
            .stat-card {{
                background: rgba(255, 255, 255, 0.9);
                border-radius: 15px;
                padding: 20px;
                text-align: center;
                box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            }}
            .stat-value {{
                font-size: 2.5rem;
                font-weight: bold;
                color: #667eea;
                margin-bottom: 10px;
            }}
            .stat-label {{
                color: #666;
                font-size: 0.9rem;
                text-transform: uppercase;
                letter-spacing: 1px;
            }}
            .progress-modern {{
                height: 8px;
                border-radius: 10px;
                background: rgba(255,255,255,0.3);
                overflow: hidden;
                margin: 15px 0;
            }}
            .progress-bar-modern {{
                height: 100%;
                background: linear-gradient(90deg, #4facfe, #00f2fe);
                border-radius: 10px;
                transition: width 0.3s ease;
            }}
            .ai-chat {{
                background: rgba(255,255,255,0.1);
                border-radius: 15px;
                padding: 20px;
                margin: 20px 0;
                max-height: 300px;
                overflow-y: auto;
            }}
            .ai-message {{
                margin: 10px 0;
                padding: 15px;
                border-radius: 15px;
                max-width: 80%;
            }}
            .ai-user {{
                background: rgba(255,255,255,0.2);
                margin-left: auto;
            }}
            .ai-assistant {{
                background: rgba(255,255,255,0.1);
            }}
            .heatmap-container {{
                background: rgba(255,255,255,0.1);
                border-radius: 15px;
                padding: 20px;
                margin: 20px 0;
                position: relative;
                height: 200px;
            }}
            .heatmap-point {{
                position: absolute;
                width: 12px;
                height: 12px;
                background: #ff6b6b;
                border-radius: 50%;
                opacity: 0.8;
                animation: pulse 2s infinite;
            }}
            @keyframes pulse {{
                0% {{ transform: scale(1); opacity: 0.8; }}
                50% {{ transform: scale(1.2); opacity: 0.6; }}
                100% {{ transform: scale(1); opacity: 0.8; }}
            }}
            .alert-modern {{
                border-radius: 15px;
                border: none;
                padding: 15px 20px;
                margin: 10px 0;
                backdrop-filter: blur(10px);
            }}
            .btn-modern {{
                border-radius: 25px;
                padding: 12px 30px;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 1px;
                transition: all 0.3s ease;
                border: none;
            }}
            .btn-modern:hover {{
                transform: translateY(-2px);
                box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            }}
            .language-selector {{
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 1000;
            }}
            .uptime-display {{
                font-family: 'Courier New', monospace;
                font-size: 1.2rem;
                color: #28a745;
                font-weight: bold;
            }}
            .link-indicator {{
                color: #007bff;
                font-size: 0.8rem;
                margin-top: 10px;
            }}
        </style>
    </head>
    <body>
        <!-- 언어 선택기 -->
        <div class="language-selector">
            <div class="btn-group" role="group">
                <a href="?lang=ko" class="btn btn-light btn-sm">🇰🇷 한국어</a>
                <a href="?lang=en" class="btn btn-light btn-sm">🇺🇸 English</a>
                <a href="?lang=zh" class="btn btn-light btn-sm">🇨🇳 中文</a>
            </div>
        </div>

        <div class="main-container">
            <!-- 헤더 -->
            <div class="header-card">
                <h1 class="display-4 mb-4">
                    <i class="fas fa-brain"></i> Digital Experience Intelligence Platform
                </h1>
                <p class="lead mb-4">포괄적인 사용자 경험 분석 및 최적화 솔루션</p>
                
                <!-- 실시간 통계 -->
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-value" id="totalInteractions">0</div>
                        <div class="stat-label">총 상호작용</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value" id="activeSessions">0</div>
                        <div class="stat-label">활성 세션</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value" id="conversionRate">0%</div>
                        <div class="stat-label">전환율</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value" id="errorRate">0%</div>
                        <div class="stat-label">오류율</div>
                    </div>
                </div>
            </div>

            <!-- 시스템 상태 (Health 카드들) -->
            <div class="system-status-grid">
                <div class="system-card" onclick="window.location.href='/?lang={lang}'">
                    <i class="fas fa-server fa-3x text-success mb-3"></i>
                    <h5>Web Server</h5>
                    <p>
                        <span class="status-indicator status-online"></span>
                        <strong>Online</strong>
                    </p>
                    <small class="text-muted">Port: 8000</small>
                    <div class="link-indicator">
                        🔗 메인 대시보드로 이동
                    </div>
                </div>
                
                <div class="system-card" onclick="window.location.href='/api/health'">
                    <i class="fas fa-cogs fa-3x text-primary mb-3"></i>
                    <h5>API Services</h5>
                    <p>
                        <span class="status-indicator status-online"></span>
                        <strong>Healthy</strong>
                    </p>
                    <small class="text-muted">All endpoints active</small>
                    <div class="link-indicator">
                        🔗 API 상태 확인
                    </div>
                </div>
                
                <div class="system-card" onclick="window.location.href='/data-collection?lang={lang}'">
                    <i class="fas fa-database fa-3x text-info mb-3"></i>
                    <h5>Data Storage</h5>
                    <p>
                        <span class="status-indicator status-online"></span>
                        <strong>Connected</strong>
                    </p>
                    <small class="text-muted">SQLite Database</small>
                    <div class="link-indicator">
                        🔗 데이터 수집 페이지
                    </div>
                </div>
                
                <div class="system-card" onclick="window.location.href='/statistics?lang={lang}'">
                    <i class="fas fa-clock fa-3x text-warning mb-3"></i>
                    <h5>Uptime</h5>
                    <p class="uptime-display" id="uptime">Calculating...</p>
                    <small class="text-muted">Last Update: <span id="lastUpdate"></span></small>
                    <div class="link-indicator">
                        🔗 통계 페이지
                    </div>
                </div>
            </div>

            <!-- 기능 카드들 (메뉴) -->
            <div class="feature-grid">
                <!-- 실시간 이벤트 캡처 -->
                <div class="feature-card interaction-tracker" onclick="window.location.href='/data-analysis?lang={lang}'">
                    <div class="feature-icon">
                        <i class="fas fa-mouse-pointer"></i>
                    </div>
                    <h3>실시간 이벤트 캡처</h3>
                    <p>클릭, 스크롤, 폼 제출 등 모든 사용자 상호작용을 실시간으로 추적합니다.</p>
                    
                    <div class="progress-modern">
                        <div class="progress-bar-modern" style="width: 95%"></div>
                    </div>
                    <small>프론트엔드 이벤트 캡처율: 95%</small>
                    
                    <div class="progress-modern">
                        <div class="progress-bar-modern" style="width: 98%"></div>
                    </div>
                    <small>백엔드 API 호출 캡처율: 98%</small>
                    
                    <div class="mt-3">
                        <button class="btn btn-light btn-modern" onclick="event.stopPropagation(); window.location.href='/data-analysis?lang={lang}'">
                            <i class="fas fa-chart-line"></i> 데이터 분석 페이지
                        </button>
                    </div>
                </div>

                <!-- AI 인사이트 -->
                <div class="feature-card ai-insights" onclick="window.location.href='/llm-slm?lang={lang}'">
                    <div class="feature-icon">
                        <i class="fas fa-robot"></i>
                    </div>
                    <h3>AI 인사이트 (SLM 기반)</h3>
                    <p>Small Language Model 기반 대화형 분석 어시스턴트로 심층적인 인사이트를 제공합니다.</p>
                    
                    <div class="ai-chat" id="aiChat">
                        <div class="ai-message ai-assistant">
                            <strong>AI Assistant:</strong> 안녕하세요! 사용자 경험 분석을 도와드리겠습니다.
                        </div>
                        <div class="ai-message ai-user">
                            전환율을 개선하는 방법을 알려주세요
                        </div>
                        <div class="ai-message ai-assistant">
                            <strong>AI Assistant:</strong> 분석 결과, 3단계에서 이탈률이 높습니다. CTA 버튼 위치를 조정해보세요.
                        </div>
                    </div>
                    
                    <div class="mt-3">
                        <button class="btn btn-light btn-modern" onclick="event.stopPropagation(); window.location.href='/llm-slm?lang={lang}'">
                            <i class="fas fa-brain"></i> LLM-SLM 개발 페이지
                        </button>
                    </div>
                </div>

                <!-- 세션 리플레이 -->
                <div class="feature-card session-replay" onclick="window.location.href='/weather-analysis?lang={lang}'">
                    <div class="feature-icon">
                        <i class="fas fa-video"></i>
                    </div>
                    <h3>세션 리플레이</h3>
                    <p>사용자 행동 패턴을 시각화하고 히트맵으로 마찰 지점을 분석합니다.</p>
                    
                    <div class="heatmap-container" id="heatmapContainer">
                        <div class="heatmap-point" style="top: 20px; left: 30px;"></div>
                        <div class="heatmap-point" style="top: 50px; left: 80px;"></div>
                        <div class="heatmap-point" style="top: 80px; left: 120px;"></div>
                        <div class="heatmap-point" style="top: 120px; left: 200px;"></div>
                        <div class="heatmap-point" style="top: 150px; left: 250px;"></div>
                    </div>
                    
                    <div class="mt-3">
                        <button class="btn btn-light btn-modern" onclick="event.stopPropagation(); window.location.href='/weather-analysis?lang={lang}'">
                            <i class="fas fa-cloud-sun"></i> 날씨 분석 페이지
                        </button>
                    </div>
                </div>

                <!-- 프라이버시 보호 -->
                <div class="feature-card privacy-protection" onclick="window.location.href='/model-testing?lang={lang}'">
                    <div class="feature-icon">
                        <i class="fas fa-shield-alt"></i>
                    </div>
                    <h3>프라이버시 보호</h3>
                    <p>PII, PCI, PHI 등 민감한 데이터를 자동으로 마스킹하여 보안을 보장합니다.</p>
                    
                    <div class="alert alert-modern alert-success">
                        <i class="fas fa-check-circle"></i> PII 데이터 마스킹: 100% 활성
                    </div>
                    <div class="alert alert-modern alert-success">
                        <i class="fas fa-check-circle"></i> PCI 데이터 마스킹: 100% 활성
                    </div>
                    <div class="alert alert-modern alert-success">
                        <i class="fas fa-check-circle"></i> PHI 데이터 마스킹: 100% 활성
                    </div>
                    
                    <div class="mt-3">
                        <button class="btn btn-light btn-modern" onclick="event.stopPropagation(); window.location.href='/model-testing?lang={lang}'">
                            <i class="fas fa-cogs"></i> ML/AI 엔진 페이지
                        </button>
                    </div>
                </div>

                <!-- 실시간 모니터링 -->
                <div class="feature-card real-time-monitoring" onclick="window.location.href='/weather-dashboard?lang={lang}'">
                    <div class="feature-icon">
                        <i class="fas fa-bell"></i>
                    </div>
                    <h3>실시간 모니터링</h3>
                    <p>전환율 변화, 오류 감지, 사용자 불편을 실시간으로 모니터링하고 알림합니다.</p>
                    
                    <div class="alert alert-modern alert-warning">
                        <i class="fas fa-exclamation-triangle"></i> 전환율 15% 감소 감지
                    </div>
                    <div class="alert alert-modern alert-info">
                        <i class="fas fa-info-circle"></i> 새로운 사용자 세션 시작
                    </div>
                    <div class="alert alert-modern alert-success">
                        <i class="fas fa-check-circle"></i> 시스템 정상 작동
                    </div>
                    
                    <div class="mt-3">
                        <button class="btn btn-light btn-modern" onclick="event.stopPropagation(); window.location.href='/weather-dashboard?lang={lang}'">
                            <i class="fas fa-chart-area"></i> 날씨 대시보드
                        </button>
                    </div>
                </div>

                <!-- 유연한 배포 -->
                <div class="feature-card flexible-deployment" onclick="window.location.href='/api/dashboard'">
                    <div class="feature-icon">
                        <i class="fas fa-cloud"></i>
                    </div>
                    <h3>유연한 배포</h3>
                    <p>하이브리드, 싱글 테넌트, 멀티 테넌트 환경을 지원합니다.</p>
                    
                    <div class="row">
                        <div class="col-4 text-center">
                            <i class="fas fa-cloud fa-2x mb-2" style="color: #667eea;"></i>
                            <div class="small">하이브리드</div>
                            <span class="badge bg-primary">활성</span>
                        </div>
                        <div class="col-4 text-center">
                            <i class="fas fa-server fa-2x mb-2" style="color: #28a745;"></i>
                            <div class="small">싱글 테넌트</div>
                            <span class="badge bg-success">사용 가능</span>
                        </div>
                        <div class="col-4 text-center">
                            <i class="fas fa-users fa-2x mb-2" style="color: #17a2b8;"></i>
                            <div class="small">멀티 테넌트</div>
                            <span class="badge bg-info">사용 가능</span>
                        </div>
                    </div>
                    
                    <div class="mt-3">
                        <button class="btn btn-light btn-modern" onclick="event.stopPropagation(); window.location.href='/api/dashboard'">
                            <i class="fas fa-chart-bar"></i> API 대시보드
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
        <script>
            // 실시간 통계 업데이트
            function updateStats() {{
                document.getElementById('totalInteractions').textContent = (Math.floor(Math.random() * 1000) + 1000).toLocaleString();
                document.getElementById('activeSessions').textContent = Math.floor(Math.random() * 50) + 10;
                document.getElementById('conversionRate').textContent = (Math.random() * 10 + 5).toFixed(1) + '%';
                document.getElementById('errorRate').textContent = (Math.random() * 2).toFixed(2) + '%';
            }}

            // 히트맵 업데이트
            function generateHeatmap() {{
                const container = document.getElementById('heatmapContainer');
                const points = container.querySelectorAll('.heatmap-point');
                points.forEach(point => {{
                    point.style.top = Math.random() * 180 + 'px';
                    point.style.left = Math.random() * 300 + 'px';
                }});
            }}

            // 업타임 계산
            function updateUptime() {{
                const startTime = new Date('2025-10-11T01:22:47Z');
                const now = new Date();
                const diff = now - startTime;
                
                const hours = Math.floor(diff / (1000 * 60 * 60));
                const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
                const seconds = Math.floor((diff % (1000 * 60)) / 1000);
                
                document.getElementById('uptime').textContent = `${{hours}}h ${{minutes}}m ${{seconds}}s`;
            }}

            // 초기화
            document.addEventListener('DOMContentLoaded', function() {{
                updateStats();
                updateUptime();
                setInterval(updateStats, 5000); // 5초마다 통계 업데이트
                setInterval(updateUptime, 1000); // 1초마다 업타임 업데이트
                setInterval(generateHeatmap, 10000); // 10초마다 히트맵 업데이트
                document.getElementById('lastUpdate').textContent = new Date().toLocaleTimeString();
            }});
        </script>
    </body>
    </html>
    """

@web_app.get("/digital-experience", response_class=HTMLResponse)
async def digital_experience_page(request: Request, lang: str = Query("ko", description="Language code")):
    """Digital Experience Intelligence 전용 페이지 - 리다이렉트용"""
    # /health로 리다이렉트
    return RedirectResponse(url=f"/health?lang={lang}")

# API 엔드포인트들
@web_app.get("/api/health")
async def api_health():
    """API Health Check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "services": {
            "web_interface": "online",
            "api": "online",
            "database": "online"
        }
    }

@web_app.get("/api/dashboard")
async def api_dashboard():
    """Dashboard API"""
    return {
        "message": "Dashboard API is working",
        "timestamp": datetime.now().isoformat()
    }

@web_app.get("/api/models")
async def api_models():
    """Models API"""
    return {
        "message": "Models API is working",
        "timestamp": datetime.now().isoformat()
    }

@web_app.get("/api/statistics")
async def api_statistics():
    """Statistics API"""
    return {
        "message": "Statistics API is working",
        "timestamp": datetime.now().isoformat()
    }

@web_app.get("/api/languages")
async def api_languages():
    """Languages API"""
    return {
        "languages": get_available_languages(),
        "current": "ko",
        "timestamp": datetime.now().isoformat()
    }

@web_app.get("/statistics", response_class=HTMLResponse)
async def statistics_page(request: Request, lang: str = Query("ko", description="Language code")):
    """Demand Control 페이지 - Smart Grid Service Overview 기반"""
    # 언어 설정
    if lang not in get_available_languages():
        lang = "ko"
    
    return f"""
    <!DOCTYPE html>
    <html lang="{lang}">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{t('demandControl.title', lang)}</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <script src="https://cdn.jsdelivr.net/npm/chart.js?v=2.0"></script>
        <style>
            body {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }}
            .control-card {{
                background: rgba(255, 255, 255, 0.95);
                border-radius: 15px;
                padding: 20px;
                margin-bottom: 20px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }}
            .smart-ess-card {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }}
            .control-value {{
                font-size: 2rem;
                font-weight: bold;
                color: #2c3e50;
            }}
            .control-label {{
                font-size: 0.9rem;
                color: #7f8c8d;
                margin-top: 5px;
            }}
            .device-item {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 10px 0;
                border-bottom: 1px solid #ecf0f1;
            }}
            .device-item:last-child {{
                border-bottom: none;
            }}
            .chart-container {{
                max-height: 200px;
            }}
            .status-badge {{
                padding: 5px 10px;
                border-radius: 20px;
                font-size: 0.8rem;
                font-weight: bold;
            }}
            .status-active {{ background-color: #2ecc71; color: white; }}
            .status-standby {{ background-color: #f39c12; color: white; }}
            .status-offline {{ background-color: #e74c3c; color: white; }}
        </style>
    </head>
    <body>
        {generate_navigation(lang)}

        <div class="container-fluid mt-4">
            <!-- Smart ESS 중앙 제어 -->
            <div class="row">
                <div class="col-12">
                    <div class="control-card smart-ess-card">
                        <h4><i class="fas fa-microchip"></i> <span data-translate="smart_ess_title">Smart ESS (Energy Storage System)</span></h4>
                        <div class="row">
                            <div class="col-md-3">
                                <div class="control-value" id="essCapacity">85%</div>
                                <div class="control-label" data-translate="smart_ess_capacity">Battery Capacity</div>
                            </div>
                            <div class="col-md-3">
                                <div class="control-value" id="essPower">2.3 kW</div>
                                <div class="control-label" data-translate="smart_ess_power">Current Power</div>
                            </div>
                            <div class="col-md-3">
                                <div class="control-value" id="essEfficiency">94.2%</div>
                                <div class="control-label" data-translate="smart_ess_efficiency">System Efficiency</div>
                            </div>
                            <div class="col-md-3">
                                <div class="control-value" id="essStatus" data-translate="online">Online</div>
                                <div class="control-label" data-translate="smart_ess_status">System Status</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Peak/Night-time Power Supply & Environmental Sensors -->
            <div class="row">
                <!-- Peak/Night-time Power Supply -->
                <div class="col-lg-6">
                    <div class="control-card">
                        <h5><i class="fas fa-solar-panel"></i> Peak/Night-time Power Supply</h5>
                        <div class="row">
                            <div class="col-md-6">
                                <div class="device-item">
                                    <span><i class="fas fa-sun text-warning"></i> Solar Generation</span>
                                    <span class="text-success" id="solarGen">3.2 kW</span>
                                </div>
                                <div class="device-item">
                                    <span><i class="fas fa-wind text-info"></i> Small-scale Wind Energy</span>
                                    <span class="text-info" id="windGen">1.8 kW</span>
                                </div>
                                <div class="device-item">
                                    <span><i class="fas fa-battery-half text-primary"></i> Fuel Cells & Others</span>
                                    <span class="text-primary" id="fuelCell">0.5 kW</span>
                                </div>
                                <div class="alert alert-info mt-3" role="alert">
                                    <i class="fas fa-wifi"></i> <strong>WiFi Network:</strong> Connected to Supply-side Monitoring
                                </div>
                            </div>
                            <div class="col-md-6">
                                <canvas id="supplyChart" class="chart-container"></canvas>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Wireless Integrated Environmental Sensors -->
                <div class="col-lg-6">
                    <div class="control-card sensor-card">
                        <h5><i class="fas fa-thermometer-half"></i> Wireless Integrated Environmental Sensors</h5>
                        <div class="row">
                            <div class="col-md-6">
                                <div class="device-item">
                                    <span><i class="fas fa-thermometer-half text-danger"></i> Temperature</span>
                                    <span class="text-danger" id="temperature">23.5°C</span>
                                </div>
                                <div class="device-item">
                                    <span><i class="fas fa-tint text-info"></i> Humidity</span>
                                    <span class="text-info" id="humidity">65%</span>
                                </div>
                                <div class="device-item">
                                    <span><i class="fas fa-wind text-success"></i> Wind Speed</span>
                                    <span class="text-success" id="windSpeed">12 km/h</span>
                                </div>
                                <div class="device-item">
                                    <span><i class="fas fa-sun text-warning"></i> Solar Irradiance</span>
                                    <span class="text-warning" id="solarIrradiance">850 W/m²</span>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <canvas id="sensorChart" class="chart-container"></canvas>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Device Control Panel -->
            <div class="row">
                <div class="col-12">
                    <div class="control-card">
                        <h5><i class="fas fa-cogs"></i> Device Control Panel</h5>
                        <div class="row">
                            <div class="col-md-4">
                                <h6>Energy Storage System</h6>
                                <div class="device-item">
                                    <span>ESS Controller</span>
                                    <span class="status-badge status-active">Active</span>
                                </div>
                                <div class="device-item">
                                    <span>Battery Management</span>
                                    <span class="status-badge status-active">Active</span>
                                </div>
                                <div class="device-item">
                                    <span>Power Conversion</span>
                                    <span class="status-badge status-standby">Standby</span>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <h6>Renewable Energy</h6>
                                <div class="device-item">
                                    <span>Solar Inverter</span>
                                    <span class="status-badge status-active">Active</span>
                                </div>
                                <div class="device-item">
                                    <span>Wind Turbine</span>
                                    <span class="status-badge status-active">Active</span>
                                </div>
                                <div class="device-item">
                                    <span>Fuel Cell System</span>
                                    <span class="status-badge status-standby">Standby</span>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <h6>Monitoring Systems</h6>
                                <div class="device-item">
                                    <span>Environmental Sensors</span>
                                    <span class="status-badge status-active">Active</span>
                                </div>
                                <div class="device-item">
                                    <span>Power Meters</span>
                                    <span class="status-badge status-active">Active</span>
                                </div>
                                <div class="device-item">
                                    <span>Communication Hub</span>
                                    <span class="status-badge status-active">Active</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 실증 사이트 관리 -->
            <div class="row">
                <div class="col-12">
                    <div class="control-card">
                        <h5><i class="fas fa-globe"></i> 실증 사이트 관리 (Demo Sites)</h5>
                        <div class="row">
                            <!-- Demo 1: Finland -->
                            <div class="col-md-6 mb-4">
                                <div class="card h-100" style="border: 2px solid #007bff;">
                                    <div class="card-header bg-primary text-white">
                                        <h6 class="mb-0"><i class="fas fa-university"></i> Demo 1: Oulu University</h6>
                                        <small>🇫🇮 Finland - 대학/공공</small>
                                    </div>
                                    <div class="card-body">
                                        <h6>Academic Buildings</h6>
                                        <p class="card-text">
                                            <strong>특징:</strong> 극한 기후, 스마트 빌딩<br>
                                            <strong>연구 분야:</strong> 극한 환경 에너지 관리<br>
                                            <strong>시스템 상태:</strong> 
                                            <span class="status-badge status-active">Active</span>
                                        </p>
                                        <div class="row text-center">
                                            <div class="col-4">
                                                <small>에너지 효율</small><br>
                                                <strong>92.3%</strong>
                                            </div>
                                            <div class="col-4">
                                                <small>절약률</small><br>
                                                <strong>15.7%</strong>
                                            </div>
                                            <div class="col-4">
                                                <small>연결 상태</small><br>
                                                <span class="status-badge status-active">Online</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- Demo 2: Sweden -->
                            <div class="col-md-6 mb-4">
                                <div class="card h-100" style="border: 2px solid #28a745;">
                                    <div class="card-header bg-success text-white">
                                        <h6 class="mb-0"><i class="fas fa-flask"></i> Demo 2: KTH University</h6>
                                        <small>🇸🇪 Sweden - 대학</small>
                                    </div>
                                    <div class="card-body">
                                        <h6>Living Lab</h6>
                                        <p class="card-text">
                                            <strong>특징:</strong> 실증 연구, 지속가능성<br>
                                            <strong>연구 분야:</strong> 지속가능 에너지 시스템<br>
                                            <strong>시스템 상태:</strong> 
                                            <span class="status-badge status-active">Active</span>
                                        </p>
                                        <div class="row text-center">
                                            <div class="col-4">
                                                <small>에너지 효율</small><br>
                                                <strong>94.8%</strong>
                                            </div>
                                            <div class="col-4">
                                                <small>절약률</small><br>
                                                <strong>18.2%</strong>
                                            </div>
                                            <div class="col-4">
                                                <small>연결 상태</small><br>
                                                <span class="status-badge status-active">Online</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- Demo 3: Romania -->
                            <div class="col-md-6 mb-4">
                                <div class="card h-100" style="border: 2px solid #ffc107;">
                                    <div class="card-header bg-warning text-dark">
                                        <h6 class="mb-0"><i class="fas fa-microchip"></i> Demo 3: BEIA</h6>
                                        <small>🇷🇴 Romania - 연구소</small>
                                    </div>
                                    <div class="card-body">
                                        <h6>Research Institute</h6>
                                        <p class="card-text">
                                            <strong>특징:</strong> IoT, 스마트 시스템<br>
                                            <strong>연구 분야:</strong> IoT 기반 에너지 관리<br>
                                            <strong>시스템 상태:</strong> 
                                            <span class="status-badge status-active">Active</span>
                                        </p>
                                        <div class="row text-center">
                                            <div class="col-4">
                                                <small>에너지 효율</small><br>
                                                <strong>89.5%</strong>
                                            </div>
                                            <div class="col-4">
                                                <small>절약률</small><br>
                                                <strong>12.4%</strong>
                                            </div>
                                            <div class="col-4">
                                                <small>연결 상태</small><br>
                                                <span class="status-badge status-active">Online</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- Demo 4: Greece -->
                            <div class="col-md-6 mb-4">
                                <div class="card h-100" style="border: 2px solid #dc3545;">
                                    <div class="card-header bg-danger text-white">
                                        <h6 class="mb-0"><i class="fas fa-building"></i> Demo 4: Triaena/OTE</h6>
                                        <small>🇬🇷 Greece - 기업</small>
                                    </div>
                                    <div class="card-body">
                                        <h6>Commercial Buildings</h6>
                                        <p class="card-text">
                                            <strong>특징:</strong> 상업 빌딩, 통신 인프라<br>
                                            <strong>연구 분야:</strong> 상업용 에너지 최적화<br>
                                            <strong>시스템 상태:</strong> 
                                            <span class="status-badge status-active">Active</span>
                                        </p>
                                        <div class="row text-center">
                                            <div class="col-4">
                                                <small>에너지 효율</small><br>
                                                <strong>91.7%</strong>
                                            </div>
                                            <div class="col-4">
                                                <small>절약률</small><br>
                                                <strong>16.9%</strong>
                                            </div>
                                            <div class="col-4">
                                                <small>연결 상태</small><br>
                                                <span class="status-badge status-active">Online</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- 실증 사이트 통합 모니터링 -->
                        <div class="row mt-4">
                            <div class="col-12">
                                <div class="card">
                                    <div class="card-header bg-info text-white">
                                        <h6 class="mb-0"><i class="fas fa-chart-line"></i> 실증 사이트 통합 모니터링</h6>
                                    </div>
                                    <div class="card-body">
                                        <div class="row text-center">
                                            <div class="col-md-3">
                                                <h4 class="text-primary">4</h4>
                                                <small>활성 사이트</small>
                                            </div>
                                            <div class="col-md-3">
                                                <h4 class="text-success">92.1%</h4>
                                                <small>평균 효율</small>
                                            </div>
                                            <div class="col-md-3">
                                                <h4 class="text-warning">15.8%</h4>
                                                <small>평균 절약률</small>
                                            </div>
                                            <div class="col-md-3">
                                                <h4 class="text-info">100%</h4>
                                                <small>연결률</small>
                                            </div>
                                        </div>
                                        <div class="mt-3">
                                            <canvas id="demoSitesChart" class="chart-container"></canvas>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
        <script>
            // 실시간 데이터 업데이트
            function updateRealtimeData() {{
                // ESS 데이터 업데이트
                document.getElementById('essCapacity').textContent = (Math.random() * 20 + 80).toFixed(0) + '%';
                document.getElementById('essPower').textContent = (Math.random() * 2 + 1.5).toFixed(1) + ' kW';
                document.getElementById('essEfficiency').textContent = (Math.random() * 5 + 92).toFixed(1) + '%';

                // 발전량 데이터 업데이트
                document.getElementById('solarGen').textContent = (Math.random() * 2 + 2.5).toFixed(1) + ' kW';
                document.getElementById('windGen').textContent = (Math.random() * 1.5 + 1.2).toFixed(1) + ' kW';
                document.getElementById('fuelCell').textContent = (Math.random() * 0.5 + 0.3).toFixed(1) + ' kW';

                // 환경 센서 데이터 업데이트
                document.getElementById('temperature').textContent = (Math.random() * 10 + 20).toFixed(1) + '°C';
                document.getElementById('humidity').textContent = (Math.random() * 20 + 50).toFixed(0) + '%';
                document.getElementById('windSpeed').textContent = (Math.random() * 15 + 5).toFixed(0) + ' km/h';
                document.getElementById('solarIrradiance').textContent = (Math.random() * 300 + 700).toFixed(0) + ' W/m²';
            }}

            // 차트 초기화
            function initCharts() {{
                // 공급 차트
                const supplyCtx = document.getElementById('supplyChart').getContext('2d');
                new Chart(supplyCtx, {{
                    type: 'doughnut',
                    data: {{
                        labels: ['Solar', 'Wind', 'Fuel Cell'],
                        datasets: [{{
                            data: [3.2, 1.8, 0.5],
                            backgroundColor: ['#ffc107', '#17a2b8', '#007bff']
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {{
                            legend: {{
                                position: 'bottom'
                            }}
                        }}
                    }}
                }});

                // 센서 차트
                const sensorCtx = document.getElementById('sensorChart').getContext('2d');
                new Chart(sensorCtx, {{
                    type: 'line',
                    data: {{
                        labels: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00'],
                        datasets: [{{
                            label: 'Temperature (°C)',
                            data: [18, 16, 20, 25, 28, 22],
                            borderColor: '#dc3545',
                            backgroundColor: 'rgba(220, 53, 69, 0.1)',
                            tension: 0.4
                        }}, {{
                            label: 'Humidity (%)',
                            data: [70, 75, 60, 55, 50, 65],
                            borderColor: '#17a2b8',
                            backgroundColor: 'rgba(23, 162, 184, 0.1)',
                            tension: 0.4
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {{
                            y: {{
                                beginAtZero: true
                            }}
                        }}
                    }}
                }});

                // 실증 사이트 차트
                const demoSitesCtx = document.getElementById('demoSitesChart').getContext('2d');
                new Chart(demoSitesCtx, {{
                    type: 'bar',
                    data: {{
                        labels: ['Oulu University', 'KTH University', 'BEIA', 'Triaena/OTE'],
                        datasets: [{{
                            label: '에너지 효율 (%)',
                            data: [92.3, 94.8, 89.5, 91.7],
                            backgroundColor: ['#007bff', '#28a745', '#ffc107', '#dc3545'],
                            borderColor: ['#0056b3', '#1e7e34', '#e0a800', '#bd2130'],
                            borderWidth: 2
                        }}, {{
                            label: '절약률 (%)',
                            data: [15.7, 18.2, 12.4, 16.9],
                            backgroundColor: ['rgba(0, 123, 255, 0.6)', 'rgba(40, 167, 69, 0.6)', 'rgba(255, 193, 7, 0.6)', 'rgba(220, 53, 69, 0.6)'],
                            borderColor: ['#0056b3', '#1e7e34', '#e0a800', '#bd2130'],
                            borderWidth: 2
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {{
                            y: {{
                                beginAtZero: true,
                                max: 100,
                                title: {{
                                    display: true,
                                    text: '성능 지표 (%)'
                                }}
                            }},
                            x: {{
                                title: {{
                                    display: true,
                                    text: '실증 사이트'
                                }}
                            }}
                        }},
                        plugins: {{
                            legend: {{
                                display: true,
                                position: 'top'
                            }},
                            title: {{
                                display: true,
                                text: '실증 사이트별 성능 비교'
                            }}
                        }}
                    }}
                }});
            }}

            // 페이지 로드 시 초기화
            document.addEventListener('DOMContentLoaded', function() {{
                initCharts();
                updateRealtimeData();
                
                // 5초마다 데이터 업데이트
                setInterval(updateRealtimeData, 5000);
            }});
        </script>
    </body>
    </html>
    """

@web_app.get("/data-collection", response_class=HTMLResponse)
async def data_collection_page(request: Request, lang: str = Query("ko", description="Language code")):
    """Energy Supply Monitoring with Advanced Weather Analysis 페이지"""
    # 언어 설정
    if lang not in get_available_languages():
        lang = "ko"
    
    return f"""
    <!DOCTYPE html>
    <html lang="{lang}">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{t('energySupply.title', lang)}</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <script src="https://cdn.jsdelivr.net/npm/chart.js?v=2.0"></script>
        <style>
            body {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }}
            .dashboard-card {{
                background: rgba(255, 255, 255, 0.95);
                border-radius: 15px;
                padding: 20px;
                margin-bottom: 20px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }}
            .metric-card {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border-radius: 10px;
                padding: 15px;
                margin-bottom: 15px;
            }}
            .weather-card {{
                background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
                color: white;
                border-radius: 10px;
                padding: 15px;
                margin-bottom: 15px;
            }}
            .metric-value {{
                font-size: 2rem;
                font-weight: bold;
                margin-bottom: 5px;
            }}
            .metric-label {{
                font-size: 0.9rem;
                opacity: 0.9;
            }}
            .chart-container {{
                max-height: 300px;
            }}
            .status-indicator {{
                width: 12px;
                height: 12px;
                border-radius: 50%;
                display: inline-block;
                margin-right: 8px;
            }}
            .status-online {{ background-color: #28a745; }}
            .status-offline {{ background-color: #dc3545; }}
            .status-warning {{ background-color: #ffc107; }}
            .weather-icon {{
                font-size: 3rem;
                margin-bottom: 10px;
            }}
            .correlation-card {{
                background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
                color: #333;
                border-radius: 10px;
                padding: 15px;
                margin-bottom: 15px;
            }}
        </style>
    </head>
    <body>
        {generate_navigation(lang)}

        <div class="container-fluid mt-4">
            <!-- 실시간 에너지 공급 현황 -->
            <div class="row">
                <div class="col-12">
                    <div class="dashboard-card">
                        <h4><i class="fas fa-chart-line"></i> 실시간 에너지 공급 현황</h4>
                        <div class="row">
                            <div class="col-md-3">
                                <div class="metric-card">
                                    <div class="metric-value" id="totalGeneration">5.2 kW</div>
                                    <div class="metric-label">총 발전량</div>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="metric-card">
                                    <div class="metric-value" id="solarGeneration">3.2 kW</div>
                                    <div class="metric-label">태양광 발전</div>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="metric-card">
                                    <div class="metric-value" id="essGeneration">2.1 kW</div>
                                    <div class="metric-label">ESS 발전</div>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="metric-card">
                                    <div class="metric-value" id="systemEfficiency">94.2%</div>
                                    <div class="metric-label">시스템 효율</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 에너지 공급 예측 분석 -->
            <div class="row">
                <div class="col-12">
                    <div class="dashboard-card">
                        <h4><i class="fas fa-crystal-ball"></i> 에너지 공급 예측 분석</h4>
                        <div class="row">
                            <div class="col-md-3">
                                <div class="weather-card text-center">
                                    <h6>1시간 후 예측</h6>
                                    <div class="metric-value" id="supplyPrediction1h">5.8 kW</div>
                                    <div class="metric-label">예측 공급량</div>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="weather-card text-center">
                                    <h6>6시간 후 예측</h6>
                                    <div class="metric-value" id="supplyPrediction6h">4.2 kW</div>
                                    <div class="metric-label">예측 공급량</div>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="weather-card text-center">
                                    <h6>24시간 후 예측</h6>
                                    <div class="metric-value" id="supplyPrediction24h">6.1 kW</div>
                                    <div class="metric-label">예측 공급량</div>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="weather-card text-center">
                                    <h6>예측 정확도</h6>
                                    <div class="metric-value" id="supplyPredictionAccuracy">96.8%</div>
                                    <div class="metric-label">AI 예측 정확도</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 고급 날씨 정보 분석 -->
            <div class="row">
                <div class="col-12">
                    <div class="dashboard-card">
                        <h4><i class="fas fa-cloud-sun"></i> Advanced Weather Analysis System</h4>
                        <div class="row">
                            <div class="col-md-2">
                                <div class="weather-card text-center">
                                    <div class="weather-icon" id="weatherIcon">☀️</div>
                                    <div class="metric-value" id="temperature">23°C</div>
                                    <div class="metric-label">Temperature</div>
                                </div>
                            </div>
                            <div class="col-md-2">
                                <div class="weather-card text-center">
                                    <div class="weather-icon">💧</div>
                                    <div class="metric-value" id="humidity">65%</div>
                                    <div class="metric-label">Humidity</div>
                                </div>
                            </div>
                            <div class="col-md-2">
                                <div class="weather-card text-center">
                                    <div class="weather-icon">💨</div>
                                    <div class="metric-value" id="windSpeed">12 km/h</div>
                                    <div class="metric-label">Wind Speed</div>
                                </div>
                            </div>
                            <div class="col-md-2">
                                <div class="weather-card text-center">
                                    <div class="weather-icon">☀️</div>
                                    <div class="metric-value" id="solarIrradiance">850 W/m²</div>
                                    <div class="metric-label">Solar Irradiance</div>
                                </div>
                            </div>
                            <div class="col-md-2">
                                <div class="weather-card text-center">
                                    <div class="weather-icon">🌧️</div>
                                    <div class="metric-value" id="precipitation">0 mm</div>
                                    <div class="metric-label">Precipitation</div>
                                </div>
                            </div>
                            <div class="col-md-2">
                                <div class="weather-card text-center">
                                    <div class="weather-icon">👁️</div>
                                    <div class="metric-value" id="visibility">10 km</div>
                                    <div class="metric-label">Visibility</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 에너지-날씨 상관관계 분석 -->
            <div class="row">
                <div class="col-lg-6">
                    <div class="dashboard-card">
                        <h5><i class="fas fa-chart-area"></i> Energy Generation Trends</h5>
                        <canvas id="generationChart" class="chart-container"></canvas>
                    </div>
                </div>
                <div class="col-lg-6">
                    <div class="dashboard-card">
                        <h5><i class="fas fa-thermometer-half"></i> Weather Conditions</h5>
                        <canvas id="weatherChart" class="chart-container"></canvas>
                    </div>
                </div>
            </div>

            <!-- 에너지-날씨 상관관계 분석 -->
            <div class="row">
                <div class="col-lg-4">
                    <div class="dashboard-card">
                        <h5><i class="fas fa-chart-pie"></i> Energy Mix Distribution</h5>
                        <canvas id="energyMixChart" class="chart-container"></canvas>
                    </div>
                </div>
                <div class="col-lg-4">
                    <div class="dashboard-card">
                        <h5><i class="fas fa-link"></i> Energy-Weather Correlation</h5>
                        <div class="correlation-card">
                            <h6><i class="fas fa-sun"></i> Solar vs Irradiance</h6>
                            <div class="mb-2">
                                <small>Correlation: <strong id="solarCorrelation">0.87</strong></small>
                                <div class="progress">
                                    <div class="progress-bar bg-warning" style="width: 87%"></div>
                                </div>
                            </div>
                            <h6><i class="fas fa-battery-half"></i> ESS vs Efficiency</h6>
                            <div class="mb-2">
                                <small>Correlation: <strong id="essCorrelation">0.92</strong></small>
                                <div class="progress">
                                    <div class="progress-bar bg-info" style="width: 92%"></div>
                                </div>
                            </div>
                            <h6><i class="fas fa-thermometer-half"></i> Efficiency vs Temperature</h6>
                            <div class="mb-2">
                                <small>Correlation: <strong id="tempCorrelation">-0.34</strong></small>
                                <div class="progress">
                                    <div class="progress-bar bg-danger" style="width: 34%"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-lg-4">
                    <div class="dashboard-card">
                        <h5><i class="fas fa-chart-line"></i> Weather Impact Analysis</h5>
                        <canvas id="impactChart" class="chart-container"></canvas>
                    </div>
                </div>
            </div>

            <!-- 시스템 상태 모니터링 -->
            <div class="row">
                <div class="col-12">
                    <div class="dashboard-card">
                        <h5><i class="fas fa-cogs"></i> System Status Monitoring</h5>
                        <div class="row">
                            <div class="col-md-3">
                                <h6>Solar Panel Array</h6>
                                <div class="mb-2">
                                    <span class="status-indicator status-online"></span>
                                    <span>Panel 1-10: <strong>Online</strong></span>
                                </div>
                                <div class="mb-2">
                                    <span class="status-indicator status-online"></span>
                                    <span>Panel 11-20: <strong>Online</strong></span>
                                </div>
                                <div class="mb-2">
                                    <span class="status-indicator status-warning"></span>
                                    <span>Panel 21-25: <strong>Maintenance</strong></span>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <h6>Wind Turbine System</h6>
                                <div class="mb-2">
                                    <span class="status-indicator status-online"></span>
                                    <span>Turbine 1: <strong>Online</strong></span>
                                </div>
                                <div class="mb-2">
                                    <span class="status-indicator status-online"></span>
                                    <span>Turbine 2: <strong>Online</strong></span>
                                </div>
                                <div class="mb-2">
                                    <span class="status-indicator status-offline"></span>
                                    <span>Turbine 3: <strong>Offline</strong></span>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <h6>Energy Storage System</h6>
                                <div class="mb-2">
                                    <span class="status-indicator status-online"></span>
                                    <span>Battery Bank 1: <strong>Online</strong></span>
                                </div>
                                <div class="mb-2">
                                    <span class="status-indicator status-online"></span>
                                    <span>Battery Bank 2: <strong>Online</strong></span>
                                </div>
                                <div class="mb-2">
                                    <span class="status-indicator status-online"></span>
                                    <span>Inverter System: <strong>Online</strong></span>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <h6>Weather Sensors</h6>
                                <div class="mb-2">
                                    <span class="status-indicator status-online"></span>
                                    <span>Temperature: <strong>Online</strong></span>
                                </div>
                                <div class="mb-2">
                                    <span class="status-indicator status-online"></span>
                                    <span>Wind Speed: <strong>Online</strong></span>
                                </div>
                                <div class="mb-2">
                                    <span class="status-indicator status-online"></span>
                                    <span>Solar Sensor: <strong>Online</strong></span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 날씨 예측 및 에너지 예측 -->
            <div class="row">
                <div class="col-12">
                    <div class="dashboard-card">
                        <h5><i class="fas fa-crystal-ball"></i> Weather Forecast & Energy Prediction</h5>
                        <div class="row">
                            <div class="col-md-6">
                                <h6>Next 24 Hours Weather Forecast</h6>
                                <div class="table-responsive">
                                    <table class="table table-sm">
                                        <thead>
                                            <tr>
                                                <th>Time</th>
                                                <th>Weather</th>
                                                <th>Temp</th>
                                                <th>Wind</th>
                                                <th>Solar</th>
                                            </tr>
                                        </thead>
                                        <tbody id="weatherForecast">
                                            <tr>
                                                <td>00:00</td>
                                                <td>🌙 Clear</td>
                                                <td>18°C</td>
                                                <td>8 km/h</td>
                                                <td>0 W/m²</td>
                                            </tr>
                                            <tr>
                                                <td>06:00</td>
                                                <td>🌅 Sunny</td>
                                                <td>22°C</td>
                                                <td>12 km/h</td>
                                                <td>450 W/m²</td>
                                            </tr>
                                            <tr>
                                                <td>12:00</td>
                                                <td>☀️ Sunny</td>
                                                <td>28°C</td>
                                                <td>15 km/h</td>
                                                <td>850 W/m²</td>
                                            </tr>
                                            <tr>
                                                <td>18:00</td>
                                                <td>🌤️ Partly Cloudy</td>
                                                <td>25°C</td>
                                                <td>10 km/h</td>
                                                <td>300 W/m²</td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <h6>Energy Generation Prediction</h6>
                                <div class="table-responsive">
                                    <table class="table table-sm">
                                        <thead>
                                            <tr>
                                                <th>Time</th>
                                                <th>Solar (kW)</th>
                                                <th>ESS (kW)</th>
                                                <th>Total (kW)</th>
                                                <th>Efficiency</th>
                                            </tr>
                                        </thead>
                                        <tbody id="energyPrediction">
                                            <tr>
                                                <td>00:00</td>
                                                <td>0.0</td>
                                                <td>1.2</td>
                                                <td>1.2</td>
                                                <td>92%</td>
                                            </tr>
                                            <tr>
                                                <td>06:00</td>
                                                <td>1.8</td>
                                                <td>1.5</td>
                                                <td>3.3</td>
                                                <td>94%</td>
                                            </tr>
                                            <tr>
                                                <td>12:00</td>
                                                <td>3.5</td>
                                                <td>2.1</td>
                                                <td>5.6</td>
                                                <td>96%</td>
                                            </tr>
                                            <tr>
                                                <td>18:00</td>
                                                <td>1.2</td>
                                                <td>1.8</td>
                                                <td>3.0</td>
                                                <td>93%</td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
        <script>
            // 실시간 데이터 업데이트
            function updateRealtimeData() {{
                // 발전량 데이터 업데이트
                const solarGen = (Math.random() * 2 + 2.5).toFixed(1);
                const essGen = (Math.random() * 1.5 + 1.2).toFixed(1);
                const totalGen = (parseFloat(solarGen) + parseFloat(essGen)).toFixed(1);
                const efficiency = (Math.random() * 5 + 92).toFixed(1);

                document.getElementById('totalGeneration').textContent = totalGen + ' kW';
                document.getElementById('solarGeneration').textContent = solarGen + ' kW';
                document.getElementById('essGeneration').textContent = essGen + ' kW';
                document.getElementById('systemEfficiency').textContent = efficiency + '%';

                // 공급 예측 데이터 업데이트
                const supplyPrediction1h = (Math.random() * 1.5 + 5.0).toFixed(1);
                const supplyPrediction6h = (Math.random() * 2.0 + 3.5).toFixed(1);
                const supplyPrediction24h = (Math.random() * 2.5 + 5.5).toFixed(1);
                const supplyPredictionAccuracy = (Math.random() * 3 + 95).toFixed(1);

                document.getElementById('supplyPrediction1h').textContent = supplyPrediction1h + ' kW';
                document.getElementById('supplyPrediction6h').textContent = supplyPrediction6h + ' kW';
                document.getElementById('supplyPrediction24h').textContent = supplyPrediction24h + ' kW';
                document.getElementById('supplyPredictionAccuracy').textContent = supplyPredictionAccuracy + '%';

                // 날씨 데이터 업데이트
                const temperature = (Math.random() * 15 + 15).toFixed(0);
                const humidity = (Math.random() * 30 + 40).toFixed(0);
                const windSpeed = (Math.random() * 20 + 5).toFixed(0);
                const solarIrradiance = (Math.random() * 500 + 300).toFixed(0);
                const precipitation = (Math.random() * 5).toFixed(1);
                const visibility = (Math.random() * 5 + 8).toFixed(0);

                document.getElementById('temperature').textContent = temperature + '°C';
                document.getElementById('humidity').textContent = humidity + '%';
                document.getElementById('windSpeed').textContent = windSpeed + ' km/h';
                document.getElementById('solarIrradiance').textContent = solarIrradiance + ' W/m²';
                document.getElementById('precipitation').textContent = precipitation + ' mm';
                document.getElementById('visibility').textContent = visibility + ' km';

                // 날씨 아이콘 업데이트
                const weatherIcons = ['☀️', '⛅', '☁️', '🌧️', '⛈️', '🌩️'];
                const randomIcon = weatherIcons[Math.floor(Math.random() * weatherIcons.length)];
                document.getElementById('weatherIcon').textContent = randomIcon;

                // 상관관계 업데이트
                const solarCorr = (Math.random() * 0.2 + 0.8).toFixed(2);
                const windCorr = (Math.random() * 0.2 + 0.8).toFixed(2);
                const tempCorr = (Math.random() * 0.4 - 0.2).toFixed(2);

                document.getElementById('solarCorrelation').textContent = solarCorr;
                document.getElementById('essCorrelation').textContent = windCorr;
                document.getElementById('tempCorrelation').textContent = tempCorr;

                // 진행률 바 업데이트
                document.querySelector('.progress-bar.bg-warning').style.width = (solarCorr * 100) + '%';
                document.querySelector('.progress-bar.bg-info').style.width = (windCorr * 100) + '%';
                document.querySelector('.progress-bar.bg-danger').style.width = (Math.abs(tempCorr) * 100) + '%';
            }}

            // 차트 초기화
            function initCharts() {{
                // 발전량 트렌드 차트
                const generationCtx = document.getElementById('generationChart').getContext('2d');
                new Chart(generationCtx, {{
                    type: 'line',
                    data: {{
                        labels: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00'],
                        datasets: [{{
                            label: 'Solar Generation',
                            data: [0, 0, 1.5, 3.2, 2.8, 0.5],
                            borderColor: '#ffc107',
                            backgroundColor: 'rgba(255, 193, 7, 0.1)',
                            tension: 0.4
                        }}, {{
                            label: 'ESS Generation',
                            data: [1.2, 1.8, 1.5, 1.0, 1.5, 1.8],
                            borderColor: '#17a2b8',
                            backgroundColor: 'rgba(23, 162, 184, 0.1)',
                            tension: 0.4
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {{
                            y: {{
                                beginAtZero: true,
                                title: {{
                                    display: true,
                                    text: 'Power (kW)'
                                }}
                            }}
                        }}
                    }}
                }});

                // 날씨 조건 차트
                const weatherCtx = document.getElementById('weatherChart').getContext('2d');
                new Chart(weatherCtx, {{
                    type: 'line',
                    data: {{
                        labels: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00'],
                        datasets: [{{
                            label: 'Temperature (°C)',
                            data: [18, 16, 20, 25, 28, 22],
                            borderColor: '#dc3545',
                            backgroundColor: 'rgba(220, 53, 69, 0.1)',
                            tension: 0.4,
                            yAxisID: 'y'
                        }}, {{
                            label: 'Wind Speed (km/h)',
                            data: [8, 12, 15, 18, 12, 10],
                            borderColor: '#17a2b8',
                            backgroundColor: 'rgba(23, 162, 184, 0.1)',
                            tension: 0.4,
                            yAxisID: 'y1'
                        }}, {{
                            label: 'Solar Irradiance (W/m²)',
                            data: [0, 0, 300, 850, 600, 100],
                            borderColor: '#ffc107',
                            backgroundColor: 'rgba(255, 193, 7, 0.1)',
                            tension: 0.4,
                            yAxisID: 'y2'
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {{
                            y: {{
                                type: 'linear',
                                display: true,
                                position: 'left',
                                title: {{
                                    display: true,
                                    text: 'Temperature (°C)'
                                }}
                            }},
                            y1: {{
                                type: 'linear',
                                display: true,
                                position: 'right',
                                title: {{
                                    display: true,
                                    text: 'Wind Speed (km/h)'
                                }},
                                grid: {{
                                    drawOnChartArea: false,
                                }},
                            }},
                            y2: {{
                                type: 'linear',
                                display: false,
                            }}
                        }}
                    }}
                }});

                // 에너지 믹스 차트
                const energyMixCtx = document.getElementById('energyMixChart').getContext('2d');
                new Chart(energyMixCtx, {{
                    type: 'doughnut',
                    data: {{
                        labels: ['Solar', 'ESS', 'Storage'],
                        datasets: [{{
                            data: [3.2, 1.8, 0.2],
                            backgroundColor: ['#ffc107', '#17a2b8', '#28a745']
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {{
                            legend: {{
                                position: 'bottom'
                            }}
                        }}
                    }}
                }});

                // 날씨 영향 분석 차트
                const impactCtx = document.getElementById('impactChart').getContext('2d');
                new Chart(impactCtx, {{
                    type: 'bar',
                    data: {{
                        labels: ['Solar', 'ESS', 'Efficiency', 'Storage'],
                        datasets: [{{
                            label: 'Weather Impact (%)',
                            data: [85, 92, -15, 5],
                            backgroundColor: ['#ffc107', '#17a2b8', '#dc3545', '#28a745']
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {{
                            y: {{
                                beginAtZero: true,
                                title: {{
                                    display: true,
                                    text: 'Impact (%)'
                                }}
                            }}
                        }}
                    }}
                }});
            }}

            // 페이지 로드 시 초기화
            document.addEventListener('DOMContentLoaded', function() {{
                initCharts();
                updateRealtimeData();
                
                // 5초마다 데이터 업데이트
                setInterval(updateRealtimeData, 5000);
            }});
        </script>
    </body>
    </html>
    """

@web_app.get("/data-analysis", response_class=HTMLResponse)
async def data_analysis_page(request: Request, lang: str = Query("ko", description="Language code")):
    """시설 모니터링 및 데이터 분석 페이지"""
    # 언어 설정
    if lang not in get_available_languages():
        lang = "ko"
    
    return f"""
    <!DOCTYPE html>
    <html lang="{lang}">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{t('energyDemand.title', lang)}</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <script src="https://cdn.jsdelivr.net/npm/chart.js?v=2.0"></script>
        <style>
            body {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }}
            .monitoring-card {{
                background: rgba(255, 255, 255, 0.95);
                border-radius: 15px;
                padding: 20px;
                margin-bottom: 20px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }}
            .facility-info {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border-radius: 10px;
                padding: 15px;
                margin-bottom: 15px;
            }}
            .sensor-card {{
                background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
                color: #333;
                border-radius: 10px;
                padding: 15px;
                margin-bottom: 15px;
            }}
            .power-card {{
                background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
                color: #333;
                border-radius: 10px;
                padding: 15px;
                margin-bottom: 15px;
            }}
            .event-card {{
                background: rgba(255, 255, 255, 0.9);
                border-radius: 10px;
                padding: 15px;
                margin-bottom: 15px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }}
            .calendar-card {{
                background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
                color: #333;
                border-radius: 10px;
                padding: 15px;
                margin-bottom: 15px;
            }}
            .metric-value {{
                font-size: 2rem;
                font-weight: bold;
                margin-bottom: 5px;
            }}
            .metric-label {{
                font-size: 0.9rem;
                opacity: 0.9;
            }}
            .chart-container {{
                max-height: 300px;
            }}
            .status-indicator {{
                width: 12px;
                height: 12px;
                border-radius: 50%;
                display: inline-block;
                margin-right: 8px;
            }}
            .status-online {{ background-color: #28a745; }}
            .status-offline {{ background-color: #dc3545; }}
            .status-warning {{ background-color: #ffc107; }}
            .event-timeline {{
                max-height: 400px;
                overflow-y: auto;
            }}
            .event-item {{
                border-left: 3px solid #007bff;
                padding-left: 15px;
                margin-bottom: 15px;
                background: rgba(255, 255, 255, 0.8);
                border-radius: 5px;
                padding: 10px;
            }}
            .event-time {{
                font-size: 0.8rem;
                color: #666;
                font-weight: bold;
            }}
            .event-content {{
                margin-top: 5px;
            }}
            .memo-input {{
                background: rgba(255, 255, 255, 0.9);
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 10px;
                margin-top: 10px;
            }}
        </style>
    </head>
    <body>
        {generate_navigation(lang)}

        <div class="container-fluid mt-4">
            <!-- 에너지 수요 현황 -->
            <div class="row mb-4">
                <div class="col-12">
                    <div class="facility-info">
                        <h4><i class="fas fa-bolt"></i> 실시간 에너지 수요 현황</h4>
                        <div class="row">
                            <div class="col-md-3">
                                <h6>현재 수요</h6>
                                <p><strong id="currentDemand">1,250 kW</strong></p>
                            </div>
                            <div class="col-md-3">
                                <h6>피크 수요</h6>
                                <p><strong id="peakDemand">1,450 kW</strong></p>
                            </div>
                            <div class="col-md-3">
                                <h6>예측 수요 (1시간 후)</h6>
                                <p><strong id="predictedDemand">1,320 kW</strong></p>
                            </div>
                            <div class="col-md-3">
                                <h6>수요 증가율</h6>
                                <p><span class="status-indicator status-warning"></span><strong id="demandGrowth">+5.6%</strong></p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 전자기기별 수요 분석 -->
            <div class="row mb-4">
                <div class="col-12">
                    <div class="monitoring-card">
                        <h5><i class="fas fa-microchip"></i> 전자기기별 에너지 수요 분석</h5>
                        <div class="row">
                            <div class="col-md-3">
                                <div class="sensor-card text-center">
                                    <h6>HVAC 시스템</h6>
                                    <div class="metric-value" id="hvacDemand">450 kW</div>
                                    <div class="metric-label">냉난방 수요</div>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="sensor-card text-center">
                                    <h6>조명 시스템</h6>
                                    <div class="metric-value" id="lightingDemand">180 kW</div>
                                    <div class="metric-label">조명 수요</div>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="sensor-card text-center">
                                    <h6>IT 장비</h6>
                                    <div class="metric-value" id="itDemand">320 kW</div>
                                    <div class="metric-label">IT 장비 수요</div>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="sensor-card text-center">
                                    <h6>기타 장비</h6>
                                    <div class="metric-value" id="otherDemand">300 kW</div>
                                    <div class="metric-label">기타 장비 수요</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 수요 예측 분석 -->
            <div class="row mb-4">
                <div class="col-12">
                    <div class="monitoring-card">
                        <h5><i class="fas fa-crystal-ball"></i> 에너지 수요 예측 분석</h5>
                        <div class="row">
                            <div class="col-md-3">
                                <div class="power-card text-center">
                                    <h6>1시간 후 예측</h6>
                                    <div class="metric-value" id="prediction1h">1,320 kW</div>
                                    <div class="metric-label">예측 수요량</div>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="power-card text-center">
                                    <h6>6시간 후 예측</h6>
                                    <div class="metric-value" id="prediction6h">1,180 kW</div>
                                    <div class="metric-label">예측 수요량</div>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="power-card text-center">
                                    <h6>24시간 후 예측</h6>
                                    <div class="metric-value" id="prediction24h">1,410 kW</div>
                                    <div class="metric-label">예측 수요량</div>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="power-card text-center">
                                    <h6>예측 정확도</h6>
                                    <div class="metric-value" id="predictionAccuracy">94.2%</div>
                                    <div class="metric-label">AI 예측 정확도</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 수요-공급 매칭 분석 -->
            <div class="row mb-4">
                <div class="col-lg-8">
                    <div class="monitoring-card">
                        <h5><i class="fas fa-chart-line"></i> 수요-공급 매칭 분석</h5>
                        <canvas id="demandSupplyChart" class="chart-container"></canvas>
                    </div>
                </div>
                <div class="col-lg-4">
                    <div class="monitoring-card">
                        <h5><i class="fas fa-percentage"></i> 매칭율 분석</h5>
                        <div class="calendar-card">
                            <h6>실시간 매칭 현황</h6>
                            <div class="event-timeline" id="matchingStatus">
                                <div class="event-item">
                                    <div class="event-time">현재</div>
                                    <div class="event-content">
                                        <strong>매칭율: 87.3%</strong><br>
                                        <small>수요: 1,250 kW / 공급: 1,432 kW</small>
                                    </div>
                                </div>
                                <div class="event-item">
                                    <div class="event-time">1시간 후</div>
                                    <div class="event-content">
                                        <strong>예측 매칭율: 92.1%</strong><br>
                                        <small>예측 수요: 1,320 kW / 예측 공급: 1,434 kW</small>
                                    </div>
                                </div>
                                <div class="event-item">
                                    <div class="event-time">6시간 후</div>
                                    <div class="event-content">
                                        <strong>예측 매칭율: 78.5%</strong><br>
                                        <small>예측 수요: 1,180 kW / 예측 공급: 1,503 kW</small>
                                    </div>
                                </div>
                            </div>
                            <button class="btn btn-success btn-sm mt-2" onclick="optimizeMatching()">
                                <i class="fas fa-cogs"></i> 매칭 최적화
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 전자기기 시뮬레이션 및 동적 제어 -->
            <div class="row mb-4">
                <div class="col-lg-6">
                    <div class="monitoring-card">
                        <h5><i class="fas fa-desktop"></i> 전자기기 시뮬레이션</h5>
                        <div class="mb-3">
                            <h6>기기 선택:</h6>
                            <select class="form-select" id="deviceSelect" onchange="simulateDevice()">
                                <option value="">기기를 선택하세요</option>
                                <option value="hvac">HVAC 시스템 (450 kW)</option>
                                <option value="lighting">조명 시스템 (180 kW)</option>
                                <option value="it">IT 장비 (320 kW)</option>
                                <option value="elevator">엘리베이터 (150 kW)</option>
                                <option value="pump">펌프 시스템 (200 kW)</option>
                                <option value="security">보안 시스템 (80 kW)</option>
                            </select>
                        </div>
                        <div class="event-timeline" id="simulationResults">
                            <div class="event-item">
                                <div class="event-time">시뮬레이션 결과</div>
                                <div class="event-content">
                                    <strong>기기를 선택하면 수요 예측이 표시됩니다</strong><br>
                                    <small>선택한 기기의 에너지 소비 패턴을 분석하여 수요를 예측합니다.</small>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-lg-6">
                    <div class="monitoring-card">
                        <h5><i class="fas fa-cogs"></i> 동적 제어 평가</h5>
                        <div class="mb-3">
                            <h6>제어 시나리오:</h6>
                            <div class="btn-group w-100" role="group">
                                <button type="button" class="btn btn-outline-primary btn-sm" onclick="evaluateControl('peak')">피크 제어</button>
                                <button type="button" class="btn btn-outline-success btn-sm" onclick="evaluateControl('load')">부하 분산</button>
                                <button type="button" class="btn btn-outline-warning btn-sm" onclick="evaluateControl('efficiency')">효율 최적화</button>
                            </div>
                        </div>
                        <div class="event-timeline" id="controlResults">
                            <div class="event-item">
                                <div class="event-time">제어 평가 결과</div>
                                <div class="event-content">
                                    <strong>제어 시나리오를 선택하면 평가 결과가 표시됩니다</strong><br>
                                    <small>동적 제어의 효과와 가능성을 분석합니다.</small>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
        <script>
            // 실시간 데이터 업데이트
            function updateRealtimeData() {{
                // 에너지 수요 데이터 업데이트
                const currentDemand = (Math.random() * 200 + 1200).toFixed(0);
                const peakDemand = (Math.random() * 100 + 1400).toFixed(0);
                const predictedDemand = (Math.random() * 150 + 1300).toFixed(0);
                const demandGrowth = (Math.random() * 10 - 2).toFixed(1);

                document.getElementById('currentDemand').textContent = currentDemand + ' kW';
                document.getElementById('peakDemand').textContent = peakDemand + ' kW';
                document.getElementById('predictedDemand').textContent = predictedDemand + ' kW';
                document.getElementById('demandGrowth').textContent = (demandGrowth > 0 ? '+' : '') + demandGrowth + '%';

                // 전자기기별 수요 업데이트
                const hvacDemand = (Math.random() * 100 + 400).toFixed(0);
                const lightingDemand = (Math.random() * 50 + 150).toFixed(0);
                const itDemand = (Math.random() * 80 + 280).toFixed(0);
                const otherDemand = (Math.random() * 100 + 250).toFixed(0);

                document.getElementById('hvacDemand').textContent = hvacDemand + ' kW';
                document.getElementById('lightingDemand').textContent = lightingDemand + ' kW';
                document.getElementById('itDemand').textContent = itDemand + ' kW';
                document.getElementById('otherDemand').textContent = otherDemand + ' kW';

                // 수요 예측 업데이트
                const prediction1h = (Math.random() * 150 + 1300).toFixed(0);
                const prediction6h = (Math.random() * 200 + 1100).toFixed(0);
                const prediction24h = (Math.random() * 300 + 1300).toFixed(0);
                const predictionAccuracy = (Math.random() * 5 + 92).toFixed(1);

                document.getElementById('prediction1h').textContent = prediction1h + ' kW';
                document.getElementById('prediction6h').textContent = prediction6h + ' kW';
                document.getElementById('prediction24h').textContent = prediction24h + ' kW';
                document.getElementById('predictionAccuracy').textContent = predictionAccuracy + '%';
            }}

            // 수요-공급 매칭 차트 초기화
            function initDemandSupplyChart() {{
                const ctx = document.getElementById('demandSupplyChart').getContext('2d');
                const hours = [];
                const demandData = [];
                const supplyData = [];
                const matchingData = [];
                
                for (let i = 0; i < 24; i++) {{
                    hours.push(i.toString().padStart(2, '0') + ':00');
                    const demand = Math.random() * 200 + 1200;
                    const supply = Math.random() * 300 + 1300;
                    const matching = (Math.min(demand, supply) / Math.max(demand, supply) * 100);
                    
                    demandData.push(demand);
                    supplyData.push(supply);
                    matchingData.push(matching);
                }}
                
                new Chart(ctx, {{
                    type: 'line',
                    data: {{
                        labels: hours,
                        datasets: [{{
                            label: '에너지 수요 (kW)',
                            data: demandData,
                            borderColor: '#ff6b6b',
                            backgroundColor: 'rgba(255, 107, 107, 0.1)',
                            tension: 0.4,
                            yAxisID: 'y'
                        }}, {{
                            label: '에너지 공급 (kW)',
                            data: supplyData,
                            borderColor: '#4ecdc4',
                            backgroundColor: 'rgba(78, 205, 196, 0.1)',
                            tension: 0.4,
                            yAxisID: 'y'
                        }}, {{
                            label: '매칭율 (%)',
                            data: matchingData,
                            borderColor: '#ffa726',
                            backgroundColor: 'rgba(255, 167, 38, 0.1)',
                            tension: 0.4,
                            yAxisID: 'y1'
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {{
                            y: {{
                                type: 'linear',
                                display: true,
                                position: 'left',
                                title: {{
                                    display: true,
                                    text: '에너지 (kW)'
                                }}
                            }},
                            y1: {{
                                type: 'linear',
                                display: true,
                                position: 'right',
                                title: {{
                                    display: true,
                                    text: '매칭율 (%)'
                                }},
                                min: 0,
                                max: 100,
                                grid: {{
                                    drawOnChartArea: false,
                                }},
                            }}
                        }},
                        plugins: {{
                            legend: {{
                                display: true,
                                position: 'top'
                            }}
                        }}
                    }}
                }});
            }}

            // 매칭 최적화
            function optimizeMatching() {{
                const matchingStatus = document.getElementById('matchingStatus');
                const newEvent = document.createElement('div');
                newEvent.className = 'event-item';
                newEvent.innerHTML = `
                    <div class="event-time">${{new Date().toLocaleTimeString()}}</div>
                    <div class="event-content">
                        <strong>매칭 최적화 실행</strong><br>
                        <small>수요-공급 매칭 알고리즘이 최적화되었습니다. 매칭율이 5.2% 향상되었습니다.</small>
                    </div>
                `;
                matchingStatus.insertBefore(newEvent, matchingStatus.firstChild);
            }}

            // 전자기기 시뮬레이션
            function simulateDevice() {{
                const deviceSelect = document.getElementById('deviceSelect');
                const selectedDevice = deviceSelect.value;
                const simulationResults = document.getElementById('simulationResults');
                
                if (!selectedDevice) {{
                    simulationResults.innerHTML = `
                        <div class="event-item">
                            <div class="event-time">시뮬레이션 결과</div>
                            <div class="event-content">
                                <strong>기기를 선택하면 수요 예측이 표시됩니다</strong><br>
                                <small>선택한 기기의 에너지 소비 패턴을 분석하여 수요를 예측합니다.</small>
                            </div>
                        </div>
                    `;
                    return;
                }}
                
                const deviceData = {{
                    hvac: {{ name: 'HVAC 시스템', power: 450, pattern: '계절성', efficiency: 85 }},
                    lighting: {{ name: '조명 시스템', power: 180, pattern: '시간대별', efficiency: 92 }},
                    it: {{ name: 'IT 장비', power: 320, pattern: '지속적', efficiency: 88 }},
                    elevator: {{ name: '엘리베이터', power: 150, pattern: '피크시간', efficiency: 90 }},
                    pump: {{ name: '펌프 시스템', power: 200, pattern: '수요기반', efficiency: 87 }},
                    security: {{ name: '보안 시스템', power: 80, pattern: '24시간', efficiency: 95 }}
                }};
                
                const device = deviceData[selectedDevice];
                const predictedDemand = (device.power * (Math.random() * 0.3 + 0.85)).toFixed(0);
                const efficiency = device.efficiency + (Math.random() * 10 - 5);
                
                simulationResults.innerHTML = `
                    <div class="event-item">
                        <div class="event-time">${{new Date().toLocaleTimeString()}}</div>
                        <div class="event-content">
                            <strong>${{device.name}} 시뮬레이션 결과</strong><br>
                            <small>현재 소비: ${{device.power}} kW</small><br>
                            <small>예측 수요: ${{predictedDemand}} kW</small><br>
                            <small>소비 패턴: ${{device.pattern}}</small><br>
                            <small>효율성: ${{efficiency.toFixed(1)}}%</small>
                        </div>
                    </div>
                `;
            }}

            // 동적 제어 평가
            function evaluateControl(scenario) {{
                const controlResults = document.getElementById('controlResults');
                const scenarios = {{
                    peak: {{ name: '피크 제어', savings: 15, efficiency: 8, cost: 5 }},
                    load: {{ name: '부하 분산', savings: 12, efficiency: 6, cost: 3 }},
                    efficiency: {{ name: '효율 최적화', savings: 8, efficiency: 12, cost: 2 }}
                }};
                
                const scenarioData = scenarios[scenario];
                const newEvent = document.createElement('div');
                newEvent.className = 'event-item';
                newEvent.innerHTML = `
                    <div class="event-time">${{new Date().toLocaleTimeString()}}</div>
                    <div class="event-content">
                        <strong>${{scenarioData.name}} 평가 결과</strong><br>
                        <small>에너지 절약: ${{scenarioData.savings}}%</small><br>
                        <small>효율성 향상: ${{scenarioData.efficiency}}%</small><br>
                        <small>비용 절감: ${{scenarioData.cost}}%</small><br>
                        <small>제어 가능성: 높음</small>
                    </div>
                `;
                controlResults.insertBefore(newEvent, controlResults.firstChild);
            }}

            // 초기화
            document.addEventListener('DOMContentLoaded', function() {{
                initDemandSupplyChart();
                updateRealtimeData();
                
                // 5초마다 데이터 업데이트
                setInterval(updateRealtimeData, 5000);
            }});
        </script>
    </body>
    </html>
    """

@web_app.get("/model-testing", response_class=HTMLResponse)
async def model_testing_page(request: Request, lang: str = Query("ko", description="Language code")):
    """MCP 기반 자동화 ML/AI Engine 페이지"""
    # 언어 설정
    if lang not in get_available_languages():
        lang = "ko"
    
    return f"""
    <!DOCTYPE html>
    <html lang="{lang}">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{t('modelTesting.title', lang)}</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <script src="https://cdn.jsdelivr.net/npm/chart.js?v=2.0"></script>
        <style>
            body {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }}
            .mcp-card {{
                background: rgba(255, 255, 255, 0.95);
                border-radius: 15px;
                padding: 20px;
                margin-bottom: 20px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }}
            .process-step {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border-radius: 10px;
                padding: 15px;
                margin-bottom: 15px;
                position: relative;
                overflow: hidden;
            }}
            .process-step::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
                pointer-events: none;
            }}
            .process-step.active {{
                background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
                animation: pulse 2s infinite;
            }}
            .process-step.completed {{
                background: linear-gradient(135deg, #6c757d 0%, #495057 100%);
            }}
            @keyframes pulse {{
                0% {{ transform: scale(1); }}
                50% {{ transform: scale(1.02); }}
                100% {{ transform: scale(1); }}
            }}
            .agent-status {{
                background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
                color: #333;
                border-radius: 10px;
                padding: 15px;
                margin-bottom: 15px;
            }}
            .metric-card {{
                background: rgba(255, 255, 255, 0.9);
                border-radius: 10px;
                padding: 15px;
                margin-bottom: 15px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }}
            .progress-step {{
                height: 8px;
                border-radius: 4px;
                background: rgba(255, 255, 255, 0.3);
                overflow: hidden;
            }}
            .progress-fill {{
                height: 100%;
                background: linear-gradient(90deg, #28a745, #20c997);
                border-radius: 4px;
                transition: width 0.5s ease;
            }}
            .log-container {{
                background: #1e1e1e;
                color: #00ff00;
                border-radius: 10px;
                padding: 15px;
                font-family: 'Courier New', monospace;
                font-size: 0.9rem;
                max-height: 300px;
                overflow-y: auto;
            }}
            .log-entry {{
                margin-bottom: 5px;
                padding: 2px 0;
            }}
            .log-timestamp {{
                color: #888;
            }}
            .log-info {{ color: #00ff00; }}
            .log-warning {{ color: #ffaa00; }}
            .log-error {{ color: #ff0000; }}
            .log-success {{ color: #00ff88; }}
        </style>
    </head>
    <body>
        {generate_navigation(lang)}

        <div class="container-fluid mt-4">
            <!-- 헤더 -->
            <div class="row mb-4">
                <div class="col-12">
                    <div class="mcp-card">
                        <h1 class="mb-2">
                            <i class="fas fa-robot"></i> {t('modelTesting.title', lang)}
                        </h1>
                        <p class="mb-0">{t('modelTesting.pipeline', lang)}</p>
                    </div>
                </div>
            </div>

            <!-- MCP 에이전트 상태 -->
            <div class="row mb-4">
                <div class="col-12">
                    <div class="agent-status">
                        <h5><i class="fas fa-brain"></i> {t('modelTesting.agentStatus', lang)}</h5>
                        <div class="row">
                            <div class="col-md-3">
                                <div class="text-center">
                                    <h6>{t('common.status', lang)}</h6>
                                    <span class="badge bg-success fs-6" id="agentStatus">{t('common.active', lang)}</span>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="text-center">
                                    <h6>{t('modelTesting.currentTask', lang)}</h6>
                                    <span id="currentTask">{t('modelTesting.dataCollection', lang)}</span>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="text-center">
                                    <h6>{t('modelTesting.progress', lang)}</h6>
                                    <div class="progress-step">
                                        <div class="progress-fill" id="overallProgress" style="width: 20%"></div>
                                    </div>
                                    <small id="progressText">20% {t('modelTesting.complete', lang)}</small>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="text-center">
                                    <button class="btn btn-primary" onclick="startMCPPipeline()">
                                        <i class="fas fa-play"></i> {t('modelTesting.startPipeline', lang)}
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- MCP 자동화 프로세스 -->
            <div class="row">
                <div class="col-lg-8">
                    <div class="mcp-card">
                        <h5><i class="fas fa-cogs"></i> MCP 자동화 프로세스</h5>
                        
                        <!-- 1단계: 데이터 자동 정제 -->
                        <div class="process-step" id="step1">
                            <div class="d-flex justify-content-between align-items-center">
                                <div>
                                    <h6><i class="fas fa-broom"></i> 1. 수집된 데이터 자동 정제</h6>
                                    <small>이상치 제거, 결측값 처리, 데이터 타입 변환</small>
                                </div>
                                <div class="text-end">
                                    <span class="badge bg-secondary" id="step1Status">Pending</span>
                                    <div class="progress-step mt-2" style="width: 100px;">
                                        <div class="progress-fill" id="step1Progress" style="width: 0%"></div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- 2단계: 메타데이터 라벨링 -->
                        <div class="process-step" id="step2">
                            <div class="d-flex justify-content-between align-items-center">
                                <div>
                                    <h6><i class="fas fa-tags"></i> 2. 메타데이터 시계열 데이터 라벨링</h6>
                                    <small>시계열 특성 분석, 패턴 인식, 라벨 자동 생성</small>
                                </div>
                                <div class="text-end">
                                    <span class="badge bg-secondary" id="step2Status">Pending</span>
                                    <div class="progress-step mt-2" style="width: 100px;">
                                        <div class="progress-fill" id="step2Progress" style="width: 0%"></div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- 3단계: 모델 선택과 학습 -->
                        <div class="process-step" id="step3">
                            <div class="d-flex justify-content-between align-items-center">
                                <div>
                                    <h6><i class="fas fa-brain"></i> 3. 학습 데이터 예측 모델 선택과 학습</h6>
                                    <small>AutoML 기반 모델 선택, 하이퍼파라미터 최적화, 자동 학습</small>
                                </div>
                                <div class="text-end">
                                    <span class="badge bg-secondary" id="step3Status">Pending</span>
                                    <div class="progress-step mt-2" style="width: 100px;">
                                        <div class="progress-fill" id="step3Progress" style="width: 0%"></div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- 4단계: 데이터 품질 검증 -->
                        <div class="process-step" id="step4">
                            <div class="d-flex justify-content-between align-items-center">
                                <div>
                                    <h6><i class="fas fa-shield-alt"></i> 4. 데이터 품질 검증 리포트</h6>
                                    <small>모델 성능 평가, 데이터 품질 메트릭, 검증 리포트 생성</small>
                                </div>
                                <div class="text-end">
                                    <span class="badge bg-secondary" id="step4Status">Pending</span>
                                    <div class="progress-step mt-2" style="width: 100px;">
                                        <div class="progress-fill" id="step4Progress" style="width: 0%"></div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- 5단계: 최종 모델 확정 -->
                        <div class="process-step" id="step5">
                            <div class="d-flex justify-content-between align-items-center">
                                <div>
                                    <h6><i class="fas fa-check-circle"></i> 5. 최종 모델 확정</h6>
                                    <small>모델 배포, 성능 모니터링, 자동 재학습 설정</small>
                                </div>
                                <div class="text-end">
                                    <span class="badge bg-secondary" id="step5Status">Pending</span>
                                    <div class="progress-step mt-2" style="width: 100px;">
                                        <div class="progress-fill" id="step5Progress" style="width: 0%"></div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 실시간 로그 및 메트릭 -->
                <div class="col-lg-4">
                    <div class="mcp-card">
                        <h5><i class="fas fa-terminal"></i> 실시간 로그</h5>
                        <div class="log-container" id="logContainer">
                            <div class="log-entry">
                                <span class="log-timestamp">[2024-01-15 10:30:15]</span>
                                <span class="log-info">MCP Agent initialized</span>
                            </div>
                            <div class="log-entry">
                                <span class="log-timestamp">[2024-01-15 10:30:16]</span>
                                <span class="log-info">Waiting for pipeline start...</span>
                            </div>
                        </div>
                    </div>

                    <div class="mcp-card">
                        <h5><i class="fas fa-chart-line"></i> 실시간 메트릭</h5>
                        <div class="metric-card">
                            <h6>Data Quality Score</h6>
                            <div class="progress mb-2">
                                <div class="progress-bar bg-success" id="dataQuality" style="width: 0%"></div>
                            </div>
                            <small id="dataQualityText">0%</small>
                        </div>
                        <div class="metric-card">
                            <h6>Model Accuracy</h6>
                            <div class="progress mb-2">
                                <div class="progress-bar bg-info" id="modelAccuracy" style="width: 0%"></div>
                            </div>
                            <small id="modelAccuracyText">0%</small>
                        </div>
                        <div class="metric-card">
                            <h6>Processing Speed</h6>
                            <div class="progress mb-2">
                                <div class="progress-bar bg-warning" id="processingSpeed" style="width: 0%"></div>
                            </div>
                            <small id="processingSpeedText">0 records/sec</small>
                        </div>
                    </div>
                </div>
            </div>

            <!-- AI/ML 서버 MCP 연결 -->
            <div class="row mt-4">
                <div class="col-12">
                    <div class="mcp-card">
                        <h5><i class="fas fa-server"></i> AI/ML 서버 MCP 연결</h5>
                        <div class="row">
                            <div class="col-md-6">
                                <div class="metric-card">
                                    <h6><i class="fas fa-link"></i> MCP 서버 연결 상태</h6>
                                    <div class="mb-3">
                                        <span class="badge bg-success" id="mcpConnectionStatus">Connected</span>
                                        <span class="ms-2" id="mcpServerInfo">ML Server v2.1.0</span>
                                    </div>
                                    <div class="mb-3">
                                        <button class="btn btn-primary btn-sm" onclick="connectMCPServer()">
                                            <i class="fas fa-plug"></i> Connect to MCP Server
                                        </button>
                                        <button class="btn btn-info btn-sm ms-2" onclick="refreshModelList()">
                                            <i class="fas fa-sync"></i> Refresh Models
                                        </button>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="metric-card">
                                    <h6><i class="fas fa-download"></i> 모델 다운로드</h6>
                                    <div class="mb-3">
                                        <select class="form-select" id="modelSelectDropdown">
                                            <option value="">모델을 선택하세요</option>
                                            <option value="xgboost-v1.2">XGBoost Regressor v1.2</option>
                                            <option value="lightgbm-v2.0">LightGBM v2.0</option>
                                            <option value="random-forest-v1.5">Random Forest v1.5</option>
                                            <option value="neural-network-v3.1">Neural Network v3.1</option>
                                        </select>
                                    </div>
                                    <div class="mb-3">
                                        <button class="btn btn-success btn-sm" onclick="downloadModel()" id="downloadBtn" disabled>
                                            <i class="fas fa-download"></i> Download Model
                                        </button>
                                        <button class="btn btn-warning btn-sm ms-2" onclick="optimizeModel()">
                                            <i class="fas fa-magic"></i> Optimize Model
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 모델 성능 대시보드 -->
            <div class="row mt-4">
                <div class="col-12">
                    <div class="mcp-card">
                        <h5><i class="fas fa-chart-bar"></i> 모델 성능 대시보드</h5>
                        <div class="row">
                            <div class="col-md-3">
                                <div class="metric-card text-center">
                                    <h6>Selected Model</h6>
                                    <h4 id="selectedModel">AutoML Selected</h4>
                                    <small class="text-muted">Best performing model</small>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="metric-card text-center">
                                    <h6>Training Time</h6>
                                    <h4 id="trainingTime">-</h4>
                                    <small class="text-muted">Total training duration</small>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="metric-card text-center">
                                    <h6>Validation Score</h6>
                                    <h4 id="validationScore">-</h4>
                                    <small class="text-muted">Cross-validation score</small>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="metric-card text-center">
                                    <h6>Deployment Status</h6>
                                    <h4 id="deploymentStatus">-</h4>
                                    <small class="text-muted">Model deployment status</small>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 모델 비교 및 선택 -->
            <div class="row mt-4">
                <div class="col-12">
                    <div class="mcp-card">
                        <h5><i class="fas fa-balance-scale"></i> 모델 비교 및 최적 선택</h5>
                        <div class="table-responsive">
                            <table class="table table-striped">
                                <thead>
                                    <tr>
                                        <th>Model Name</th>
                                        <th>Accuracy</th>
                                        <th>Precision</th>
                                        <th>Recall</th>
                                        <th>F1-Score</th>
                                        <th>Training Time</th>
                                        <th>Model Size</th>
                                        <th>Status</th>
                                        <th>Action</th>
                                    </tr>
                                </thead>
                                <tbody id="modelComparisonTable">
                                    <tr>
                                        <td><strong>XGBoost Regressor v1.2</strong></td>
                                        <td>0.92</td>
                                        <td>0.89</td>
                                        <td>0.91</td>
                                        <td>0.90</td>
                                        <td>2.3 min</td>
                                        <td>45 MB</td>
                                        <td><span class="badge bg-success">Available</span></td>
                                        <td>
                                            <button class="btn btn-primary btn-sm" onclick="selectModel('xgboost-v1.2')">
                                                <i class="fas fa-check"></i> Select
                                            </button>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td><strong>LightGBM v2.0</strong></td>
                                        <td>0.90</td>
                                        <td>0.87</td>
                                        <td>0.89</td>
                                        <td>0.88</td>
                                        <td>1.8 min</td>
                                        <td>32 MB</td>
                                        <td><span class="badge bg-success">Available</span></td>
                                        <td>
                                            <button class="btn btn-primary btn-sm" onclick="selectModel('lightgbm-v2.0')">
                                                <i class="fas fa-check"></i> Select
                                            </button>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td><strong>Random Forest v1.5</strong></td>
                                        <td>0.88</td>
                                        <td>0.85</td>
                                        <td>0.87</td>
                                        <td>0.86</td>
                                        <td>3.2 min</td>
                                        <td>78 MB</td>
                                        <td><span class="badge bg-warning">Training</span></td>
                                        <td>
                                            <button class="btn btn-secondary btn-sm" disabled>
                                                <i class="fas fa-clock"></i> Training
                                            </button>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td><strong>Neural Network v3.1</strong></td>
                                        <td>0.94</td>
                                        <td>0.92</td>
                                        <td>0.93</td>
                                        <td>0.925</td>
                                        <td>5.1 min</td>
                                        <td>156 MB</td>
                                        <td><span class="badge bg-success">Available</span></td>
                                        <td>
                                            <button class="btn btn-primary btn-sm" onclick="selectModel('neural-network-v3.1')">
                                                <i class="fas fa-check"></i> Select
                                            </button>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
        <script>
            let currentStep = 0;
            let pipelineRunning = false;
            let logEntries = 0;

            // 로그 추가 함수
            function addLog(message, type = 'info') {{
                const logContainer = document.getElementById('logContainer');
                const timestamp = new Date().toLocaleTimeString();
                const logEntry = document.createElement('div');
                logEntry.className = 'log-entry';
                logEntry.innerHTML = `
                    <span class="log-timestamp">[${{timestamp}}]</span>
                    <span class="log-${{type}}">${{message}}</span>
                `;
                logContainer.appendChild(logEntry);
                logContainer.scrollTop = logContainer.scrollHeight;
                logEntries++;
                
                // 로그가 너무 많아지면 오래된 것 제거
                if (logEntries > 50) {{
                    logContainer.removeChild(logContainer.firstChild);
                    logEntries--;
                }}
            }}

            // 단계 업데이트 함수
            function updateStep(stepNumber, status, progress) {{
                const stepElement = document.getElementById(`step${{stepNumber}}`);
                const statusElement = document.getElementById(`step${{stepNumber}}Status`);
                const progressElement = document.getElementById(`step${{stepNumber}}Progress`);
                
                // 이전 단계 완료 처리
                if (stepNumber > 1) {{
                    const prevStep = document.getElementById(`step${{stepNumber - 1}}`);
                    prevStep.classList.remove('active');
                    prevStep.classList.add('completed');
                    document.getElementById(`step${{stepNumber - 1}}Status`).textContent = 'Completed';
                    document.getElementById(`step${{stepNumber - 1}}Status`).className = 'badge bg-success';
                }}
                
                // 현재 단계 활성화
                stepElement.classList.add('active');
                statusElement.textContent = status;
                statusElement.className = `badge bg-${{status === 'Running' ? 'warning' : status === 'Completed' ? 'success' : 'secondary'}}`;
                progressElement.style.width = progress + '%';
            }}

            // 메트릭 업데이트 함수
            function updateMetrics(dataQuality, modelAccuracy, processingSpeed) {{
                document.getElementById('dataQuality').style.width = dataQuality + '%';
                document.getElementById('dataQualityText').textContent = dataQuality + '%';
                document.getElementById('modelAccuracy').style.width = modelAccuracy + '%';
                document.getElementById('modelAccuracyText').textContent = modelAccuracy + '%';
                document.getElementById('processingSpeed').style.width = Math.min(processingSpeed / 10, 100) + '%';
                document.getElementById('processingSpeedText').textContent = processingSpeed + ' records/sec';
            }}

            // MCP 파이프라인 시작
            function startMCPPipeline() {{
                if (pipelineRunning) return;
                
                pipelineRunning = true;
                document.getElementById('agentStatus').textContent = 'Running';
                document.getElementById('agentStatus').className = 'badge bg-warning fs-6';
                document.getElementById('currentTask').textContent = 'Data Processing';
                
                addLog('Starting MCP automated pipeline...', 'info');
                
                // 1단계: 데이터 자동 정제
                setTimeout(() => {{
                    updateStep(1, 'Running', 0);
                    addLog('Step 1: Starting data cleaning and preprocessing...', 'info');
                    
                    let progress = 0;
                    const interval1 = setInterval(() => {{
                        progress += Math.random() * 15;
                        if (progress >= 100) {{
                            progress = 100;
                            clearInterval(interval1);
                            updateStep(1, 'Completed', 100);
                            addLog('Step 1: Data cleaning completed successfully', 'success');
                            updateMetrics(95, 0, 0);
                            startStep2();
                        }} else {{
                            document.getElementById('step1Progress').style.width = progress + '%';
                            updateMetrics(Math.floor(progress * 0.95), 0, Math.floor(progress * 2));
                        }}
                    }}, 200);
                }}, 1000);
            }}

            // 2단계: 메타데이터 라벨링
            function startStep2() {{
                setTimeout(() => {{
                    updateStep(2, 'Running', 0);
                    addLog('Step 2: Starting metadata labeling and time series analysis...', 'info');
                    
                    let progress = 0;
                    const interval2 = setInterval(() => {{
                        progress += Math.random() * 12;
                        if (progress >= 100) {{
                            progress = 100;
                            clearInterval(interval2);
                            updateStep(2, 'Completed', 100);
                            addLog('Step 2: Metadata labeling completed', 'success');
                            updateMetrics(98, 0, 0);
                            startStep3();
                        }} else {{
                            document.getElementById('step2Progress').style.width = progress + '%';
                            updateMetrics(95 + Math.floor(progress * 0.03), 0, 2 + Math.floor(progress * 1.5));
                        }}
                    }}, 300);
                }}, 500);
            }}

            // 3단계: 모델 선택과 학습
            function startStep3() {{
                setTimeout(() => {{
                    updateStep(3, 'Running', 0);
                    addLog('Step 3: Starting AutoML model selection and training...', 'info');
                    
                    let progress = 0;
                    const interval3 = setInterval(() => {{
                        progress += Math.random() * 8;
                        if (progress >= 100) {{
                            progress = 100;
                            clearInterval(interval3);
                            updateStep(3, 'Completed', 100);
                            addLog('Step 3: Model training completed', 'success');
                            updateMetrics(98, 87, 0);
                            document.getElementById('selectedModel').textContent = 'XGBoost Regressor';
                            document.getElementById('trainingTime').textContent = '2.3 min';
                            document.getElementById('validationScore').textContent = '0.87';
                            startStep4();
                        }} else {{
                            document.getElementById('step3Progress').style.width = progress + '%';
                            updateMetrics(98, Math.floor(progress * 0.87), 0);
                        }}
                    }}, 400);
                }}, 500);
            }}

            // 4단계: 데이터 품질 검증
            function startStep4() {{
                setTimeout(() => {{
                    updateStep(4, 'Running', 0);
                    addLog('Step 4: Starting data quality validation and reporting...', 'info');
                    
                    let progress = 0;
                    const interval4 = setInterval(() => {{
                        progress += Math.random() * 20;
                        if (progress >= 100) {{
                            progress = 100;
                            clearInterval(interval4);
                            updateStep(4, 'Completed', 100);
                            addLog('Step 4: Quality validation completed', 'success');
                            updateMetrics(99, 89, 0);
                            startStep5();
                        }} else {{
                            document.getElementById('step4Progress').style.width = progress + '%';
                            updateMetrics(98 + Math.floor(progress * 0.01), 87 + Math.floor(progress * 0.02), 0);
                        }}
                    }}, 150);
                }}, 500);
            }}

            // 5단계: 최종 모델 확정
            function startStep5() {{
                setTimeout(() => {{
                    updateStep(5, 'Running', 0);
                    addLog('Step 5: Finalizing model and setting up deployment...', 'info');
                    
                    let progress = 0;
                    const interval5 = setInterval(() => {{
                        progress += Math.random() * 25;
                        if (progress >= 100) {{
                            progress = 100;
                            clearInterval(interval5);
                            updateStep(5, 'Completed', 100);
                            addLog('Step 5: Model deployment completed successfully!', 'success');
                            updateMetrics(100, 92, 0);
                            document.getElementById('deploymentStatus').textContent = 'Deployed';
                            document.getElementById('deploymentStatus').className = 'text-success';
                            
                            // 파이프라인 완료
                            document.getElementById('agentStatus').textContent = 'Completed';
                            document.getElementById('agentStatus').className = 'badge bg-success fs-6';
                            document.getElementById('currentTask').textContent = 'Pipeline Complete';
                            document.getElementById('overallProgress').style.width = '100%';
                            document.getElementById('progressText').textContent = '100% Complete';
                            
                            pipelineRunning = false;
                            addLog('MCP automated pipeline completed successfully!', 'success');
                        }} else {{
                            document.getElementById('step5Progress').style.width = progress + '%';
                            updateMetrics(99 + Math.floor(progress * 0.01), 89 + Math.floor(progress * 0.03), 0);
                        }}
                    }}, 100);
                }}, 500);
            }}

            // MCP 서버 연결 함수
            function connectMCPServer() {{
                addLog('Connecting to MCP ML Server...', 'info');
                document.getElementById('mcpConnectionStatus').textContent = 'Connecting';
                document.getElementById('mcpConnectionStatus').className = 'badge bg-warning';
                
                setTimeout(() => {{
                    document.getElementById('mcpConnectionStatus').textContent = 'Connected';
                    document.getElementById('mcpConnectionStatus').className = 'badge bg-success';
                    document.getElementById('mcpServerInfo').textContent = 'ML Server v2.1.0 - Connected';
                    addLog('Successfully connected to MCP ML Server', 'success');
                    refreshModelList();
                }}, 2000);
            }}

            // 모델 목록 새로고침
            function refreshModelList() {{
                addLog('Refreshing model list from MCP server...', 'info');
                
                // 모델 목록 업데이트 시뮬레이션
                setTimeout(() => {{
                    addLog('Model list refreshed: 4 models available', 'success');
                    updateModelComparisonTable();
                }}, 1500);
            }}

            // 모델 선택 함수
            function selectModel(modelId) {{
                const modelNames = {{
                    'xgboost-v1.2': 'XGBoost Regressor v1.2',
                    'lightgbm-v2.0': 'LightGBM v2.0',
                    'random-forest-v1.5': 'Random Forest v1.5',
                    'neural-network-v3.1': 'Neural Network v3.1'
                }};
                
                const modelName = modelNames[modelId];
                addLog(`Selected model: ${{modelName}}`, 'info');
                
                // 선택된 모델 정보 업데이트
                document.getElementById('selectedModel').textContent = modelName;
                document.getElementById('modelSelectDropdown').value = modelId;
                document.getElementById('downloadBtn').disabled = false;
                
                // 테이블에서 선택된 모델 하이라이트
                const rows = document.querySelectorAll('#modelComparisonTable tr');
                rows.forEach(row => {{
                    row.classList.remove('table-primary');
                    if (row.innerHTML.includes(modelName)) {{
                        row.classList.add('table-primary');
                    }}
                }});
                
                // 모델 성능 메트릭 업데이트
                updateModelMetrics(modelId);
            }}

            // 모델 다운로드 함수
            function downloadModel() {{
                const selectedModel = document.getElementById('modelSelectDropdown').value;
                if (!selectedModel) {{
                    addLog('Please select a model first', 'warning');
                    return;
                }}
                
                addLog(`Starting download for model: ${{selectedModel}}`, 'info');
                
                // 다운로드 진행률 시뮬레이션
                let progress = 0;
                const downloadInterval = setInterval(() => {{
                    progress += Math.random() * 20;
                    if (progress >= 100) {{
                        progress = 100;
                        clearInterval(downloadInterval);
                        addLog(`Model ${{selectedModel}} downloaded successfully!`, 'success');
                        document.getElementById('deploymentStatus').textContent = 'Downloaded';
                        document.getElementById('deploymentStatus').className = 'text-success';
                    }} else {{
                        addLog(`Downloading... ${{Math.floor(progress)}}%`, 'info');
                    }}
                }}, 500);
            }}

            // 모델 최적화 함수
            function optimizeModel() {{
                const selectedModel = document.getElementById('modelSelectDropdown').value;
                if (!selectedModel) {{
                    addLog('Please select a model first', 'warning');
                    return;
                }}
                
                addLog(`Starting optimization for model: ${{selectedModel}}`, 'info');
                
                // 최적화 진행률 시뮬레이션
                let progress = 0;
                const optimizeInterval = setInterval(() => {{
                    progress += Math.random() * 15;
                    if (progress >= 100) {{
                        progress = 100;
                        clearInterval(optimizeInterval);
                        addLog(`Model ${{selectedModel}} optimized successfully!`, 'success');
                        
                        // 최적화된 성능 메트릭 업데이트
                        updateModelMetrics(selectedModel, true);
                    }} else {{
                        addLog(`Optimizing... ${{Math.floor(progress)}}%`, 'info');
                    }}
                }}, 800);
            }}

            // 모델 성능 메트릭 업데이트
            function updateModelMetrics(modelId, optimized = false) {{
                const metrics = {{
                    'xgboost-v1.2': {{ accuracy: 0.92, precision: 0.89, recall: 0.91, f1: 0.90, time: '2.3 min' }},
                    'lightgbm-v2.0': {{ accuracy: 0.90, precision: 0.87, recall: 0.89, f1: 0.88, time: '1.8 min' }},
                    'random-forest-v1.5': {{ accuracy: 0.88, precision: 0.85, recall: 0.87, f1: 0.86, time: '3.2 min' }},
                    'neural-network-v3.1': {{ accuracy: 0.94, precision: 0.92, recall: 0.93, f1: 0.925, time: '5.1 min' }}
                }};
                
                const modelMetrics = metrics[modelId];
                if (modelMetrics) {{
                    if (optimized) {{
                        // 최적화된 성능 (5-10% 향상)
                        modelMetrics.accuracy += 0.05;
                        modelMetrics.precision += 0.05;
                        modelMetrics.recall += 0.05;
                        modelMetrics.f1 += 0.05;
                    }}
                    
                    document.getElementById('trainingTime').textContent = modelMetrics.time;
                    document.getElementById('validationScore').textContent = modelMetrics.accuracy.toFixed(3);
                    
                    // 실시간 메트릭 업데이트
                    updateMetrics(100, Math.floor(modelMetrics.accuracy * 100), 0);
                }}
            }}

            // 모델 비교 테이블 업데이트
            function updateModelComparisonTable() {{
                // 테이블 데이터를 동적으로 업데이트하는 로직
                addLog('Model comparison table updated with latest metrics', 'info');
            }}

            // 모델 선택 드롭다운 이벤트 리스너
            document.addEventListener('DOMContentLoaded', function() {{
                const modelSelect = document.getElementById('modelSelectDropdown');
                modelSelect.addEventListener('change', function() {{
                    if (this.value) {{
                        selectModel(this.value);
                    }} else {{
                        document.getElementById('downloadBtn').disabled = true;
                    }}
                }});
            }});

            // 초기화
            document.addEventListener('DOMContentLoaded', function() {{
                addLog('MCP Agent ready for automated ML pipeline', 'info');
                addLog('AI/ML Server MCP connection established', 'success');
                updateMetrics(0, 0, 0);
                
                // 자동으로 MCP 서버 연결
                setTimeout(() => {{
                    connectMCPServer();
                }}, 1000);
            }});
        </script>
    </body>
    </html>
    """

@web_app.get("/crewai-system", response_class=HTMLResponse)
async def crewai_system_page(request: Request, lang: str = Query("ko", description="Language code")):
    """CrewAI Specialized Agent Teams 페이지"""
    # 언어 설정
    if lang not in get_available_languages():
        lang = "ko"
    
    return f"""
    <!DOCTYPE html>
    <html lang="{lang}">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🤖 CrewAI Specialized Agent Teams</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <script src="https://cdn.jsdelivr.net/npm/chart.js?v=2.0"></script>
        <style>
            body {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }}
            .crew-card {{
                background: rgba(255, 255, 255, 0.95);
                border-radius: 15px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.2);
                margin-bottom: 20px;
                padding: 25px;
                transition: transform 0.3s ease;
            }}
            .crew-card:hover {{
                transform: translateY(-5px);
            }}
            .crew-header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border-radius: 10px;
                padding: 15px;
                margin-bottom: 20px;
            }}
            .status-indicator {{
                width: 12px;
                height: 12px;
                border-radius: 50%;
                display: inline-block;
                margin-right: 8px;
            }}
            .status-active {{ background-color: #28a745; }}
            .status-idle {{ background-color: #ffc107; }}
            .status-error {{ background-color: #dc3545; }}
            .workflow-step {{
                background: rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                padding: 15px;
                margin: 10px 0;
                border-left: 4px solid #667eea;
            }}
            .agent-avatar {{
                width: 60px;
                height: 60px;
                border-radius: 50%;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-size: 24px;
                margin: 0 auto 15px;
            }}
        </style>
    </head>
    <body>
        {generate_navigation(lang)}

        <div class="container-fluid mt-4">
            <!-- 헤더 -->
            <div class="row mb-4">
                <div class="col-12">
                    <div class="crew-card">
                        <h1 class="mb-3">
                            <i class="fas fa-users-cog text-primary"></i> CrewAI Specialized Agent Teams
                        </h1>
                        <h4 class="text-muted mb-3">전문화된 에이전트 팀을 통한 자동화된 에너지 관리</h4>
                        <p class="lead">MCP 서버 기능을 전문화된 에이전트 팀으로 분해하여 이벤트 기반 자동화 시스템 구축</p>
                    </div>
                </div>
            </div>

            <!-- Crew Status Overview -->
            <div class="row mb-4">
                <div class="col-12">
                    <div class="crew-card">
                        <h5><i class="fas fa-chart-pie"></i> Crew Status Overview</h5>
                        <div class="row">
                            <div class="col-md-2">
                                <div class="text-center">
                                    <div class="agent-avatar">
                                        <i class="fas fa-database"></i>
                                    </div>
                                    <h6>Data Ingestion</h6>
                                    <span class="status-indicator status-active"></span>
                                    <small>Active</small>
                                </div>
                            </div>
                            <div class="col-md-2">
                                <div class="text-center">
                                    <div class="agent-avatar">
                                        <i class="fas fa-chart-line"></i>
                                    </div>
                                    <h6>Forecasting</h6>
                                    <span class="status-indicator status-active"></span>
                                    <small>Active</small>
                                </div>
                            </div>
                            <div class="col-md-2">
                                <div class="text-center">
                                    <div class="agent-avatar">
                                        <i class="fas fa-exclamation-triangle"></i>
                                    </div>
                                    <h6>Anomaly Detection</h6>
                                    <span class="status-indicator status-active"></span>
                                    <small>Active</small>
                                </div>
                            </div>
                            <div class="col-md-2">
                                <div class="text-center">
                                    <div class="agent-avatar">
                                        <i class="fas fa-sliders-h"></i>
                                    </div>
                                    <h6>Demand Control</h6>
                                    <span class="status-indicator status-active"></span>
                                    <small>Active</small>
                                </div>
                            </div>
                            <div class="col-md-2">
                                <div class="text-center">
                                    <div class="agent-avatar">
                                        <i class="fas fa-file-alt"></i>
                                    </div>
                                    <h6>Reporting</h6>
                                    <span class="status-indicator status-active"></span>
                                    <small>Active</small>
                                </div>
                            </div>
                            <div class="col-md-2">
                                <div class="text-center">
                                    <div class="agent-avatar">
                                        <i class="fas fa-cogs"></i>
                                    </div>
                                    <h6>Orchestrator</h6>
                                    <span class="status-indicator status-active"></span>
                                    <small>Active</small>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Workflow Control -->
            <div class="row mb-4">
                <div class="col-md-6">
                    <div class="crew-card">
                        <h5><i class="fas fa-play-circle"></i> Workflow Control</h5>
                        <div class="mb-3">
                            <label class="form-label">Workflow Type</label>
                            <select class="form-select" id="workflowType">
                                <option value="sequential">Sequential Workflow</option>
                                <option value="parallel">Parallel Workflow</option>
                                <option value="hybrid">Hybrid Workflow</option>
                            </select>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Trigger Event</label>
                            <input type="text" class="form-control" id="triggerEvent" placeholder="Optional trigger event">
                        </div>
                        <button class="btn btn-primary w-100 mb-2" onclick="startWorkflow()">
                            <i class="fas fa-play"></i> Start Workflow
                        </button>
                        <button class="btn btn-warning w-100 mb-2" onclick="pauseWorkflow()">
                            <i class="fas fa-pause"></i> Pause Workflow
                        </button>
                        <button class="btn btn-danger w-100" onclick="stopWorkflow()">
                            <i class="fas fa-stop"></i> Stop Workflow
                        </button>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="crew-card">
                        <h5><i class="fas fa-chart-bar"></i> System Metrics</h5>
                        <div class="row">
                            <div class="col-6">
                                <div class="text-center">
                                    <h6>Active Crews</h6>
                                    <h3 class="text-success" id="activeCrews">5</h3>
                                </div>
                            </div>
                            <div class="col-6">
                                <div class="text-center">
                                    <h6>Events Processed</h6>
                                    <h3 class="text-info" id="eventsProcessed">1,247</h3>
                                </div>
                            </div>
                        </div>
                        <div class="row mt-3">
                            <div class="col-6">
                                <div class="text-center">
                                    <h6>Success Rate</h6>
                                    <h3 class="text-success" id="successRate">98.5%</h3>
                                </div>
                            </div>
                            <div class="col-6">
                                <div class="text-center">
                                    <h6>Avg Response Time</h6>
                                    <h3 class="text-warning" id="avgResponseTime">2.3s</h3>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Crew Details -->
            <div class="row mb-4">
                <div class="col-md-6">
                    <div class="crew-card">
                        <div class="crew-header">
                            <h5><i class="fas fa-database"></i> Data Ingestion Crew</h5>
                        </div>
                        <p><strong>Role:</strong> 센서/기상/발전/배터리/요금 데이터 수집·정제·스키마 검증</p>
                        <p><strong>Tools:</strong> MCP 외부데이터/날씨 도구, HTTP/API 래퍼, Health/API 상태 체크</p>
                        <div class="workflow-step">
                            <strong>Current Task:</strong> Real-time sensor data collection
                        </div>
                        <div class="workflow-step">
                            <strong>Status:</strong> <span class="status-indicator status-active"></span> Collecting data from 15 sources
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="crew-card">
                        <div class="crew-header">
                            <h5><i class="fas fa-chart-line"></i> Forecasting & Climate Crew</h5>
                        </div>
                        <p><strong>Role:</strong> 단기/중기 수요·발전 시계열 예측, 기후 Nowcasting 연계</p>
                        <p><strong>Tools:</strong> 모델 비교/AutoML 파이프라인, XGBoost/LGBM/RF/NN 모델</p>
                        <div class="workflow-step">
                            <strong>Current Task:</strong> 24-hour energy demand prediction
                        </div>
                        <div class="workflow-step">
                            <strong>Status:</strong> <span class="status-indicator status-active"></span> Model accuracy: 94.2%
                        </div>
                    </div>
                </div>
            </div>

            <div class="row mb-4">
                <div class="col-md-6">
                    <div class="crew-card">
                        <div class="crew-header">
                            <h5><i class="fas fa-exclamation-triangle"></i> Anomaly & Quality Crew</h5>
                        </div>
                        <p><strong>Role:</strong> 데이터 품질/예측 오차/장비 이상 탐지, 경보 임계치 동적 조정</p>
                        <p><strong>Tools:</strong> 이상치 탐지·품질 리포트 루틴, 5분 주기 모니터링</p>
                        <div class="workflow-step">
                            <strong>Current Task:</strong> Real-time anomaly detection
                        </div>
                        <div class="workflow-step">
                            <strong>Status:</strong> <span class="status-indicator status-active"></span> 3 anomalies detected
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="crew-card">
                        <div class="crew-header">
                            <h5><i class="fas fa-sliders-h"></i> Demand Response & Control Crew</h5>
                        </div>
                        <p><strong>Role:</strong> 수요-공급 매칭율/피크 억제/부하전환 시뮬레이션, 제어 권고·명령 생성</p>
                        <p><strong>Tools:</strong> 수요 제어/시뮬레이션/매칭율 대시보드, 운영 정책 옵션화</p>
                        <div class="workflow-step">
                            <strong>Current Task:</strong> Demand-supply matching optimization
                        </div>
                        <div class="workflow-step">
                            <strong>Status:</strong> <span class="status-indicator status-active"></span> Matching rate: 96.8%
                        </div>
                    </div>
                </div>
            </div>

            <div class="row mb-4">
                <div class="col-12">
                    <div class="crew-card">
                        <div class="crew-header">
                            <h5><i class="fas fa-file-alt"></i> LLM-SLM Ops & Reporting Crew</h5>
                        </div>
                        <p><strong>Role:</strong> 운영 리포트 생성, 요약/설명, 자연어 질의 응답, LLM-SLM 개발보드 연동</p>
                        <p><strong>Tools:</strong> 모델 거버넌스(배포/롤백) 자동화, 학습률/진행률/버전 관리</p>
                        <div class="row">
                            <div class="col-md-4">
                                <div class="workflow-step">
                                    <strong>Current Task:</strong> Daily operational report generation
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="workflow-step">
                                    <strong>Model Status:</strong> EnergySLM-v2.1 (Training: 65%)
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="workflow-step">
                                    <strong>Status:</strong> <span class="status-indicator status-active"></span> Report generation in progress
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Event Log -->
            <div class="row mb-4">
                <div class="col-12">
                    <div class="crew-card">
                        <h5><i class="fas fa-list"></i> Event Log</h5>
                        <div class="bg-dark text-light p-3 rounded" style="height: 300px; overflow-y: auto; font-family: monospace;" id="eventLog">
                            <div>[2024-01-15 10:30:15] Data Ingestion Crew: Started sensor data collection</div>
                            <div>[2024-01-15 10:30:18] Forecasting Crew: Generated 24h demand prediction</div>
                            <div>[2024-01-15 10:30:22] Anomaly Crew: Detected 3 anomalies in generation data</div>
                            <div>[2024-01-15 10:30:25] Control Crew: Optimized demand-supply matching</div>
                            <div>[2024-01-15 10:30:28] Reporting Crew: Generated operational summary</div>
                            <div class="text-warning">[2024-01-15 10:30:30] System: All crews operating normally</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
        <script>
            // Workflow control functions
            function startWorkflow() {{
                const workflowType = document.getElementById('workflowType').value;
                const triggerEvent = document.getElementById('triggerEvent').value;
                
                addEventLog(`Starting ${{workflowType}} workflow...`);
                
                // Simulate workflow execution
                setTimeout(() => {{
                    addEventLog(`${{workflowType}} workflow completed successfully`);
                    updateMetrics();
                }}, 3000);
            }}

            function pauseWorkflow() {{
                addEventLog('Workflow paused by user');
            }}

            function stopWorkflow() {{
                addEventLog('Workflow stopped by user');
            }}

            // Event logging
            function addEventLog(message, type = 'info') {{
                const logContainer = document.getElementById('eventLog');
                const timestamp = new Date().toLocaleString();
                const logEntry = document.createElement('div');
                logEntry.className = type === 'error' ? 'text-danger' : type === 'warning' ? 'text-warning' : '';
                logEntry.innerHTML = `[${{timestamp}}] ${{message}}`;
                logContainer.appendChild(logEntry);
                logContainer.scrollTop = logContainer.scrollHeight;
            }}

            // Metrics update
            function updateMetrics() {{
                const activeCrews = document.getElementById('activeCrews');
                const eventsProcessed = document.getElementById('eventsProcessed');
                const successRate = document.getElementById('successRate');
                const avgResponseTime = document.getElementById('avgResponseTime');

                // Simulate metric updates
                const currentEvents = parseInt(eventsProcessed.textContent.replace(',', ''));
                eventsProcessed.textContent = (currentEvents + Math.floor(Math.random() * 10)).toLocaleString();
                
                const currentRate = parseFloat(successRate.textContent);
                successRate.textContent = (currentRate + Math.random() * 0.1).toFixed(1) + '%';
                
                const currentTime = parseFloat(avgResponseTime.textContent);
                avgResponseTime.textContent = (currentTime + Math.random() * 0.2).toFixed(1) + 's';
            }}

            // Auto-update metrics every 30 seconds
            setInterval(updateMetrics, 30000);

            // Auto-add events every 60 seconds
            setInterval(() => {{
                const events = [
                    'Data Ingestion Crew: Collected 1,000 new data points',
                    'Forecasting Crew: Updated prediction models',
                    'Anomaly Crew: No new anomalies detected',
                    'Control Crew: Optimized energy distribution',
                    'Reporting Crew: Generated hourly summary'
                ];
                const randomEvent = events[Math.floor(Math.random() * events.length)];
                addEventLog(randomEvent);
            }}, 60000);
        </script>
    </body>
    </html>
    """

@web_app.get("/llm-slm", response_class=HTMLResponse)
async def llm_slm_page(request: Request, lang: str = Query("ko", description="Language code")):
    """LLM SLM Development 페이지"""
    # 언어 설정
    if lang not in get_available_languages():
        lang = "ko"
    
    return f"""
    <!DOCTYPE html>
    <html lang="{lang}">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🤖 LLM SLM Development - Energy Specialized Language Model</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <script src="https://cdn.jsdelivr.net/npm/chart.js?v=2.0"></script>
        <style>
            body {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }}
            .llm-card {{
                background: rgba(255, 255, 255, 0.95);
                border-radius: 15px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.2);
                margin-bottom: 20px;
                padding: 25px;
            }}
            .model-card {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border-radius: 15px;
                padding: 20px;
                margin-bottom: 20px;
                transition: transform 0.3s ease;
            }}
            .model-card:hover {{
                transform: translateY(-5px);
            }}
            .training-progress {{
                background: rgba(255, 255, 255, 0.2);
                border-radius: 10px;
                padding: 15px;
                margin: 10px 0;
            }}
            .metric-card {{
                background: rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                padding: 15px;
                text-align: center;
                margin: 10px 0;
            }}
            .status-indicator {{
                width: 12px;
                height: 12px;
                border-radius: 50%;
                display: inline-block;
                margin-right: 8px;
            }}
            .status-training {{ background-color: #ffc107; }}
            .status-completed {{ background-color: #28a745; }}
            .status-error {{ background-color: #dc3545; }}
        </style>
    </head>
    <body>
        {generate_navigation(lang)}

        <div class="container-fluid mt-4">
            <!-- 헤더 -->
            <div class="row mb-4">
                <div class="col-12">
                    <div class="llm-card">
                        <h1 class="mb-3">
                            <i class="fas fa-robot text-primary"></i> LLM SLM Development
                        </h1>
                        <h4 class="text-muted mb-3">에너지 특화 언어 모델 개발</h4>
                        <p class="lead">Advanced AI language model specialized for energy management and analysis</p>
                    </div>
                </div>
            </div>

            <!-- 모델 개발 상태 -->
            <div class="row mb-4">
                <div class="col-md-6">
                    <div class="model-card">
                        <h5><i class="fas fa-brain"></i> 현재 개발 모델</h5>
                        <div class="row">
                            <div class="col-6">
                                <div class="metric-card">
                                    <h6>모델 이름</h6>
                                    <strong>EnergySLM-v2.1</strong>
                                </div>
                            </div>
                            <div class="col-6">
                                <div class="metric-card">
                                    <h6>개발 상태</h6>
                                    <span class="status-indicator status-training"></span>
                                    <strong>훈련 중</strong>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="model-card">
                        <h5><i class="fas fa-chart-line"></i> 훈련 진행률</h5>
                        <div class="training-progress">
                            <div class="d-flex justify-content-between mb-2">
                                <span>전체 진행률</span>
                                <span id="trainingProgress">65%</span>
                            </div>
                            <div class="progress">
                                <div class="progress-bar bg-warning" role="progressbar" style="width: 65%" id="progressBar"></div>
                            </div>
                            <small class="text-light">Epoch 325/500</small>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 모델 성능 지표 -->
            <div class="row mb-4">
                <div class="col-md-3">
                    <div class="llm-card text-center">
                        <h6><i class="fas fa-bullseye"></i> 정확도</h6>
                        <h3 class="text-success" id="accuracy">94.2%</h3>
                        <small class="text-muted">Energy Prediction</small>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="llm-card text-center">
                        <h6><i class="fas fa-tachometer-alt"></i> 처리 속도</h6>
                        <h3 class="text-info" id="speed">1.2s</h3>
                        <small class="text-muted">평균 응답 시간</small>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="llm-card text-center">
                        <h6><i class="fas fa-database"></i> 데이터셋</h6>
                        <h3 class="text-warning" id="dataset">2.3M</h3>
                        <small class="text-muted">훈련 샘플</small>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="llm-card text-center">
                        <h6><i class="fas fa-memory"></i> 모델 크기</h6>
                        <h3 class="text-primary" id="modelSize">1.8GB</h3>
                        <small class="text-muted">파라미터 수</small>
                    </div>
                </div>
            </div>

            <!-- 훈련 로그 -->
            <div class="row mb-4">
                <div class="col-md-8">
                    <div class="llm-card">
                        <h5><i class="fas fa-terminal"></i> 실시간 훈련 로그</h5>
                        <div class="bg-dark text-light p-3 rounded" style="height: 300px; overflow-y: auto; font-family: monospace;" id="trainingLog">
                            <div>[2024-01-15 10:30:15] 모델 초기화 완료</div>
                            <div>[2024-01-15 10:30:16] 데이터셋 로딩 중...</div>
                            <div>[2024-01-15 10:30:18] 훈련 시작 - Epoch 1/500</div>
                            <div>[2024-01-15 10:35:22] Loss: 2.3456, Accuracy: 0.7234</div>
                            <div>[2024-01-15 10:40:15] Epoch 2 완료 - Loss: 2.1234</div>
                            <div>[2024-01-15 10:45:08] 검증 정확도: 0.7891</div>
                            <div class="text-warning">[2024-01-15 10:50:12] 현재 Epoch 325/500 진행 중...</div>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="llm-card">
                        <h5><i class="fas fa-cogs"></i> 모델 설정</h5>
                        <div class="mb-3">
                            <label class="form-label">학습률 (Learning Rate)</label>
                            <input type="range" class="form-range" min="0.001" max="0.1" step="0.001" value="0.01" id="learningRate">
                            <small class="text-muted">현재: 0.01</small>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">배치 크기 (Batch Size)</label>
                            <select class="form-select" id="batchSize">
                                <option value="16">16</option>
                                <option value="32" selected>32</option>
                                <option value="64">64</option>
                                <option value="128">128</option>
                            </select>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">에포크 수 (Epochs)</label>
                            <input type="number" class="form-control" value="500" id="epochs">
                        </div>
                        <button class="btn btn-primary w-100 mb-2" onclick="startTraining()">
                            <i class="fas fa-play"></i> 훈련 시작
                        </button>
                        <button class="btn btn-warning w-100 mb-2" onclick="pauseTraining()">
                            <i class="fas fa-pause"></i> 훈련 일시정지
                        </button>
                        <button class="btn btn-danger w-100" onclick="stopTraining()">
                            <i class="fas fa-stop"></i> 훈련 중지
                        </button>
                    </div>
                </div>
            </div>

            <!-- 모델 비교 -->
            <div class="row mb-4">
                <div class="col-12">
                    <div class="llm-card">
                        <h5><i class="fas fa-balance-scale"></i> 모델 버전 비교</h5>
                        <div class="table-responsive">
                            <table class="table table-striped">
                                <thead>
                                    <tr>
                                        <th>모델 버전</th>
                                        <th>정확도</th>
                                        <th>처리 속도</th>
                                        <th>모델 크기</th>
                                        <th>개발 상태</th>
                                        <th>작업</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td><strong>EnergySLM-v2.1</strong></td>
                                        <td>94.2%</td>
                                        <td>1.2s</td>
                                        <td>1.8GB</td>
                                        <td><span class="status-indicator status-training"></span>훈련 중</td>
                                        <td>
                                            <button class="btn btn-sm btn-outline-primary">상세보기</button>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td><strong>EnergySLM-v2.0</strong></td>
                                        <td>91.8%</td>
                                        <td>1.5s</td>
                                        <td>1.6GB</td>
                                        <td><span class="status-indicator status-completed"></span>완료</td>
                                        <td>
                                            <button class="btn btn-sm btn-success">배포</button>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td><strong>EnergySLM-v1.9</strong></td>
                                        <td>89.3%</td>
                                        <td>1.8s</td>
                                        <td>1.4GB</td>
                                        <td><span class="status-indicator status-completed"></span>완료</td>
                                        <td>
                                            <button class="btn btn-sm btn-outline-secondary">아카이브</button>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
        <script>
            // 실시간 훈련 로그 업데이트
            function addTrainingLog(message, type = 'info') {{
                const logContainer = document.getElementById('trainingLog');
                const timestamp = new Date().toLocaleString();
                const logEntry = document.createElement('div');
                logEntry.className = type === 'error' ? 'text-danger' : type === 'warning' ? 'text-warning' : '';
                logEntry.innerHTML = `[${{timestamp}}] ${{message}}`;
                logContainer.appendChild(logEntry);
                logContainer.scrollTop = logContainer.scrollHeight;
            }}

            // 훈련 진행률 업데이트
            function updateTrainingProgress() {{
                const progress = Math.min(65 + Math.random() * 2, 100);
                document.getElementById('trainingProgress').textContent = Math.round(progress) + '%';
                document.getElementById('progressBar').style.width = progress + '%';
            }}

            // 성능 지표 업데이트
            function updateMetrics() {{
                const accuracy = (94.2 + Math.random() * 0.5).toFixed(1);
                const speed = (1.2 + Math.random() * 0.1).toFixed(1);
                const dataset = (2.3 + Math.random() * 0.1).toFixed(1);
                const modelSize = (1.8 + Math.random() * 0.1).toFixed(1);

                document.getElementById('accuracy').textContent = accuracy + '%';
                document.getElementById('speed').textContent = speed + 's';
                document.getElementById('dataset').textContent = dataset + 'M';
                document.getElementById('modelSize').textContent = modelSize + 'GB';
            }}

            // 훈련 제어 함수들
            function startTraining() {{
                addTrainingLog('새로운 훈련 세션을 시작합니다...', 'info');
                document.querySelector('.status-indicator').className = 'status-indicator status-training';
                document.querySelector('.status-indicator').nextSibling.textContent = '훈련 중';
            }}

            function pauseTraining() {{
                addTrainingLog('훈련을 일시정지합니다...', 'warning');
            }}

            function stopTraining() {{
                addTrainingLog('훈련을 중지합니다...', 'error');
                document.querySelector('.status-indicator').className = 'status-indicator status-error';
                document.querySelector('.status-indicator').nextSibling.textContent = '중지됨';
            }}

            // 학습률 슬라이더 업데이트
            document.getElementById('learningRate').addEventListener('input', function() {{
                const value = this.value;
                this.nextElementSibling.textContent = '현재: ' + value;
            }});

            // 페이지 로드 시 초기화
            document.addEventListener('DOMContentLoaded', function() {{
                // 5초마다 훈련 진행률 업데이트
                setInterval(updateTrainingProgress, 5000);
                
                // 10초마다 성능 지표 업데이트
                setInterval(updateMetrics, 10000);
                
                // 30초마다 훈련 로그 추가
                setInterval(() => {{
                    const messages = [
                        'Loss: ' + (2.1 + Math.random() * 0.2).toFixed(4),
                        'Validation Accuracy: ' + (0.94 + Math.random() * 0.01).toFixed(4),
                        'Learning Rate: ' + (0.01 + Math.random() * 0.001).toFixed(4),
                        'Batch Processing: ' + Math.floor(Math.random() * 100) + ' samples/sec'
                    ];
                    addTrainingLog(messages[Math.floor(Math.random() * messages.length)]);
                }}, 30000);
            }});
        </script>
    </body>
    </html>
    """

if __name__ == "__main__":
    uvicorn.run(web_app, host="0.0.0.0", port=8000)
