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
                            <a href="/data-collection?lang={lang}" class="btn btn-info btn-sm w-100">
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
    """Energy Supply Monitoring 페이지"""
    # 언어 설정
    if lang not in get_available_languages():
        lang = "ko"
    
    return f"""
    <!DOCTYPE html>
    <html lang="{lang}">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>⚡ Energy Supply Monitoring Dashboard</title>
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
        </style>
    </head>
    <body>
        <nav class="navbar navbar-dark bg-dark">
            <div class="container-fluid">
                <span class="navbar-brand mb-0 h1">
                    <i class="fas fa-bolt"></i> <span data-translate="energy_supply_title">Energy Supply Monitoring</span>
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

            <!-- 에너지 공급 차트 -->
            <div class="row">
                <div class="col-lg-8">
                    <div class="dashboard-card">
                        <h5><i class="fas fa-chart-area"></i> Energy Generation Trends</h5>
                        <canvas id="generationChart" class="chart-container"></canvas>
                    </div>
                </div>
                <div class="col-lg-4">
                    <div class="dashboard-card">
                        <h5><i class="fas fa-chart-pie"></i> Energy Mix Distribution</h5>
                        <canvas id="energyMixChart" class="chart-container"></canvas>
                    </div>
                </div>
            </div>

            <!-- 시스템 상태 모니터링 -->
            <div class="row">
                <div class="col-12">
                    <div class="dashboard-card">
                        <h5><i class="fas fa-cogs"></i> System Status Monitoring</h5>
                        <div class="row">
                            <div class="col-md-4">
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
                            <div class="col-md-4">
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
                            <div class="col-md-4">
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

@web_app.get("/model-testing", response_class=HTMLResponse)
async def model_testing_page(request: Request, lang: str = Query("ko", description="Language code")):
    """ML/AI Engine 페이지"""
    # 언어 설정
    if lang not in get_available_languages():
        lang = "ko"
    
    return f"""
    <!DOCTYPE html>
    <html lang="{lang}">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🧠 ML/AI Engine</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            .model-card {{
                transition: transform 0.2s;
                border: none;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }}
            .model-card:hover {{
                transform: translateY(-5px);
                box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
            }}
            .performance-controls {{
                background: rgba(255, 255, 255, 0.95);
                border-radius: 15px;
                padding: 20px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }}
            .model-selection {{
                margin-bottom: 20px;
            }}
            .form-check {{
                padding: 10px;
                border: 2px solid transparent;
                border-radius: 8px;
                transition: all 0.3s ease;
            }}
            .form-check:hover {{
                background: #f8f9fa;
                border-color: #e9ecef;
            }}
            .form-check-input:checked + .form-check-label {{
                color: #007bff;
            }}
            .form-check:has(.form-check-input:checked) {{
                background: #e3f2fd;
                border-color: #2196f3;
            }}
            .model-actions .btn {{
                margin-bottom: 10px;
                transition: all 0.3s ease;
            }}
            .model-actions .btn:hover {{
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }}
            .selected-model-info {{
                animation: fadeIn 0.5s ease-in;
            }}
            @keyframes fadeIn {{
                from {{ opacity: 0; transform: translateY(10px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
            .metric-card {{
                background: rgba(255, 255, 255, 0.9);
                border-radius: 10px;
                padding: 15px;
                margin-bottom: 15px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }}
            .metric-card h6 {{
                color: #333;
                margin-bottom: 15px;
                font-weight: bold;
            }}
        </style>
    </head>
    <body class="bg-light">
        <nav class="navbar navbar-dark bg-dark">
            <div class="container-fluid">
                <span class="navbar-brand mb-0 h1">
                    <i class="fas fa-brain"></i> <span data-translate="ml_ai_engine">ML/AI Engine</span>
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
                    <div class="card bg-primary text-white">
                        <div class="card-body">
                            <h1 class="card-title mb-2">
                                <i class="fas fa-brain"></i> ML/AI Engine
                            </h1>
                            <p class="card-text">Machine Learning and Artificial Intelligence Model Management and Testing Platform</p>
                        </div>
                    </div>
                </div>
            </div>

            <div class="row">
                <!-- 모델 선택 및 제어 -->
                <div class="col-md-4">
                    <div class="performance-controls">
                        <h5 class="mb-4">
                            <i class="fas fa-cogs"></i> Model Selection & Control
                        </h5>
                        
                        <!-- 모델 선택 -->
                        <div class="model-selection">
                            <h6 class="mb-3">Available Models:</h6>
                            <div class="form-check">
                                <input class="form-check-input" type="radio" name="modelSelect" id="model1" value="energy-forecast-v1" checked>
                                <label class="form-check-label" for="model1">
                                    <strong>Energy Forecast v1.0</strong><br>
                                    <small class="text-muted">Time series forecasting for energy consumption</small>
                                </label>
                            </div>
                            <div class="form-check">
                                <input class="form-check-input" type="radio" name="modelSelect" id="model2" value="demand-predict-v2">
                                <label class="form-check-label" for="model2">
                                    <strong>Demand Predict v2.0</strong><br>
                                    <small class="text-muted">Advanced demand prediction with weather integration</small>
                                </label>
                            </div>
                            <div class="form-check">
                                <input class="form-check-input" type="radio" name="modelSelect" id="model3" value="anomaly-detection-v1">
                                <label class="form-check-label" for="model3">
                                    <strong>Anomaly Detection v1.0</strong><br>
                                    <small class="text-muted">Real-time anomaly detection for energy systems</small>
                                </label>
                            </div>
                        </div>

                        <!-- 모델 액션 -->
                        <div class="model-actions">
                            <button class="btn btn-primary w-100" onclick="loadModel()">
                                <i class="fas fa-download"></i> Load Model
                            </button>
                            <button class="btn btn-success w-100" onclick="trainModel()">
                                <i class="fas fa-play"></i> Train Model
                            </button>
                            <button class="btn btn-warning w-100" onclick="testModel()">
                                <i class="fas fa-vial"></i> Test Model
                            </button>
                            <button class="btn btn-info w-100" onclick="evaluateModel()">
                                <i class="fas fa-chart-line"></i> Evaluate Performance
                            </button>
                            <button class="btn btn-secondary w-100" onclick="exportModel()">
                                <i class="fas fa-download"></i> Export Model
                            </button>
                        </div>

                        <!-- 선택된 모델 정보 -->
                        <div id="selectedModelInfo" class="selected-model-info mt-4" style="display: none;">
                            <h6>Selected Model Information:</h6>
                            <div class="alert alert-info">
                                <strong>Model:</strong> <span id="selectedModelName">-</span><br>
                                <strong>Version:</strong> <span id="selectedModelVersion">-</span><br>
                                <strong>Status:</strong> <span id="selectedModelStatus">-</span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 모델 성능 메트릭 -->
                <div class="col-md-8">
                    <div class="row">
                        <div class="col-md-6">
                            <div class="metric-card">
                                <h6><i class="fas fa-chart-line"></i> Model Performance</h6>
                                <div class="mb-2">
                                    <small>Accuracy: <strong id="modelAccuracy">-</strong></small>
                                    <div class="progress">
                                        <div class="progress-bar bg-success" id="accuracyBar" style="width: 0%"></div>
                                    </div>
                                </div>
                                <div class="mb-2">
                                    <small>Precision: <strong id="modelPrecision">-</strong></small>
                                    <div class="progress">
                                        <div class="progress-bar bg-info" id="precisionBar" style="width: 0%"></div>
                                    </div>
                                </div>
                                <div class="mb-2">
                                    <small>Recall: <strong id="modelRecall">-</strong></small>
                                    <div class="progress">
                                        <div class="progress-bar bg-warning" id="recallBar" style="width: 0%"></div>
                                    </div>
                                </div>
                                <div class="mb-2">
                                    <small>F1-Score: <strong id="modelF1">-</strong></small>
                                    <div class="progress">
                                        <div class="progress-bar bg-danger" id="f1Bar" style="width: 0%"></div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="metric-card">
                                <h6><i class="fas fa-clock"></i> Training Status</h6>
                                <div class="mb-2">
                                    <small>Epoch: <strong id="currentEpoch">-</strong></small>
                                    <div class="progress">
                                        <div class="progress-bar bg-primary" id="epochBar" style="width: 0%"></div>
                                    </div>
                                </div>
                                <div class="mb-2">
                                    <small>Loss: <strong id="currentLoss">-</strong></small>
                                    <div class="progress">
                                        <div class="progress-bar bg-secondary" id="lossBar" style="width: 0%"></div>
                                    </div>
                                </div>
                                <div class="mb-2">
                                    <small>Learning Rate: <strong id="learningRate">-</strong></small>
                                </div>
                                <div class="mb-2">
                                    <small>Status: <span class="badge bg-success" id="trainingStatus">Ready</span></small>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- 모델 테스트 결과 -->
                    <div class="card mt-4">
                        <div class="card-header">
                            <h5 class="mb-0">
                                <i class="fas fa-vial"></i> Model Test Results
                            </h5>
                        </div>
                        <div class="card-body">
                            <div id="testResults">
                                <p class="text-muted">No test results available. Please run a test first.</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
        <script>
            // 모델 선택 이벤트
            document.querySelectorAll('input[name="modelSelect"]').forEach(radio => {{
                radio.addEventListener('change', function() {{
                    updateSelectedModelInfo(this.value);
                }});
            }});

            // 모델 정보 업데이트
            function updateSelectedModelInfo(modelId) {{
                const modelInfo = {{
                    'energy-forecast-v1': {{ name: 'Energy Forecast', version: 'v1.0', status: 'Ready' }},
                    'demand-predict-v2': {{ name: 'Demand Predict', version: 'v2.0', status: 'Training' }},
                    'anomaly-detection-v1': {{ name: 'Anomaly Detection', version: 'v1.0', status: 'Ready' }}
                }};

                const info = modelInfo[modelId];
                if (info) {{
                    document.getElementById('selectedModelName').textContent = info.name;
                    document.getElementById('selectedModelVersion').textContent = info.version;
                    document.getElementById('selectedModelStatus').textContent = info.status;
                    document.getElementById('selectedModelInfo').style.display = 'block';
                }}
            }}

            // 모델 로드
            function loadModel() {{
                const selectedModel = document.querySelector('input[name="modelSelect"]:checked').value;
                showNotification(`Loading model: ${{selectedModel}}`, 'info');
                updateMetrics();
            }}

            // 모델 훈련
            function trainModel() {{
                const selectedModel = document.querySelector('input[name="modelSelect"]:checked').value;
                showNotification(`Training model: ${{selectedModel}}`, 'warning');
                simulateTraining();
            }}

            // 모델 테스트
            function testModel() {{
                const selectedModel = document.querySelector('input[name="modelSelect"]:checked').value;
                showNotification(`Testing model: ${{selectedModel}}`, 'info');
                simulateTest();
            }}

            // 모델 평가
            function evaluateModel() {{
                const selectedModel = document.querySelector('input[name="modelSelect"]:checked').value;
                showNotification(`Evaluating model: ${{selectedModel}}`, 'success');
                updateMetrics();
            }}

            // 모델 내보내기
            function exportModel() {{
                const selectedModel = document.querySelector('input[name="modelSelect"]:checked').value;
                showNotification(`Exporting model: ${{selectedModel}}`, 'info');
            }}

            // 메트릭 업데이트
            function updateMetrics() {{
                // 랜덤 메트릭 생성
                const accuracy = (Math.random() * 0.3 + 0.7).toFixed(3);
                const precision = (Math.random() * 0.3 + 0.7).toFixed(3);
                const recall = (Math.random() * 0.3 + 0.7).toFixed(3);
                const f1 = (Math.random() * 0.3 + 0.7).toFixed(3);

                document.getElementById('modelAccuracy').textContent = accuracy;
                document.getElementById('modelPrecision').textContent = precision;
                document.getElementById('modelRecall').textContent = recall;
                document.getElementById('modelF1').textContent = f1;

                document.getElementById('accuracyBar').style.width = (accuracy * 100) + '%';
                document.getElementById('precisionBar').style.width = (precision * 100) + '%';
                document.getElementById('recallBar').style.width = (recall * 100) + '%';
                document.getElementById('f1Bar').style.width = (f1 * 100) + '%';
            }}

            // 훈련 시뮬레이션
            function simulateTraining() {{
                let epoch = 0;
                const maxEpochs = 100;
                const trainingInterval = setInterval(() => {{
                    epoch++;
                    const progress = (epoch / maxEpochs) * 100;
                    const loss = Math.max(0.1, 1.0 - (epoch / maxEpochs) * 0.8);

                    document.getElementById('currentEpoch').textContent = epoch;
                    document.getElementById('currentLoss').textContent = loss.toFixed(4);
                    document.getElementById('epochBar').style.width = progress + '%';
                    document.getElementById('lossBar').style.width = (loss * 100) + '%';
                    document.getElementById('trainingStatus').textContent = 'Training';
                    document.getElementById('trainingStatus').className = 'badge bg-warning';

                    if (epoch >= maxEpochs) {{
                        clearInterval(trainingInterval);
                        document.getElementById('trainingStatus').textContent = 'Completed';
                        document.getElementById('trainingStatus').className = 'badge bg-success';
                        showNotification('Training completed successfully!', 'success');
                    }}
                }}, 100);
            }}

            // 테스트 시뮬레이션
            function simulateTest() {{
                const testResults = document.getElementById('testResults');
                testResults.innerHTML = `
                    <div class="alert alert-success">
                        <h6><i class="fas fa-check-circle"></i> Test Results</h6>
                        <ul class="mb-0">
                            <li>Test Accuracy: <strong>${{(Math.random() * 0.2 + 0.8).toFixed(3)}}</strong></li>
                            <li>Test Loss: <strong>${{(Math.random() * 0.1 + 0.05).toFixed(4)}}</strong></li>
                            <li>Inference Time: <strong>${{(Math.random() * 50 + 10).toFixed(1)}}ms</strong></li>
                            <li>Memory Usage: <strong>${{(Math.random() * 200 + 100).toFixed(1)}}MB</strong></li>
                        </ul>
                    </div>
                `;
            }}

            // 알림 표시
            function showNotification(message, type) {{
                const alertDiv = document.createElement('div');
                alertDiv.className = `alert alert-${{type}} alert-dismissible fade show`;
                alertDiv.innerHTML = `
                    ${{message}}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                `;
                
                const container = document.querySelector('.container-fluid');
                container.insertBefore(alertDiv, container.firstChild);
                
                setTimeout(() => {{
                    alertDiv.remove();
                }}, 3000);
            }}

            // 초기화
            document.addEventListener('DOMContentLoaded', function() {{
                updateSelectedModelInfo('energy-forecast-v1');
                updateMetrics();
            }});
        </script>
    </body>
    </html>
    """

if __name__ == "__main__":
    uvicorn.run(web_app, host="0.0.0.0", port=8000)
