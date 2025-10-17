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
    return ["ko", "en", "zh"]

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
        <title>🔋 Energy Management System</title>
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
        <nav class="navbar navbar-dark bg-dark">
            <div class="container-fluid">
                <span class="navbar-brand mb-0 h1">
                    <i class="fas fa-bolt"></i> <span data-translate="dashboard_title">Energy Management System</span>
                </span>
                <div class="navbar-nav ms-auto d-flex flex-row">
                    <a class="nav-link me-2" href="/health?lang={lang}">
                        <i class="fas fa-heartbeat"></i> <span data-translate="nav_health">Health</span>
                    </a>
                    <a class="nav-link me-2" href="/model-testing?lang={lang}">
                        <i class="fas fa-brain"></i> <span data-translate="nav_ml_ai">ML/AI Engine</span>
                    </a>
                    <a class="nav-link me-2" href="/data-collection?lang={lang}">
                        <i class="fas fa-chart-bar"></i> <span data-translate="nav_demand">Demand</span>
                    </a>
                    <a class="nav-link me-2" href="/data-collection?lang={lang}">
                        <i class="fas fa-bolt"></i> <span data-translate="nav_supply">Supply</span>
                    </a>
                    <a class="nav-link me-2" href="/statistics?lang={lang}">
                        <i class="fas fa-cogs"></i> <span data-translate="nav_control">Control</span>
                    </a>
                    <a class="nav-link me-2" href="/llm-slm?lang={lang}">
                        <i class="fas fa-lightbulb"></i> <span data-translate="nav_llm_slm">LLM SLM</span>
                    </a>
                    <a class="nav-link me-2" href="/api/docs">
                        <i class="fas fa-file-alt"></i> <span data-translate="nav_api_docs">API Docs</span>
                    </a>
                    <span class="badge bg-success ms-2">
                        <i class="fas fa-circle"></i> <span data-translate="system_online">System Online</span>
                    </span>
                    <!-- 언어 선택 드롭다운 -->
                    <div class="dropdown ms-2">
                        <button class="btn btn-outline-light btn-sm dropdown-toggle" type="button" id="languageDropdown" data-bs-toggle="dropdown">
                            <i class="fas fa-globe"></i> <span data-translate="current_language">한국어</span>
                        </button>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="?lang=ko">🇰🇷 한국어</a></li>
                            <li><a class="dropdown-item" href="?lang=en">🇺🇸 English</a></li>
                            <li><a class="dropdown-item" href="?lang=zh">🇨🇳 中文</a></li>
                        </ul>
                    </div>
                </div>
            </div>
        </nav>

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
                            <h6 class="card-title">System Health</h6>
                            <p class="card-text small text-muted mb-3">
                                Real-time system status monitoring
                            </p>
                            <a href="/health?lang={lang}" class="btn btn-success btn-sm w-100">
                                <i class="fas fa-arrow-right"></i> Health
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
                            <h6 class="card-title">ML/AI Engine</h6>
                            <p class="card-text small text-muted mb-3">
                                ML/AI model management and testing
                            </p>
                            <a href="/model-testing?lang={lang}" class="btn btn-primary btn-sm w-100">
                                <i class="fas fa-arrow-right"></i> ML/AI Engine
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
                            <h6 class="card-title">Energy Demand Monitoring</h6>
                            <p class="card-text small text-muted mb-3">
                                Energy demand analysis and quality management
                            </p>
                            <a href="/data-analysis?lang={lang}" class="btn btn-info btn-sm w-100">
                                <i class="fas fa-arrow-right"></i> Demand
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
                            <h6 class="card-title">Energy Supply Monitoring</h6>
                            <p class="card-text small text-muted mb-3">
                                Energy supply monitoring and management
                            </p>
                            <a href="/data-collection?lang={lang}" class="btn btn-warning btn-sm w-100">
                                <i class="fas fa-arrow-right"></i> Supply
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
                            <h6 class="card-title">Demand Control</h6>
                            <p class="card-text small text-muted mb-3">
                                Demand control and system management
                            </p>
                            <a href="/statistics?lang={lang}" class="btn btn-danger btn-sm w-100">
                                <i class="fas fa-arrow-right"></i> Control
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
        <title>🔍 Digital Experience Intelligence Platform</title>
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
        <title>🎛️ Demand Control - Smart Grid Management</title>
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
        <nav class="navbar navbar-dark bg-dark">
            <div class="container-fluid">
                <span class="navbar-brand mb-0 h1">
                    <i class="fas fa-sliders-h"></i> <span data-translate="demand_control_title">Demand Control</span>
                </span>
                <div class="navbar-nav ms-auto d-flex flex-row">
                    <a href="/?lang={lang}" class="btn btn-outline-light btn-sm me-2">
                        <i class="fas fa-home"></i> <span data-translate="nav_home">Dashboard</span>
                    </a>
                    <!-- 언어 선택 드롭다운 -->
                    <div class="dropdown">
                        <button class="btn btn-outline-light btn-sm dropdown-toggle" type="button" id="languageDropdown" data-bs-toggle="dropdown" aria-expanded="false">
                            <i class="fas fa-globe"></i> <span id="currentLanguage">한국어</span>
                        </button>
                        <ul class="dropdown-menu" aria-labelledby="languageDropdown">
                            <li><a class="dropdown-item" href="?lang=ko">🇰🇷 한국어</a></li>
                            <li><a class="dropdown-item" href="?lang=en">🇺🇸 English</a></li>
                            <li><a class="dropdown-item" href="?lang=zh">🇨🇳 中文</a></li>
                        </ul>
                    </div>
                </div>
            </div>
        </nav>

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
        <title>⚡ Energy Supply & Weather Analysis Dashboard</title>
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
        <nav class="navbar navbar-dark bg-dark">
            <div class="container-fluid">
                <span class="navbar-brand mb-0 h1">
                    <i class="fas fa-bolt"></i> <span data-translate="energy_supply_title">Energy Supply & Weather Analysis</span>
                </span>
                <div class="navbar-nav ms-auto d-flex flex-row">
                    <a href="/?lang={lang}" class="btn btn-outline-light btn-sm me-2">
                        <i class="fas fa-home"></i> <span data-translate="nav_home">Dashboard</span>
                    </a>
                    <!-- 언어 선택 드롭다운 -->
                    <div class="dropdown">
                        <button class="btn btn-outline-light btn-sm dropdown-toggle" type="button" id="languageDropdown" data-bs-toggle="dropdown" aria-expanded="false">
                            <i class="fas fa-globe"></i> <span id="currentLanguage">한국어</span>
                        </button>
                        <ul class="dropdown-menu" aria-labelledby="languageDropdown">
                            <li><a class="dropdown-item" href="?lang=ko">🇰🇷 한국어</a></li>
                            <li><a class="dropdown-item" href="?lang=en">🇺🇸 English</a></li>
                            <li><a class="dropdown-item" href="?lang=zh">🇨🇳 中文</a></li>
                        </ul>
                    </div>
                </div>
            </div>
        </nav>

        <div class="container-fluid mt-4">
            <!-- 실시간 에너지 공급 현황 -->
            <div class="row">
                <div class="col-12">
                    <div class="dashboard-card">
                        <h4><i class="fas fa-chart-line"></i> Real-time Energy Supply Status</h4>
                        <div class="row">
                            <div class="col-md-3">
                                <div class="metric-card">
                                    <div class="metric-value" id="totalGeneration">5.2 kW</div>
                                    <div class="metric-label">Total Generation</div>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="metric-card">
                                    <div class="metric-value" id="solarGeneration">3.2 kW</div>
                                    <div class="metric-label">Solar Generation</div>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="metric-card">
                                    <div class="metric-value" id="windGeneration">1.8 kW</div>
                                    <div class="metric-label">Wind Generation</div>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="metric-card">
                                    <div class="metric-value" id="systemEfficiency">94.2%</div>
                                    <div class="metric-label">System Efficiency</div>
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
                            <h6><i class="fas fa-wind"></i> Wind vs Speed</h6>
                            <div class="mb-2">
                                <small>Correlation: <strong id="windCorrelation">0.92</strong></small>
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
                                                <th>Wind (kW)</th>
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
                const windGen = (Math.random() * 1.5 + 1.2).toFixed(1);
                const totalGen = (parseFloat(solarGen) + parseFloat(windGen)).toFixed(1);
                const efficiency = (Math.random() * 5 + 92).toFixed(1);

                document.getElementById('totalGeneration').textContent = totalGen + ' kW';
                document.getElementById('solarGeneration').textContent = solarGen + ' kW';
                document.getElementById('windGeneration').textContent = windGen + ' kW';
                document.getElementById('systemEfficiency').textContent = efficiency + '%';

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
                document.getElementById('windCorrelation').textContent = windCorr;
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
                            label: 'Wind Generation',
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
                        labels: ['Solar', 'Wind', 'Storage'],
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
                        labels: ['Solar', 'Wind', 'Efficiency', 'Storage'],
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
        <title>🏭 시설 모니터링 및 데이터 분석</title>
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
        <nav class="navbar navbar-dark bg-dark">
            <div class="container-fluid">
                <span class="navbar-brand mb-0 h1">
                    <i class="fas fa-industry"></i> <span data-translate="facility_monitoring">시설 모니터링 및 데이터 분석</span>
                </span>
                <div class="navbar-nav ms-auto d-flex flex-row">
                    <a href="/?lang={lang}" class="btn btn-outline-light btn-sm me-2">
                        <i class="fas fa-home"></i> <span data-translate="nav_home">Dashboard</span>
                    </a>
                    <!-- 언어 선택 드롭다운 -->
                    <div class="dropdown">
                        <button class="btn btn-outline-light btn-sm dropdown-toggle" type="button" id="languageDropdown" data-bs-toggle="dropdown">
                            <i class="fas fa-globe"></i> <span data-translate="current_language">한국어</span>
                        </button>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="?lang=ko">🇰🇷 한국어</a></li>
                            <li><a class="dropdown-item" href="?lang=en">🇺🇸 English</a></li>
                            <li><a class="dropdown-item" href="?lang=zh">🇨🇳 中文</a></li>
                        </ul>
                    </div>
                </div>
            </div>
        </nav>

        <div class="container-fluid mt-4">
            <!-- 시설 정보 -->
            <div class="row mb-4">
                <div class="col-12">
                    <div class="facility-info">
                        <h4><i class="fas fa-map-marker-alt"></i> 시설 위치 및 정보</h4>
                        <div class="row">
                            <div class="col-md-3">
                                <h6>시설명</h6>
                                <p><strong>서울 에너지 센터</strong></p>
                            </div>
                            <div class="col-md-3">
                                <h6>위치</h6>
                                <p><strong>서울특별시 강남구 테헤란로 123</strong></p>
                            </div>
                            <div class="col-md-3">
                                <h6>시설 유형</h6>
                                <p><strong>스마트 그리드 시설</strong></p>
                            </div>
                            <div class="col-md-3">
                                <h6>운영 상태</h6>
                                <p><span class="status-indicator status-online"></span><strong>정상 운영</strong></p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 센서링 데이터 모니터링 -->
            <div class="row mb-4">
                <div class="col-12">
                    <div class="monitoring-card">
                        <h5><i class="fas fa-microchip"></i> 센서링 데이터 실시간 모니터링</h5>
                        <div class="row">
                            <div class="col-md-3">
                                <div class="sensor-card text-center">
                                    <h6>온도 센서</h6>
                                    <div class="metric-value" id="temperature">23.5°C</div>
                                    <div class="metric-label">실내 온도</div>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="sensor-card text-center">
                                    <h6>습도 센서</h6>
                                    <div class="metric-value" id="humidity">65%</div>
                                    <div class="metric-label">실내 습도</div>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="sensor-card text-center">
                                    <h6>진동 센서</h6>
                                    <div class="metric-value" id="vibration">0.2g</div>
                                    <div class="metric-label">기계 진동</div>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="sensor-card text-center">
                                    <h6>압력 센서</h6>
                                    <div class="metric-value" id="pressure">101.3 kPa</div>
                                    <div class="metric-label">기압</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 전력 데이터 실시간 모니터링 -->
            <div class="row mb-4">
                <div class="col-12">
                    <div class="monitoring-card">
                        <h5><i class="fas fa-bolt"></i> 전력 데이터 실시간 모니터링</h5>
                        <div class="row">
                            <div class="col-md-3">
                                <div class="power-card text-center">
                                    <h6>총 전력 소비</h6>
                                    <div class="metric-value" id="totalPower">1,250 kW</div>
                                    <div class="metric-label">현재 소비량</div>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="power-card text-center">
                                    <h6>피크 전력</h6>
                                    <div class="metric-value" id="peakPower">1,450 kW</div>
                                    <div class="metric-label">최대 소비량</div>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="power-card text-center">
                                    <h6>전력 효율</h6>
                                    <div class="metric-value" id="powerEfficiency">94.2%</div>
                                    <div class="metric-label">시스템 효율</div>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="power-card text-center">
                                    <h6>일일 소비량</h6>
                                    <div class="metric-value" id="dailyConsumption">28.5 MWh</div>
                                    <div class="metric-label">오늘 소비량</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 시계열 데이터 차트 -->
            <div class="row mb-4">
                <div class="col-lg-8">
                    <div class="monitoring-card">
                        <h5><i class="fas fa-chart-line"></i> 시계열 데이터 분석</h5>
                        <canvas id="timeSeriesChart" class="chart-container"></canvas>
                    </div>
                </div>
                <div class="col-lg-4">
                    <div class="monitoring-card">
                        <h5><i class="fas fa-calendar-alt"></i> 구글 일정 연동</h5>
                        <div class="calendar-card">
                            <h6>오늘의 일정</h6>
                            <div class="event-timeline" id="calendarEvents">
                                <div class="event-item">
                                    <div class="event-time">09:00 - 10:00</div>
                                    <div class="event-content">
                                        <strong>시설 점검</strong><br>
                                        <small>정기 시설 점검 및 유지보수</small>
                                    </div>
                                </div>
                                <div class="event-item">
                                    <div class="event-time">14:00 - 15:00</div>
                                    <div class="event-content">
                                        <strong>데이터 분석 회의</strong><br>
                                        <small>주간 데이터 분석 결과 검토</small>
                                    </div>
                                </div>
                                <div class="event-item">
                                    <div class="event-time">16:30 - 17:30</div>
                                    <div class="event-content">
                                        <strong>시스템 업데이트</strong><br>
                                        <small>센서 시스템 소프트웨어 업데이트</small>
                                    </div>
                                </div>
                            </div>
                            <button class="btn btn-primary btn-sm mt-2" onclick="syncGoogleCalendar()">
                                <i class="fas fa-sync"></i> 구글 일정 동기화
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 이벤트 및 메모 기능 -->
            <div class="row mb-4">
                <div class="col-lg-6">
                    <div class="monitoring-card">
                        <h5><i class="fas fa-history"></i> 시계열 이벤트 타임라인</h5>
                        <div class="event-timeline" id="eventTimeline">
                            <div class="event-item">
                                <div class="event-time">2024-01-15 10:30:15</div>
                                <div class="event-content">
                                    <strong>전력 소비 급증</strong><br>
                                    <small>전력 소비량이 평균 대비 15% 증가</small>
                                    <div class="memo-input">
                                        <textarea class="form-control form-control-sm" placeholder="이벤트에 대한 메모를 입력하세요..." rows="2"></textarea>
                                        <button class="btn btn-primary btn-sm mt-1" onclick="saveMemo(this)">메모 저장</button>
                                    </div>
                                </div>
                            </div>
                            <div class="event-item">
                                <div class="event-time">2024-01-15 09:45:22</div>
                                <div class="event-content">
                                    <strong>온도 센서 이상</strong><br>
                                    <small>온도 센서 값이 정상 범위를 벗어남</small>
                                    <div class="memo-input">
                                        <textarea class="form-control form-control-sm" placeholder="이벤트에 대한 메모를 입력하세요..." rows="2"></textarea>
                                        <button class="btn btn-primary btn-sm mt-1" onclick="saveMemo(this)">메모 저장</button>
                                    </div>
                                </div>
                            </div>
                            <div class="event-item">
                                <div class="event-time">2024-01-15 08:15:33</div>
                                <div class="event-content">
                                    <strong>시스템 시작</strong><br>
                                    <small>모니터링 시스템이 정상적으로 시작됨</small>
                                    <div class="memo-input">
                                        <textarea class="form-control form-control-sm" placeholder="이벤트에 대한 메모를 입력하세요..." rows="2"></textarea>
                                        <button class="btn btn-primary btn-sm mt-1" onclick="saveMemo(this)">메모 저장</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-lg-6">
                    <div class="monitoring-card">
                        <h5><i class="fas fa-sticky-note"></i> 사용자 이벤트 및 메모</h5>
                        <div class="mb-3">
                            <button class="btn btn-success btn-sm" onclick="addUserEvent()">
                                <i class="fas fa-plus"></i> 새 이벤트 추가
                            </button>
                            <button class="btn btn-info btn-sm ms-2" onclick="exportEvents()">
                                <i class="fas fa-download"></i> 이벤트 내보내기
                            </button>
                        </div>
                        <div class="event-timeline" id="userEvents">
                            <div class="event-item">
                                <div class="event-time">2024-01-15 11:20:45</div>
                                <div class="event-content">
                                    <strong>사용자 메모</strong><br>
                                    <small>시설 점검 완료. 모든 시스템 정상 작동 중.</small>
                                </div>
                            </div>
                            <div class="event-item">
                                <div class="event-time">2024-01-15 10:45:12</div>
                                <div class="event-content">
                                    <strong>알림 설정</strong><br>
                                    <small>전력 소비량 임계값 알림 설정 완료</small>
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
                // 센서 데이터 업데이트
                const temperature = (Math.random() * 10 + 20).toFixed(1);
                const humidity = (Math.random() * 20 + 50).toFixed(0);
                const vibration = (Math.random() * 0.5).toFixed(1);
                const pressure = (Math.random() * 5 + 100).toFixed(1);

                document.getElementById('temperature').textContent = temperature + '°C';
                document.getElementById('humidity').textContent = humidity + '%';
                document.getElementById('vibration').textContent = vibration + 'g';
                document.getElementById('pressure').textContent = pressure + ' kPa';

                // 전력 데이터 업데이트
                const totalPower = (Math.random() * 200 + 1200).toFixed(0);
                const peakPower = (Math.random() * 100 + 1400).toFixed(0);
                const powerEfficiency = (Math.random() * 5 + 92).toFixed(1);
                const dailyConsumption = (Math.random() * 5 + 27).toFixed(1);

                document.getElementById('totalPower').textContent = totalPower + ' kW';
                document.getElementById('peakPower').textContent = peakPower + ' kW';
                document.getElementById('powerEfficiency').textContent = powerEfficiency + '%';
                document.getElementById('dailyConsumption').textContent = dailyConsumption + ' MWh';
            }}

            // 시계열 차트 초기화
            function initTimeSeriesChart() {{
                const ctx = document.getElementById('timeSeriesChart').getContext('2d');
                const hours = [];
                const powerData = [];
                const temperatureData = [];
                
                for (let i = 0; i < 24; i++) {{
                    hours.push(i.toString().padStart(2, '0') + ':00');
                    powerData.push(Math.random() * 200 + 1200);
                    temperatureData.push(Math.random() * 10 + 20);
                }}
                
                new Chart(ctx, {{
                    type: 'line',
                    data: {{
                        labels: hours,
                        datasets: [{{
                            label: '전력 소비 (kW)',
                            data: powerData,
                            borderColor: '#ff6b6b',
                            backgroundColor: 'rgba(255, 107, 107, 0.1)',
                            tension: 0.4,
                            yAxisID: 'y'
                        }}, {{
                            label: '온도 (°C)',
                            data: temperatureData,
                            borderColor: '#4ecdc4',
                            backgroundColor: 'rgba(78, 205, 196, 0.1)',
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
                                    text: '전력 소비 (kW)'
                                }}
                            }},
                            y1: {{
                                type: 'linear',
                                display: true,
                                position: 'right',
                                title: {{
                                    display: true,
                                    text: '온도 (°C)'
                                }},
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

            // 구글 일정 동기화
            function syncGoogleCalendar() {{
                // 구글 일정 API 연동 시뮬레이션
                const calendarEvents = document.getElementById('calendarEvents');
                const newEvent = document.createElement('div');
                newEvent.className = 'event-item';
                newEvent.innerHTML = `
                    <div class="event-time">${{new Date().toLocaleTimeString()}}</div>
                    <div class="event-content">
                        <strong>새 일정 추가됨</strong><br>
                        <small>구글 일정에서 동기화된 새로운 일정</small>
                    </div>
                `;
                calendarEvents.insertBefore(newEvent, calendarEvents.firstChild);
            }}

            // 메모 저장
            function saveMemo(button) {{
                const textarea = button.previousElementSibling;
                const memo = textarea.value.trim();
                if (memo) {{
                    // 메모 저장 로직
                    button.textContent = '저장됨';
                    button.className = 'btn btn-success btn-sm mt-1';
                    textarea.disabled = true;
                }}
            }}

            // 새 사용자 이벤트 추가
            function addUserEvent() {{
                const userEvents = document.getElementById('userEvents');
                const newEvent = document.createElement('div');
                newEvent.className = 'event-item';
                newEvent.innerHTML = `
                    <div class="event-time">${{new Date().toLocaleString()}}</div>
                    <div class="event-content">
                        <strong>새 사용자 이벤트</strong><br>
                        <small>사용자가 추가한 새로운 이벤트</small>
                    </div>
                `;
                userEvents.insertBefore(newEvent, userEvents.firstChild);
            }}

            // 이벤트 내보내기
            function exportEvents() {{
                // 이벤트 데이터를 CSV나 JSON 형태로 내보내기
                alert('이벤트 데이터가 내보내기되었습니다.');
            }}

            // 초기화
            document.addEventListener('DOMContentLoaded', function() {{
                initTimeSeriesChart();
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
        <title>🤖 MCP 기반 자동화 ML/AI Engine</title>
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
        <nav class="navbar navbar-dark bg-dark">
            <div class="container-fluid">
                <span class="navbar-brand mb-0 h1">
                    <i class="fas fa-robot"></i> <span data-translate="mcp_ai_engine">MCP 기반 자동화 ML/AI Engine</span>
                </span>
                <div class="navbar-nav ms-auto d-flex flex-row">
                    <a href="/?lang={lang}" class="btn btn-outline-light btn-sm me-2">
                        <i class="fas fa-home"></i> <span data-translate="nav_home">Dashboard</span>
                    </a>
                    <a href="/health?lang={lang}" class="btn btn-outline-light btn-sm me-2">
                        <i class="fas fa-heartbeat"></i> <span data-translate="nav_health">Health</span>
                    </a>
                    <!-- 언어 선택 드롭다운 -->
                    <div class="dropdown">
                        <button class="btn btn-outline-light btn-sm dropdown-toggle" type="button" id="languageDropdown" data-bs-toggle="dropdown">
                            <i class="fas fa-globe"></i> <span data-translate="current_language">한국어</span>
                        </button>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="?lang=ko">🇰🇷 한국어</a></li>
                            <li><a class="dropdown-item" href="?lang=en">🇺🇸 English</a></li>
                            <li><a class="dropdown-item" href="?lang=zh">🇨🇳 中文</a></li>
                        </ul>
                    </div>
                </div>
            </div>
        </nav>

        <div class="container-fluid mt-4">
            <!-- 헤더 -->
            <div class="row mb-4">
                <div class="col-12">
                    <div class="mcp-card">
                        <h1 class="mb-2">
                            <i class="fas fa-robot"></i> MCP 기반 자동화 ML/AI Engine
                        </h1>
                        <p class="mb-0">Model Context Protocol을 활용한 지능형 에이전트 기반 머신러닝 파이프라인 자동화 시스템</p>
                    </div>
                </div>
            </div>

            <!-- MCP 에이전트 상태 -->
            <div class="row mb-4">
                <div class="col-12">
                    <div class="agent-status">
                        <h5><i class="fas fa-brain"></i> MCP 에이전트 상태</h5>
                        <div class="row">
                            <div class="col-md-3">
                                <div class="text-center">
                                    <h6>Agent Status</h6>
                                    <span class="badge bg-success fs-6" id="agentStatus">Active</span>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="text-center">
                                    <h6>Current Task</h6>
                                    <span id="currentTask">Data Collection</span>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="text-center">
                                    <h6>Progress</h6>
                                    <div class="progress-step">
                                        <div class="progress-fill" id="overallProgress" style="width: 20%"></div>
                                    </div>
                                    <small id="progressText">20% Complete</small>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="text-center">
                                    <button class="btn btn-primary" onclick="startMCPPipeline()">
                                        <i class="fas fa-play"></i> Start Pipeline
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

if __name__ == "__main__":
    uvicorn.run(web_app, host="0.0.0.0", port=8000)
