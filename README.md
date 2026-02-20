<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 400">
    <defs>
        <pattern id="wp" width="80" height="80" patternUnits="userSpaceOnUse">
            <path d="M 40 0 L 80 40 L 40 80 L 0 40 Z" fill="#1b1425"/>
            <circle cx="40" cy="40" r="8" fill="#140f1c"/>
            <path d="M 40 20 L 60 40 L 40 60 L 20 40 Z" fill="none" stroke="#231a30" stroke-width="2"/>
        </pattern>
        <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="6" result="blur" />
            <feComposite in="SourceGraphic" in2="blur" operator="over" />
        </filter>
        <linearGradient id="beam-grad" x1="0%" y1="50%" x2="100%" y2="50%">
            <stop offset="0%" stop-color="#fef08a" stop-opacity="0.5"/>
            <stop offset="100%" stop-color="#fef08a" stop-opacity="0"/>
        </linearGradient>
        <g id="ghost-shape" fill="#88ffd1" opacity="0.8">
            <path d="M 25 0 C 45 0 50 20 50 40 C 50 60 45 70 35 80 C 30 85 20 75 15 80 C 10 85 5 75 0 80 C -5 70 -5 60 0 40 C 0 20 5 0 25 0 Z" filter="url(#glow)"/>
            <ellipse cx="18" cy="30" rx="3" ry="6" fill="#04020a"/>
            <ellipse cx="32" cy="30" rx="3" ry="6" fill="#04020a"/>
            <circle cx="25" cy="45" r="4" fill="#04020a"/>
        </g>
        <g id="bg-wall">
            <rect width="800" height="320" fill="#140f1c"/>
            <rect width="800" height="320" fill="url(#wp)"/>
            <g transform="translate(150, 60)">
                <rect x="0" y="0" width="140" height="180" rx="5" fill="#1a1c29"/>
                <circle cx="100" cy="40" r="25" fill="#fef08a" filter="url(#glow)"/>
                <circle cx="95" cy="35" r="5" fill="#eab308" opacity="0.3"/>
                <rect x="0" y="0" width="140" height="180" fill="#ffffff" class="lightning" rx="5"/>
                <path d="M 0 180 L 40 100 L 45 100 L 25 180 Z" fill="#0a0f18"/>
                <path d="M 35 120 L 70 90 L 75 95 L 40 130 Z" fill="#0a0f18"/>
                <rect x="0" y="0" width="140" height="180" rx="5" fill="none" stroke="#0a0f18" stroke-width="12"/>
                <line x1="70" y1="0" x2="70" y2="180" stroke="#0a0f18" stroke-width="8"/>
                <line x1="0" y1="90" x2="140" y2="90" stroke="#0a0f18" stroke-width="8"/>
            </g>
            <g transform="translate(420, 120)">
                <path d="M 0 20 L 10 40 L -10 40 Z" fill="#475569"/>
                <path d="M 0 0 Q 15 15 0 25 Q -15 15 0 0 Z" fill="#fbbf24" class="flicker-fast"/>
                <circle cx="0" cy="15" r="35" fill="#fbbf24" opacity="0.08" class="flicker-fast"/>
            </g>
            <g transform="translate(600, 90)">
                <rect x="0" y="0" width="90" height="110" fill="#78350f" stroke="#451a03" stroke-width="6"/>
                <rect x="6" y="6" width="78" height="98" fill="#1c1917"/>
                <ellipse cx="45" cy="65" rx="25" ry="35" fill="#0c0a09"/>
                <ellipse cx="45" cy="25" rx="15" ry="20" fill="#0c0a09"/>
                <circle cx="38" cy="22" r="3" fill="#ef4444" class="blink-evil"/>
                <circle cx="52" cy="22" r="3" fill="#ef4444" class="blink-evil"/>
            </g>
            <path d="M 800 0 L 700 0 Q 730 40 800 80 Z" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="2"/>
            <path d="M 800 0 L 730 0 Q 750 30 800 50 Z" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="2"/>
            <rect y="310" width="800" height="10" fill="#09060d"/>
            <rect y="320" width="800" height="80" fill="#0f0a14"/>
            <line x1="0" y1="340" x2="800" y2="340" stroke="#000" stroke-width="3"/>
            <line x1="0" y1="365" x2="800" y2="365" stroke="#000" stroke-width="4"/>
            <line x1="0" y1="390" x2="800" y2="390" stroke="#000" stroke-width="5"/>
        </g>
        <g id="fg-col">
            <rect x="700" y="0" width="100" height="400" fill="#030205"/>
            <rect x="685" y="0" width="15" height="400" fill="#010102"/>
            <rect x="700" y="0" width="5" height="400" fill="#090514"/>
        </g>
    </defs>
    <style>
        .scroll-wall { animation: scroll-left 10s infinite linear; }
        .scroll-fg { animation: scroll-left 4s infinite linear; }
        @keyframes scroll-left {
            0% { transform: translateX(0); }
            100% { transform: translateX(-800px); }
        }
        .bob-all { animation: walk-bob 0.6s infinite ease-in-out; }
        @keyframes walk-bob {
            0%, 100% { transform: translateY(4px); }
            50% { transform: translateY(-3px); }
        }
        .leg-f { animation: walk-leg 1.2s infinite ease-in-out; transform-origin: 400px 270px; }
        .leg-b { animation: walk-leg 1.2s infinite ease-in-out; transform-origin: 400px 270px; animation-delay: -0.6s; }
        @keyframes walk-leg {
            0% { transform: rotate(-35deg); }
            50% { transform: rotate(35deg); }
            100% { transform: rotate(-35deg); }
        }
        .arm-b { animation: walk-arm 1.2s infinite ease-in-out; transform-origin: 397px 217px; animation-delay: -0.6s; }
        @keyframes walk-arm {
            0%, 100% { transform: rotate(30deg); }
            50% { transform: rotate(-30deg); }
        }
        .shadow-pulse { animation: shadow-scale 0.6s infinite ease-in-out; transform-origin: 400px 335px; }
        @keyframes shadow-scale {
            0%, 100% { transform: scaleX(1); opacity: 0.7; }
            50% { transform: scaleX(1.3); opacity: 0.3; }
        }
        .flicker { animation: flashlight-flicker 4s infinite; }
        @keyframes flashlight-flicker {
            0%, 100% { opacity: 0.9; }
            20%, 22% { opacity: 0.4; }
            25% { opacity: 0.95; }
            65%, 67% { opacity: 0.3; }
            70% { opacity: 0.8; }
        }
        .flicker-fast { animation: flash-fast 0.2s infinite alternate; }
        @keyframes flash-fast { from { opacity: 0.8; } to { opacity: 1; } }
        .blink-evil { animation: evil-eye 6s infinite; }
        @keyframes evil-eye {
            0%, 46%, 54%, 100% { opacity: 1; transform: scale(1); }
            48%, 52% { opacity: 0.1; transform: scale(0.2); }
            50% { opacity: 1; transform: scale(1.2); }
        }
        .lightning { animation: thunder-flash 12s infinite; }
        @keyframes thunder-flash {
            0%, 93%, 97%, 100% { opacity: 0; }
            94%, 96%, 98% { opacity: 0.4; }
            95% { opacity: 1; }
        }
        .led-blink { animation: led 1s infinite step-end; }
        @keyframes led { 50% { fill: #065f46; } }
        .ghost-1 { animation: float-chase 14s infinite ease-in-out; }
        @keyframes float-chase {
            0% { transform: translate(-150px, 150px) scale(0.8); opacity: 0; }
            15% { opacity: 0.8; }
            50% { transform: translate(120px, 80px) scale(1); }
            85% { opacity: 0.8; }
            100% { transform: translate(-150px, 200px) scale(0.6); opacity: 0; }
        }
        .ghost-2 { animation: float-updown 7s infinite ease-in-out; }
        @keyframes float-updown {
            0%, 100% { transform: translate(520px, 30px) scale(0.7); }
            50% { transform: translate(490px, 60px) scale(0.75); }
        }
        .ghost-3 { animation: peek-a-boo 9s infinite ease-in-out; }
        @keyframes peek-a-boo {
            0%, 20%, 80%, 100% { transform: translate(650px, 350px) scale(0.5); opacity: 0; }
            40%, 60% { transform: translate(650px, 200px) scale(0.6); opacity: 0.9; }
        }
        .dust { fill: #fff; opacity: 0; }
        .d1 { animation: dust-drift 5s infinite linear; }
        .d2 { animation: dust-drift 6s infinite linear 2s; }
        .d3 { animation: dust-drift 4s infinite linear 1s; }
        @keyframes dust-drift {
            0% { transform: translate(0, 0); opacity: 0; }
            20% { opacity: 0.4; }
            80% { opacity: 0.4; }
            100% { transform: translate(-120px, -40px); opacity: 0; }
        }
    </style>
    <g class="scroll-wall">
        <use href="#bg-wall" x="0" />
        <use href="#bg-wall" x="800" />
    </g>
    <circle cx="500" cy="200" r="1.5" class="dust d1"/>
    <circle cx="650" cy="150" r="2" class="dust d2"/>
    <circle cx="350" cy="250" r="1" class="dust d3"/>
    <use href="#ghost-shape" class="ghost-1" />
    <use href="#ghost-shape" class="ghost-2" />
    <use href="#ghost-shape" class="ghost-3" />
    <g id="hunter">
        <ellipse cx="400" cy="335" rx="22" ry="5" fill="#000" class="shadow-pulse"/>
        <g class="bob-all">
            <rect x="390" y="210" width="14" height="42" rx="7" fill="#080c14" class="arm-b"/>
            <rect x="393" y="270" width="14" height="65" rx="7" fill="#080c14" class="leg-b"/>
            <rect x="355" y="195" width="35" height="60" rx="6" fill="#0a0f18"/>
            <rect x="348" y="205" width="12" height="40" rx="4" fill="#0d9488"/>
            <line x1="365" y1="195" x2="365" y2="160" stroke="#475569" stroke-width="4"/>
            <circle cx="365" cy="160" r="5" fill="#10b981" class="led-blink" filter="url(#glow)"/>
            <circle cx="372" cy="235" r="4" fill="#ef4444" class="led-blink"/>
            <rect x="382" y="200" width="38" height="75" rx="12" fill="#131c2e"/>
            <path d="M 385 200 L 415 250" stroke="#0a0f18" stroke-width="4"/>
            <rect x="385" y="162" width="36" height="45" rx="14" fill="#131c2e"/>
            <path d="M 385 175 L 440 175 L 435 185 L 385 185 Z" fill="#0a0f18"/>
            <rect x="405" y="180" width="22" height="12" rx="5" fill="#06b6d4" filter="url(#glow)"/>
            <rect x="410" y="182" width="6" height="8" rx="2" fill="#cffafe"/>
            <rect x="393" y="270" width="16" height="65" rx="8" fill="#1e293b" class="leg-f"/>
            <g transform="rotate(-6, 400, 220)">
                <rect x="395" y="210" width="50" height="15" rx="7.5" fill="#1e293b"/>
                <rect x="435" y="208" width="25" height="19" rx="5" fill="#0f172a"/>
                <rect x="455" y="204" width="18" height="27" rx="3" fill="#334155"/>
                <rect x="470" y="202" width="8" height="31" rx="2" fill="#0f172a"/>
                <polygon points="478,217.5 800,50 800,380" fill="url(#beam-grad)" class="flicker" style="mix-blend-mode: screen;"/>
            </g>
        </g>
    </g>
    <g class="scroll-fg">
        <use href="#fg-col" x="0" />
        <use href="#fg-col" x="800" />
    </g>
    <radialGradient id="vignette" cx="50%" cy="50%" r="70%">
        <stop offset="60%" stop-color="#000" stop-opacity="0"/>
        <stop offset="100%" stop-color="#000" stop-opacity="0.8"/>
    </radialGradient>
    <rect width="800" height="400" fill="url(#vignette)" pointer-events="none"/>
</svg>

## robotics_papers

${\LaTeX}$ Template: `neurips_2023`

[Template](https://github.com/nicewang/robotics_papers/actions/runs/21002896691/artifacts/5129631517)
- [ ] Move to a valid position.

### Journal

#### TRO
IEEE Transactions on Robotics
##### 2024
- [FlowMPC: Learning a Generalizable Trajectory Sampling Distribution for Model Predictive Control](journal/TRO/24/FlowMPC)


### Conf

#### CoRL
Conference on Robot Learning. PMLR.
##### 2021
- [Meshing Box: Explicitly Encouraging Low Fractional Dimensional Trajectories via Reinforcement Learning](conf/corl/21/meshing_box/)

#### ICRA
IEEE International Conference on Robotics
##### 2024
- [A GP-based Robust Motion Planning Framework for Agile Autonomous Robot Navigation and Recovery in Unknown Environments](conf/icra/24/gp_based_motion_planing_frame_4_navi_recov_in_unknown_envs)

##### 2025
- [BoxMap: Efficient Structural Mapping and Navigation](conf/icra/25/boxmap)

##### 2026
- [CLF-RL: Chasing Stability: Humanoid Running via Control Lyapunov Function Guided Reinforcement Learning](conf/icra/26/CLF-RL)

#### HRI
ACM/IEEE International Conference on Human-Robot Interaction
##### 2025
- [CLEA: Contrastive Learning from Exploratory Actions: Leveraging Natural Interactions for Preference Elicitation](conf/HRI/25/CLEA)
